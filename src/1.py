import lxml.etree

selector = "{http://schemas.xmlsoap.org/soap/envelope/}Body/{http://xml.amadeus.com/QDQLRR_11_1_1A}Queue_ListReply/{http://xml.amadeus.com/QDQLRR_11_1_1A}queueView/{http://xml.amadeus.com/QDQLRR_11_1_1A}item/{http://xml.amadeus.com/QDQLRR_11_1_1A}recLoc/{http://xml.amadeus.com/QDQLRR_11_1_1A}reservation/{http://xml.amadeus.com/QDQLRR_11_1_1A}controlNumber"
selector = (
    "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}Queue_ListReply/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}queueView/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}item/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}recLoc/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}reservation/"
    "{http://xml.amadeus.com/QDQLRR_11_1_1A}controlNumber"
)

fff = "/home/android/Projects/Traxess/@Refactoring/GDS/Amadeus/data/QDQLRQ_11_1_1A IN dd8ee8e8-fa9b-435f-90e3-bc0f3030171c.xml"

with open(fff, "r") as f:
    xml_str = f.read()
xml_root = lxml.etree.fromstring(xml_str)
found_items = xml_root.findall(selector)
for item in found_items:
    print(">>", item.text)

found_texts = xml_root.findtext(selector)
print()

# env_data = None
# env_data = env_data if env_data is dict else "{}"
# print(env_data)
# import logging
# import sys

# log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(log_format)
# logger.addHandler(handler)


# total = 10
# accessible = 5
# shown = 5
# env_data = {"number": 90}
# logger.info(
#     "Queue *`%s`* state: Total: *`%s`*, Accessible: *`%s`*  Shown: *`%s`*",
#     env_data.get("number"),
#     total,
#     accessible,
#     shown,
#     extra={"notify_slack": False},
# )

# import datetime

# print(datetime.datetime.utcnow())
# print(str(datetime.datetime.utcnow()))
# import ulid

# u = ulid.ULID()
# print(u)
# print(str(u))
# uhex = u.hex
# print(uhex)
# u_uuid = u.to_uuid()
# u_uuid4 = u.to_uuid4()
# print(u_uuid)
# print(u_uuid4)

# class AMixin:
#     @staticmethod
#     def a_func():
#         print("A func")


# class BMixin:
#     @staticmethod
#     def b_func():
#         print("B func")


# class CC(AMixin, BMixin):
#     def c_func(self):
#         print("C func")


# o = CC()
# o.a_func()
# o.b_func()
# o.c_func()


# class MyClass:
#     my = "My"

#     @classmethod
#     def check(cls, attr_name: str):
#         # Check if the attribute exists
#         if hasattr(cls, attr_name):
#             # Get the attribute's value
#             value = getattr(my_instance, attr_name)
#             print(f"Attribute '{attr_name}' exists with value: {value}")
#         else:
#             print(f"Attribute '{attr_name}' does not exist.")


# # Create an instance
# my_instance = MyClass()

# # Attribute name to check
# attr_name = "my1"
# my_instance.check(attr_name=attr_name)

# from pydantic import BaseModel


# class RequestResult(BaseModel):
#     request_err: str | None = None
#     status_code: int | None = None
#     response_text: str | None = None
#     response_json: dict | None = None


# class BaseAPI:
#     def _json(post_func):
#         def json_from_post(self):
#             request_err: str | None = None
#             status_code: int | None = None
#             response_json: dict | None = None
#             response = post_func(self)
#             status_code = response["status_code"]
#             if status_code == 200:
#                 response_json = response["response_json"]
#             else:
#                 request_err = response["response_text"]
#             return RequestResult(request_err=request_err, status_code=status_code, response_json=response_json)

#         return json_from_post

#     def _text(post_func):
#         def text_from_post(self):
#             request_err: str | None = None
#             status_code: int | None = None
#             response_text: str | None = None
#             response = post_func(self)
#             status_code = response["status_code"]
#             if status_code == 200:
#                 response_text = response["response_text"]
#             else:
#                 request_err = response["response_text"]
#             return RequestResult(request_err=request_err, status_code=status_code, response_text=response_text)

#         return text_from_post

#     @_text
#     def text(self) -> dict:
#         r = {}
#         r["status_code"] = 200
#         r["response_text"] = "text"
#         return r

#     @_json
#     def json(self) -> dict:
#         r = {}
#         r["status_code"] = 200
#         r["response_json"] = {"json": "json"}
#         return r


# o = BaseAPI()
# txt = o.text()
# json = o.json()
# print(f"{txt=}")
# print(f"{json=}")
