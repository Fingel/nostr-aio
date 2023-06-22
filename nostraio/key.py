import secrets
import secp256k1


class PublicKey:
    def __init__(self, raw_key: bytes) -> None:
        self.raw_key = raw_key

    @property
    def hex(self) -> str:
        return self.raw_key.hex()

    @property
    def raw(self) -> bytes:
        return self.raw_key


class PrivateKey:
    def __init__(self, raw_key: bytes = b"") -> None:
        if raw_key:
            self.raw_key = raw_key
        else:
            self.raw_key = secrets.token_bytes(32)
        sk = secp256k1.PrivateKey(self.raw_key)
        assert sk.pubkey  # Make sure we can access the public key
        # The prefix of the generated pubkey must be stripped
        self.public_key = PublicKey(sk.pubkey.serialize()[1:])

    @property
    def hex(self) -> str:
        return self.raw_key.hex()

    @property
    def raw(self) -> bytes:
        return self.raw_key

    def sign(self, data: bytes) -> bytes:
        sk = secp256k1.PrivateKey(self.raw_key)
        return sk.schnorr_sign(data, None, raw=True)
