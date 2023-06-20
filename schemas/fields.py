import re
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import PydanticCustomError, core_schema

# https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
post_code_regex = re.compile(
    r"(?:"
    r"([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?"
    r"([0-9][A-Z]{2})|"
    r"(BFPO) ?([0-9]{1,4})|"
    r"(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|"
    r"([A-Z]{2}) ?([0-9]{2})|"
    r"(GE) ?(CX)|"
    r"(GIR) ?(0A{2})|"
    r"(SAN) ?(TA1)"
    r")"
)


class PostCodeAnnotation:
    """
    Partial UK postcode validation. Note: this is just an example, and is not
    intended for use in production; in particular this does NOT guarantee
    a postcode exists, just that it has a valid format.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern="^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$",
            # some example postcodes
            examples=["SP11 9DG", "W1J 7BU"],
        )
        return json_schema

    @classmethod
    def validate(cls, v: str):
        m = post_code_regex.fullmatch(v.upper())
        if m:
            return f"{m.group(1)} {m.group(2)}"
        else:
            raise PydanticCustomError("postcode", "invalid postcode format")
