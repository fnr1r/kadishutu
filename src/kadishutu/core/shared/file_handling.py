from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from typing_extensions import Self

from .encryption import decrypt, encrypt


def is_save_decrypted(data: bytearray) -> bool:
    return data[0x40:0x44] == b"GVAS"


@dataclass(repr=False)
class RawSave:
    data: bytearray

    def save(self, path: Path):
        with open(path, "wb") as file:
            file.write(self.data)

    def is_save_decrypted(self) -> bool:
        return is_save_decrypted(self.data)


class EncryptedSave(RawSave):
    @classmethod
    def open(cls, path: Path) -> Self:
        with open(path, "rb") as file:
            return cls(bytearray(file.read()))

    def decrypt(self) -> "DecryptedSave":
        assert not self.is_save_decrypted(), "Save not encrypted"
        return DecryptedSave(bytearray(decrypt(self.data)))


class DecryptedSave(RawSave):
    @classmethod
    def open(cls, path: Path) -> Self:
        with open(path, "rb") as file:
            return cls(bytearray(file.read()))

    @classmethod
    def auto_open(cls, path: Path) -> "DecryptedSave":
        with open(path, "rb") as file:
            data = bytearray(file.read())
        if not is_save_decrypted(data):
            return EncryptedSave(data).decrypt()
        else:
            return cls(data)

    def encrypt(self) -> EncryptedSave:
        assert self.is_save_decrypted(), "Save not decrypted"
        return EncryptedSave(bytearray(encrypt(self.data)))

    def hash_calculate(self):
        return sha1(self.data[0x40:])

    def hash_validate(self) -> bool:
        included_hash = self.data[:20]
        calculated_hash = self.hash_calculate()
        return included_hash == calculated_hash.digest()

    def hash_update(self):
        new_hash = self.hash_calculate()
        data = self.data
        self.data = bytearray(new_hash.digest()) + self.data[20:]
        assert len(data) == len(self.data)

    def save_finished(self, path: Path):
        this = self.encrypt()
        this.save(path)
