from enum import Enum


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class IOrderEnumShort(str, Enum):
    asc = "asc"
    desc = "desc"


class IOrderEnumText(str, Enum):
    az = "AZ"
    za = "ZA"
