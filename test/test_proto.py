from nostraio.proto import sign_event
from nostraio.key import PrivateKey
from nostraio.event import Event, Kind


def test_sign_event():
    event = Event(
        public_key="test",
        kind=Kind.TEXT_NOTE,
        content="derp",
    )
    pk = PrivateKey()
    assert len(sign_event(pk, event)) == 128
