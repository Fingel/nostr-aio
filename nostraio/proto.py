from nostraio.key import PrivateKey
from nostraio.event import Event


def sign_event(pk: PrivateKey, event: Event) -> str:
    """
    Returns an event signature as hex.
    """
    signature = pk.sign(bytes.fromhex(event.event_id()))
    return signature.hex()
