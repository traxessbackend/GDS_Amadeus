import logging
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import Any

import lxml

from gds import BaseAPI, Env, RequestResult, SOAPMixin, XMLMixin
from helpers.files_helper import copy_file
from settings import settings

from .amadeus_mixin import AmadeusErrorsMixin, AmadeusTemplatesMixin, AmadeusXMLItemsMixin

logger = logging.Logger(__name__)


class InfoStatAction(StrEnum):
    QUEUE_INFO = "QUEUE_INFO"
    QUEUE_ERROR = "QUEUE_ERROR"
    QUEUE_ALERT = "QUEUE_ALERT"
    GET_PNR_ERROR = "GET_PNR_ERROR"
    DELETE_PNR_ERROR = "DELETE_PNR_ERROR"


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
        queue_alert_total_accessible_ratio: int = 100,
        queue_alert_level_accessible: Decimal = Decimal(2.0),
    ):
        self.username = username
        self.password = password
        self.officeid = officeid
        self.pseudocitycode = pseudocitycode
        self.env = env
        self.notify_slack = notify_slack
        self.workdir = Path(workdir)
        self.queue_alert_total_accessible_ratio = queue_alert_total_accessible_ratio
        self.queue_alert_level_accessible = queue_alert_level_accessible

        self.request_context = {}

    def _base_placeholders(self) -> dict:
        nonce = self.generate_nonce()
        created_at = self.utc_date()
        created_at_str = created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            "messageid": self.get_ulid_as_str(),
            # "to": self.API_URLS[self.env],
            # Amadeus bug - always `https://nodeD3.test.webservices.amadeus.com/1ASIWTRXRXE`
            "to": "https://nodeD3.test.webservices.amadeus.com/1ASIWTRXRXE",
            "username": self.username,
            "nonce": self.get_nonce64(nonce),
            "password": self.get_digest(password=self.password, nonce=nonce, created_timestamp=created_at),
            "created": created_at_str,
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

    def _log_queue_info(self, xml_root: lxml.etree.ElementTree) -> None:
        if number_of_units := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_NUMBER_OF_UNITS):
            queuenumber = self.request_context.get("queuenumber")
            messageid = self.request_context.get("messageid")
            total = number_of_units[0].text
            accessible = number_of_units[1].text
            shown = number_of_units[2].text
            logger.info(
                "Queue *`%s`* state: Total: *`%s`*, Accessible: *`%s`*  Shown: *`%s`*.  MessageID: *`%s`*",
                queuenumber,
                total,
                accessible,
                shown,
                messageid,
                extra={"notify_slack": self.notify_slack},
            )
        return None

    def _log_queue_alert(self, xml_root: lxml.etree.ElementTree) -> None:
        if number_of_units := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_NUMBER_OF_UNITS):
            queuenumber = self.request_context.get("queuenumber")
            messageid = self.request_context.get("messageid")
            total = number_of_units[0].text
            accessible = number_of_units[1].text
            if int(total) / int(accessible) >= self.queue_alert_total_accessible_ratio:
                logger.warning(
                    "*WARNING*  Queue *`%s`* Total: *`%s`*, Accessible: *`%s`* Exceeded ratio *`%s`*.  MessageID: *`%s`*",
                    queuenumber,
                    total,
                    accessible,
                    self.queue_alert_total_accessible_ratio,
                    messageid,
                    extra={"notify_slack": self.notify_slack},
                )
            if int(accessible) >= self.queue_alert_level_accessible:
                logger.warning(
                    "*WARNING*  Queue *`%s`*  Accessible: *`%s`* > *`%s`*.  MessageID: *`%s`*",
                    queuenumber,
                    accessible,
                    self.queue_alert_level_accessible,
                    messageid,
                    extra={"notify_slack": self.notify_slack},
                )
        return None

    def _log_queue_error(self, xml_root: lxml.etree.ElementTree) -> dict[str, str] | None:
        if error_codes := self.get_all_xml_elements(xml_root=xml_root, selector=self.QUEUE_ERROR_CODE):
            queuenumber = self.request_context.get("queuenumber")
            messageid = self.request_context.get("messageid")
            error_code_str = error_codes[0].text.strip().upper()
            error_code_desc = self.ERRORS_PNR_LIST_IN_QUEUE.get(error_code_str).strip().upper()
            if error_code_str:
                logger.error(
                    "*ERROR* Queue *`%s`* error code: *`%s`* - *`%s`*. MessageID: *`%s`*",
                    queuenumber,
                    error_code_str,
                    error_code_desc,
                    messageid,
                    extra={"notify_slack": self.notify_slack},
                )
            return {error_code_str: error_code_desc}
        return None

    def _log_pnr_delete(self, xml_root: lxml.etree.ElementTree) -> dict[str, str] | None:
        if error_codes := self.get_all_xml_elements(xml_root=xml_root, selector=self.PNR_DELETE_ERROR_CODE):
            queuenumber = self.request_context.get("queuenumber")
            messageid = self.request_context.get("messageid")
            error_code_str = error_codes[0].strip().upper()
            error_code_desc = self.ERRORS_DELETE_PNR_FROM_QUEUE.get(error_code_str).strip().upper()

            logger.error(
                "*ERROR* Queue *`%s`* error code: *`%s`* - *`%s`*. RequestID: *`%s`*",
                queuenumber,
                error_code_str,
                error_code_desc,
                messageid,
                extra={"notify_slack": self.notify_slack},
            )
            return {error_code_str: error_code_desc}
        return None

    def _log_get_pnr_error(self, xml_root: lxml.etree.ElementTree) -> dict[str, str] | None:
        if error_codes := self.get_all_xml_elements(xml_root=xml_root, selector=self.PNR_GET_ERROR_CODE):
            error_code_str = error_codes[0].strip().upper()
            error_code_desc = self.ERRORS_PNR_RETRIEVE.get(error_code_str).strip().upper()

            logger.error(
                "*ERROR* GET PNR *`%s`* FROM QUEUE *`%s`* error code: *`%s`* - *`%s`*. RequestID: *`%s`*",
                self.request_context.get("controlnumber"),
                self.request_context.get("queuenumber"),
                error_code_str,
                error_code_desc,
                self.request_context.get("messageid"),
                extra={"notify_slack": self.notify_slack},
            )
            return {error_code_str: error_code_desc}
        return None

    def _prepare_request_body(self, **parameters) -> str | None:
        template_error: bool
        request_body: str | None = None
        action_code: str
        if action_code := parameters.get("action_code"):
            placeholders_data: dict = (
                self._base_placeholders() | parameters | {"action": f"http://webservices.amadeus.com/{action_code}"}
            )
            self.request_context.update(placeholders_data)
            template_error, request_body = self.fill_out_template(
                template_name=action_code, template_values=placeholders_data
            )
            if template_error:
                logger.error("Template `%s` filling error. Placeholders '%і'", action_code, placeholders_data)
                return None

        return request_body

    def _send_post_request(self, action_code: str, request_body: str) -> str | None:
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            _saved_file = self.save_session_file(
                folder=self.workdir / "session",
                file_name=f"{self.get_ulid_as_str()}_{action_code}_req.xml".lower(),
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
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            _saved_file = self.save_session_file(
                folder=self.workdir / "session",
                file_name=f"{self.get_ulid_as_str()}_{action_code}_resp.xml".lower(),
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

    def _get_pnr_info(self, controlnumber: str) -> str | None:
        action_code = "PNRRET_17_1_1A"
        request_body: str | None
        if not (request_body := self._prepare_request_body(action_code=action_code, controlnumber=controlnumber)):
            logger.error("Request creation error for action `%s`", action_code)
            return None
        return self._send_post_request(action_code=action_code, request_body=request_body)

    def _delete_pnr_from_queue(self, queuenumber: int, controlnumber: str) -> str | None:
        action_code = "QUQMDQ_03_1_1A"
        request_body: str | None
        if not (
            request_body := self._prepare_request_body(
                action_code=action_code, queuenumber=queuenumber, controlnumber=controlnumber
            )
        ):
            logger.error("Request creation error for action `%s`", action_code)
            return None
        return self._send_post_request(action_code=action_code, request_body=request_body)

    def status_inform(self, xml_root: lxml.etree.ElementTree, action: InfoStatAction) -> dict | None:
        result: dict | None = None
        match action:
            case InfoStatAction.QUEUE_INFO:
                result = self._log_queue_info(xml_root)
            case InfoStatAction.QUEUE_ALERT:
                result = self._log_queue_alert(xml_root)
            case InfoStatAction.QUEUE_ERROR:
                result = self._log_queue_error(xml_root)
            case InfoStatAction.GET_PNR_ERROR:
                result = self._log_get_pnr_error(xml_root)
            case InfoStatAction.DELETE_PNR_ERROR:
                result = self._log_pnr_delete(xml_root)
        return result

    def get_pnr_list(self, queuenumber: int) -> list[str] | None:
        response_text: str | None
        record_locators: list[Any] | None
        self.request_context = {"queuenumber": queuenumber}
        if response_text := self._get_queue_info(queuenumber=queuenumber):
            xml_root = self.str_to_xml(response_text)
            if xml_root is not None and (not self.status_inform(xml_root=xml_root, action=InfoStatAction.QUEUE_ERROR)):
                self.status_inform(xml_root=xml_root, action=InfoStatAction.QUEUE_INFO)
                self.status_inform(xml_root=xml_root, action=InfoStatAction.QUEUE_ALERT)

                record_locators = self.get_all_xml_elements(
                    xml_root=self.str_to_xml(response_text), selector=self.QUEUE_CONTROL_NUMBERS
                )
                return [pnr.text for pnr in record_locators]
        return None

    def get_pnr(self, controlnumber: str, queuenumber: int) -> str | None:
        response_text: str | None
        if response_text := self._get_pnr_info(controlnumber=controlnumber):
            xml_root = self.str_to_xml(response_text)
            self.request_context = {"controlnumber": controlnumber, "queuenumber": queuenumber}
            if xml_root is not None and not self.status_inform(xml_root=xml_root, action=InfoStatAction.GET_PNR_ERROR):
                saved_pnr_file = self.save_session_file(
                    folder=self.workdir / "current_pnr",
                    file_name=f"{self.get_ulid_as_str()}_{controlnumber}.xml".lower(),
                    data=self.pretty_xml(response_text),
                )
                destination_path = self.workdir / f"out/{saved_pnr_file.name}"
                copy_file(saved_pnr_file, destination_path)
                return str(saved_pnr_file)
        return None

    def delete_pnr(self, controlnumber: str, queuenumber: int) -> str | None:
        response_text: str | None
        if settings.ENABLE_DELETE_PNR_FROM_QUEUE:
            if response_text := self._delete_pnr_from_queue(queuenumber=queuenumber, controlnumber=controlnumber):
                xml_root = self.str_to_xml(response_text)
                if xml_root is not None:
                    self.request_context = {"controlnumber": controlnumber, "queuenumber": queuenumber}
                    _ = self.status_inform(
                        xml_root=xml_root,
                        action=InfoStatAction.DELETE_PNR_ERROR,
                    )
        else:
            logger.warning("Removing PNRs from the queue is disabled in the configuration")
        return None

    def launch_work_cycle(self, queue_ids: list[int]) -> tuple[int, int]:
        pnr_ids: list[str] | None
        saved_pnr_file: str | None
        successfully_processed: int = 0
        processed_with_errors: int = 0
        for queuenumber in queue_ids:
            try:
                logger.info(
                    "*[AMADEUS]* Processing of queue number *`%s`* started at *`%s`*",
                    queuenumber,
                    datetime.now(),
                    extra={"notify_slack": self.notify_slack},
                )
                if pnr_ids := self.get_pnr_list(queuenumber=queuenumber):
                    for controlnumber in pnr_ids:
                        if saved_pnr_file := self.get_pnr(controlnumber=controlnumber):
                            self.delete_pnr(controlnumber=controlnumber, queuenumber=queuenumber)

            except Exception as exc:
                processed_with_errors += 1
                logger.error(
                    "*[AMADEUS]* Processing of queue number *`%s`* finished at *`%s`* with *ERRORS* `%s`",
                    queuenumber,
                    datetime.now(),
                    exc,
                    extra={"notify_slack": self.notify_slack},
                )
            else:
                successfully_processed += 1
                logger.info(
                    "*[AMADEUS]* Processing of queue number *`%s`* completed at *`%s`* *SUCCESSFULLY* ",
                    queuenumber,
                    datetime.now(),
                    extra={"notify_slack": self.notify_slack},
                )

        return successfully_processed, processed_with_errors
