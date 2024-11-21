import logging
from enum import StrEnum
from pathlib import Path
from typing import Any

import lxml

from gds import BaseAPI, Env, RequestResult, SOAPMixin, XMLMixin

from .amadeus_mixin import AmadeusErrorsMixin, AmadeusTemplatesMixin, AmadeusXMLItemsMixin

logger = logging.Logger(__name__)


class InfoStatAction(StrEnum):
    queue_info = "queue_info"
    queue_error = "queue_error"
    queue_alert = "queue_alert"
    pnr_info = "pnr_info"
    pnr_error = "pnr_error"
    pnr_delete_error = "pnr_delete_error"


class AmadeusAPI(
    BaseAPI,
    SOAPMixin,
    XMLMixin,
    AmadeusTemplatesMixin,
    AmadeusXMLItemsMixin,
    AmadeusErrorsMixin,
):
    AgentDutyCode = "SU"
    POS_Type = "1"
    RequestorType = "U"
    SourceQualifier1 = 4
    IdentificationType = "C"
    ItemNumber = 0

    API_URLS = {
        Env.development: "https://nodeD3.test.webservices.amadeus.com/1ASIWTRXRXE",
        Env.production: "https://noded3.production.webservices.amadeus.com/1ASIWTRXRXE",
    }

    def __init__(
        self,
        username: str,
        password: str,
        officeid: str,
        pseudocitycode: str,
        workdir: Path,
        notify_slack: bool = False,
        env: Env = Env.development,
        queue_alert_total_accessible_ratio: float = 2.0,
        queue_alert_level_accessible: int = 100,
    ):
        self.username = username
        self.password = password
        self.officeid = officeid
        self.pseudocitycode = pseudocitycode
        self.env = env
        self.notify_slack = notify_slack
        self.workdir = workdir
        self.queue_alert_total_accessible_ratio = queue_alert_total_accessible_ratio
        self.queue_alert_level_accessible: int = queue_alert_level_accessible

    def _base_placeholders(self) -> dict:
        return {
            "messageid": self.get_uuid_as_str(),
            "to": self.API_URLS[self.env],
            "username": self.username,
            "nonce": self.get_nonce64(),
            "password": self.password,
            "created": str(self.utc_date()),
            "agentdutycode": AmadeusAPI.AgentDutyCode,
            "requestortype": AmadeusAPI.RequestorType,
            "pseudocitycode": self.pseudocitycode,
            "pos_type": AmadeusAPI.POS_Type,
            "sourcequalifier1": AmadeusAPI.SourceQualifier1,
            "inhouseidentification1": self.officeid,
            "identificationtype": AmadeusAPI.IdentificationType,
            "itemnumber": AmadeusAPI.ItemNumber,
        }

    @staticmethod
    def get_headers(action_code: str, encoded_request_len: int) -> dict:
        return {
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": str(encoded_request_len),
            "Accept-Encoding": "gzip, deflate",
            "SOAPAction": f"http://webservices.amadeus.com/{action_code}",
            "Host": "nodeD3.test.webservices.amadeus.com",
            # "Host":  "noded3.production.webservices.amadeus.com",
            "Connection": "Keep-Alive",
        }

    def _log_queue_info(self, xml_root: lxml.etree.ElementTree, env_data: dict | None = None) -> None:
        if number_of_units := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_NUMBER_OF_UNITS):
            env_data = env_data if env_data is dict else {}
            total = number_of_units[0].text
            accessible = number_of_units[1].text
            shown = number_of_units[2].text
            logger.info(
                "Queue *`%s`* state: Total: *`%s`*, Accessible: *`%s`*  Shown: *`%s`*.  RequestID: *`%s`*",
                env_data.get("queuenumber"),
                total,
                accessible,
                shown,
                env_data.get("messageid"),
                extra={"notify_slack": self.notify_slack},
            )

    def _log_queue_alert(self, xml_root: lxml.etree.ElementTree, env_data: dict | None = None) -> None:
        if number_of_units := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_NUMBER_OF_UNITS):
            env_data = env_data if env_data is dict else {}
            total = number_of_units[0].text
            accessible = number_of_units[1].text
            if float(total) / float(accessible) >= self.queue_alert_total_accessible_ratio:
                logger.warning(
                    "*WARNING*  Queue *`%s`* Total: *`%s`*, Accessible: *`%s`* Exceeded ratio *`%s`*.  RequestID: *`%s`*",
                    env_data.get("queuenumber"),
                    total,
                    accessible,
                    self.queue_alert_total_accessible_ratio,
                    env_data.get("messageid"),
                    extra={"notify_slack": self.notify_slack},
                )
            if float(accessible) >= float(self.queue_alert_level_accessible):
                logger.warning(
                    "*WARNING*  Queue *`%s`*  Accessible: *`%s`* > *`%s`*.  RequestID: *`%s`*",
                    env_data.get("queuenumber"),
                    accessible,
                    self.queue_alert_level_accessible,
                    env_data.get("messageid"),
                    extra={"notify_slack": self.notify_slack},
                )

    def _log_queue_error(self, xml_root: lxml.etree.ElementTree, env_data: dict | None = None) -> None:
        if error_codes := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_ERROR_CODE):
            env_data = env_data if env_data is dict else {}
            error_code = error_codes[0]
            logger.error(
                "*ERROR* Queue *`%s`* error code: *`%s`* - *`%s`*. RequestID: *`%s`*",
                env_data.get("queuenumber"),
                error_code,
                self.QUERY_LIST_ERROR.get(error_code),
                env_data.get("messageid"),
                extra={"notify_slack": self.notify_slack},
            )

    def _log_pnr_delete(self, xml_root: lxml.etree.ElementTree, env_data: dict | None = None) -> None:
        if error_codes := self.get_all_xml_elements(xml_root=xml_root, selector=self.PNR_DELETE_ERROR_CODE):
            env_data = env_data if env_data is dict else {}
            error_code = error_codes[0]
            logger.error(
                "*ERROR* Queue *`%s`* error code: *`%s`* - *`%s`*. RequestID: *`%s`*",
                env_data.get("queuenumber"),
                error_code,
                self.QUERY_LIST_ERROR.get(error_code),
                env_data.get("messageid"),
                extra={"notify_slack": self.notify_slack},
            )

    def _inform_stat(self, xml_str: str, stat_actions: list[InfoStatAction], env_data: dict | None = None) -> None:
        if xml_root := self.str_to_xml(xml_str):
            actions_set = set(stat_actions)
            for stat_action in actions_set:
                match stat_action:
                    case InfoStatAction.queue_info:
                        self._log_queue_info(xml_root, env_data=env_data)
                    case InfoStatAction.queue_alert:
                        self._log_queue_alert(xml_root, env_data=env_data)
                    case InfoStatAction.queue_error:
                        self._log_queue_error(xml_root, env_data=env_data)
                    case InfoStatAction.pnr_delete_error:
                        self._log_pnr_delete(xml_root, env_data=env_data)
                    case InfoStatAction.pnr_info:
                        self._log_pnr_info(xml_root, env_data=env_data)

    def _prepare_request_body(self, **parameters) -> str | None:
        template_error: bool
        request_body: str | None = None
        action_code: str
        if action_code := parameters.get(action_code):
            placeholders_data: dict = (
                self._base_placeholders() | parameters | {"action": f"http://webservices.amadeus.com/{action_code}"}
            )
            template_error, request_body = self.fill_out_template(
                template_name=action_code, template_values=placeholders_data
            )
            if template_error:
                logger.error("Template `%s` filling error. Placeholders '%і'", action_code, placeholders_data)
                return None

        return request_body

    def _send_post_request(self, action_code: str, request_body: str) -> str | None:
        if logger.getEffectiveLevel() == "DEBUG":
            _saved_file = self.save_session_file(
                root_dir=self.workdir / "session",
                file_name=f"{self.utc_date_short()}_{action_code}_req.xml".lower(),
                data=self.pretty_xml(request_body),
            )
        encoded_request_body: bytes = request_body.encode("utf-8")
        headers: dict = self.get_headers(action_code=action_code, encoded_request_len=len(encoded_request_body))
        response: RequestResult = self.post_request_text(
            url=AmadeusAPI.API_URLS[self.env],
            headers=headers,
            data=encoded_request_body,
        )
        if response.request_err:
            logger.error(
                "Request `%s` error '%s'. Status code: `%s`. URL: '%s'",
                action_code,
                response.request_err,
                response.status_code,
                AmadeusAPI.API_URLS[self.env],
            )
            return None
        if logger.getEffectiveLevel() == "DEBUG":
            _saved_file = self.save_session_file(
                root_dir=self.workdir / "session",
                file_name=f"{self.utc_date_short()}_{action_code}_resp.xml".lower(),
                data=self.pretty_xml(request_body),
            )
        return response.response_text

    def _get_queue_info(self, queuenumber: int) -> str | None:
        action_code = "QDQLRQ_11_1_1A"
        request_body: str | None
        if not (request_body := self._prepare_request_body(action_code=action_code, queuenumber=queuenumber)):
            logger.error("Request creation error for action `%s`", action_code)
            return None

        return self._send_post_request(action_code=action_code, request_body=request_body)

    def get_pnr_list(self, queuenumber: int) -> list[str] | None:
        response_text: str | None
        record_locators: list[Any] | None
        if (response_text := self._get_queue_info(queuenumber=queuenumber)) and (
            record_locators := self.get_all_xml_elements(
                xml_root=self.str_to_xml(response_text), selector=self.QUEUE_CONTROL_NUMBERS
            )
        ):
            return [pnr.text for pnr in record_locators]
        return None

    def _get_pnr_info(self, controlnumber: str) -> str | None:
        action_code = "PNRRET_17_1_1A"
        request_body: str | None
        if not (request_body := self._prepare_request_body(action_code=action_code, controlnumber=controlnumber)):
            logger.error("Request creation error for action `%s`", action_code)
            return None
        return self._send_post_request(action_code=action_code, request_body=request_body)

    def get_pnr(self, controlnumber: str) -> str | None:
        response_text: str | None
        if response_text := self._get_pnr_info(controlnumber=controlnumber):
            saved_file = self.save_session_file(
                root_dir=self.workdir / "pnr",
                file_name=f"ama_{self.get_uuid_as_str()}_{controlnumber}.xml".lower(),
                data=self.pretty_xml(response_text),
            )
            return str(saved_file)
        return None

    def delete_pnr_from_queue(self, queuenumber: int, controlnumber: str) -> bool:
        action_code = "QUQMDQ_03_1_1A"
        request_body: str | None
        if not (
            request_body := self._prepare_request_body(
                action_code=action_code, queuenumber=queuenumber, controlnumber=controlnumber
            )
        ):
            logger.error("Request creation error for action `%s`", action_code)
            return False
        response = self._send_post_request(action_code=action_code, request_body=request_body)
