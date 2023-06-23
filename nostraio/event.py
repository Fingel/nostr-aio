import json
import hashlib
from enum import IntEnum
from time import time
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


class Kind(IntEnum):
    SET_METADATA = 0
    TEXT_NOTE = 1
    RECOMMEND_SERVER = 2


class Event:
    def __init__(
        self, public_key: str, kind: Kind, content: str, created_at: int = int(time())
    ) -> None:
        self.public_key = public_key
        self.kind = kind
        self.content = content
        self.tags = []
        self.created_at = created_at
        self.signature = ""

    def add_event_tag(self, event: str, rec_relay_url: str = "") -> None:
        tag = ["e", event]
        if rec_relay_url:
            tag.append(rec_relay_url)
        self.tags.append(tag)

    def add_pubkey_tag(self, public_key: str, rec_relay_url: str = "") -> None:
        tag = ["p", public_key]
        if rec_relay_url:
            tag.append(rec_relay_url)
        self.tags.append(tag)

    def event_id(self) -> str:
        raw = [0, self.public_key, self.created_at, self.kind, self.tags, self.content]
        as_json = json.dumps(raw, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(as_json.encode()).hexdigest()

    def set_signature(self, signature: str) -> None:
        self.signature = signature

    def to_json(self) -> str:
        if not self.signature:
            raise ValueError("Signature not set, call set_signature()")
        return json.dumps(
            [
                "EVENT",
                {
                    "id": self.event_id(),
                    "pubkey": self.public_key,
                    "created_at": self.created_at,
                    "kind": self.kind,
                    "tags": self.tags,
                    "content": self.content,
                    "sig": self.signature,
                },
            ]
        )
