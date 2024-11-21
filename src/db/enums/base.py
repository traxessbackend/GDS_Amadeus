from enum import Enum


class CaseInsensitiveEnum(str, Enum):
    """Case insensitive enum class to be able to pass values in any case"""

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Value must be one of {[item.value for item in cls]}")
