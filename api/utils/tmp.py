import os
from pathlib import Path


TMP_PATH = Path(os.path.dirname(os.path.realpath(__file__)))\
              / '..' / 'tmp'


if not os.path.isdir(TMP_PATH):
    os.mkdir(TMP_PATH)
