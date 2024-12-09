import base64
import hashlib
import logging
import random
import re
import string
from datetime import datetime
from typing import Any

from lxml.etree import XML, ElementTree, _Element, fromstring, tostring

from helpers.ulid_helper import ulid_as_str, uuid_as_str

logger = logging.Logger(__name__)


class SOAPMixin:
    @staticmethod
    def get_random_string(length: int) -> str:
        return "".join([random.choice(string.ascii_letters + string.digits) for n in range(length)])

    @staticmethod
    def get_uuid_as_str() -> str:
        return uuid_as_str()

    @staticmethod
    def get_ulid_as_str() -> str:
        return ulid_as_str()

    @staticmethod
    def get_digest(password: str, nonce: str, created_timestamp: datetime) -> str:
        timestamp = created_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        # password_sha1 = hashlib.sha1(password.encode("utf-8")).digest()
        digest = base64.b64encode(
            hashlib.sha1(
                nonce.encode("utf-8") + timestamp.encode("utf-8") + hashlib.sha1(password.encode("utf-8")).digest()
            ).digest()
        )
        return digest.decode("utf-8")

    @staticmethod
    def generate_nonce(nonce_length: int = 16) -> str:
        return SOAPMixin.get_random_string(nonce_length)

    @staticmethod
    def get_nonce64(nonce: str) -> str:
        return base64.b64encode(nonce.encode("utf-8")).decode("utf-8")

    @classmethod
    def get_template_by_name(cls, template_name: str) -> str | None:
        return getattr(cls, template_name, None)

    @classmethod
    def fill_out_template(cls, template_name: str, template_values: dict) -> tuple[bool, str | None]:
        error: bool = True
        result_template: str | None = None
        try:
            if template := cls.get_template_by_name(template_name):
                result_template = template.format(**template_values)
                error = False
        except (KeyError, IndexError) as exc:
            logger.error("Key/Index Error `%s` in template `%s`. Values: `%s`", template_name, template_values)
        return error, result_template


class XMLMixin:
    @staticmethod
    def str_to_xml(xml_str: str) -> _Element | None:
        xml_root: _Element | None = None
        if xml_str:
            try:
                xml_root = fromstring(xml_str.encode())
            except Exception as exc:
                logger.error("`String to XML error  %s`", exc)
        return xml_root

    @staticmethod
    def pretty_xml(xml_str: str) -> str:
        return tostring(XML(xml_str), pretty_print=True).decode()

    @staticmethod
    def get_all_xml_elements(xml_root: ElementTree, selector: str) -> list[Any] | None:
        found_items = xml_root.findall(selector)
        return found_items
