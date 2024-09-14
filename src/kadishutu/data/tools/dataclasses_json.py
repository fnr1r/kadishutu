from dataclasses_json import config
from marshmallow.fields import String


def hex_int_decode(txt: str) -> int:
    return int(txt, 16)


def hex_int_encoder(t: int, padding: int = 0) -> str:
    #return f"0x{t:08x}"
    unpadded_hex = hex(t)[2:]
    return "0x" + unpadded_hex.rjust(padding, "0")


def hex_int_config(padding: int = 0):
    return config(
        decoder=hex_int_decode,
        encoder=lambda x: hex_int_encoder(x, padding)
    )


def bytes_config(size: int, *args, **kwargs):
    strlen = size * 2
    return config(
        mm_field=String(*args, **kwargs),
        decoder=bytes.fromhex,
        encoder=lambda t: t.hex().rjust(strlen, "0")
    )
