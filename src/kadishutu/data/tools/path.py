import os
from pathlib import Path


TOOLS_DIR = Path(os.path.realpath(__file__)).parent
TABLES_PATH = TOOLS_DIR.parent / "tables"
