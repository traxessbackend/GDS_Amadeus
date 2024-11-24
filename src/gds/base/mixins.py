import base64
import hashlib
import random
import re
import string
from datetime import datetime
from typing import Any

import lxml
import lxml.etree

from helpers.ulid_helper import ulid_as_str


class SOAPMixin:
    @staticmethod
    def get_random_string(length: int) -> str:
        return "".join([random.choice(string.ascii_letters + string.digits) for n in range(length)])

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
    def get_nonce64(nonce_length: int = 16) -> str:
        nonce = SOAPMixin.get_random_string(nonce_length)
        return base64.b64encode(nonce.encode("utf-8")).decode("utf-8")

    @staticmethod
    def all_placeholders_filled(filled_template: str) -> bool:
        if re.search(r"{[^{}]*}", filled_template):
            return False  # Unfilled placeholders found
        return True  # All placeholders are filled

    @classmethod
    def get_template_by_name(cls, template_name: str) -> str | None:
        return getattr(cls, template_name, None)

    @classmethod
    def fill_out_template(
        cls, template_name: str, template_values: dict, strict_mode: bool = True
    ) -> tuple[bool, str | None]:
        result: bool = False
        result_template: str | None = None
        if (template := cls.get_template_by_name(template_name)) and (
            result_template := template.format(template_values)
        ):
            if strict_mode and cls.all_placeholders_filled(result_template):
                result = True
        return result, result_template


class XMLMixin:
    @staticmethod
    def str_to_xml(xml_str: str) -> lxml.etree.ElementTree | None:
        xml_root: lxml.etree.ElementTree | None = None
        if xml_str:
            try:
                xml_root = lxml.etree.fromstring(xml_str)
            except:
                pass
        return xml_root

    @staticmethod
    def pretty_xml(xml_str: str) -> str:
        return lxml.etree.tostring(lxml.etree.XML(xml_str.encode("utf-8")), pretty_print=True)

    @staticmethod
    def get_all_xml_elements(xml_root: lxml.etree.ElementTree, selector: str) -> list[Any] | None:
        found_items = xml_root.findall(selector)
        return found_items
