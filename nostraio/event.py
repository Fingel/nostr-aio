import json
from pydantic import BaseModel

FILTER_ALIASES = {"e": "#e", "p": "#p"}


def filter_alias_generator(name: str) -> str:
    return FILTER_ALIASES.get(name, name)


class Filter(BaseModel):
    ids: list[str] | None = None
    authors: list[str] | None = None
    kinds: list[int] | None = None
    e: list[str] | None = None
    p: list[str] | None = None
    since: int | None = None
    until: int | None = None
    limit: int | None = None

    class Config:
        # Lets us set Filter.e and .p but output with the # alias
        allow_population_by_field_name = True
        alias_generator = filter_alias_generator


class Request:
    def __init__(self, sub_id: str, filter: Filter) -> None:
        self.sub_id = sub_id
        self.filter = filter

    def to_message(self) -> list:
        return ["REQ", self.sub_id, self.filter.dict(exclude_unset=True, by_alias=True)]

    def to_json(self) -> str:
        return json.dumps(self.to_message())
