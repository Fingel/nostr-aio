from nostr.key import PrivateKey


def test_generate_new_key():
    pk = PrivateKey()
    assert pk.hex
    assert pk.raw
    assert pk.public_key.hex
    assert pk.public_key.raw


def test_instantiate_key():
    raw = b"0" * 32
    pk = PrivateKey(raw)
    assert pk.raw == raw
    assert (
        pk.public_key.hex
        == "2ed557f5ad336b31a49857e4e9664954ac33385aa20a93e2d64bfe7f08f51277"
    )
