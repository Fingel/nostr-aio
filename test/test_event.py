import json
import pytest
from nostraio.event import Request, Filter, Event, Kind


def test_request_filter_keys():
    # test these json keys with hash prefixes
    filtr = Filter(e=["test123"], p=["123test"])
    req = Request(sub_id="asd123", filter=filtr)
    assert json.loads(req.to_json())[2]["#e"] == filtr.e


def test_add_tags():
    event = Event(
        public_key="test",
        kind=Kind.TEXT_NOTE,
        content="derp",
    )
    event.add_event_tag("test_event", "wss://foo.bar")
    event.add_pubkey_tag("test_pubkey", "wss://bar.foo")
    event.set_signature("notreal")
    serialized_event = json.loads(event.to_json())
    assert serialized_event[1]["tags"][0][0] == "e"
    assert serialized_event[1]["tags"][1][0] == "p"


def test_event_id():
    event = Event(
        public_key="test",
        kind=Kind.TEXT_NOTE,
        content="derp",
    )
    assert len(event.event_id()) == 64


def test_must_add_signature():
    event = Event(
        public_key="test",
        kind=Kind.TEXT_NOTE,
        content="derp",
    )
    with pytest.raises(ValueError):
        event.to_json()
