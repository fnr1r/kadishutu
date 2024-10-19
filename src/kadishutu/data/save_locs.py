import json
from kadishutu.data.tools.path import TABLES_PATH
from kadishutu.encodings import ENCODING
from typing import Dict

SAVE_LOCS_PATH = TABLES_PATH / "save_locs.json"
with SAVE_LOCS_PATH.open("rt", encoding=ENCODING) as file:
    SAVE_LOCS: Dict[int, str] = {
        int(k, base=16): v
        for k, v in json.load(file).items()
    }

SAVE_LOCS_REV = { v: k for k, v in SAVE_LOCS.items() }
