"""Config pytest per i test del data-layer.

Rende importabile ``src/`` senza installazione del pacchetto: la suite deve
girare su qualunque clone del repo senza dati esterni (GC-3, tasks/METODO.md:305-309).
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
