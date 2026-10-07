#!/usr/bin/env python3
"""Article IV reproduction entry point for this English edition.

For the current command-line options run: python3 reproducir.py --help.
The historical program is preserved under provenance/spanish-edition/.
"""
from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    if not any(a == "--articulo" or a.startswith("--articulo=") for a in sys.argv[1:]):
        sys.argv[1:1] = ["--articulo", "IV"]
    runpy.run_path(str(Path(__file__).resolve().with_name("reproducir_publicacion.py")),
                  run_name="__main__")
