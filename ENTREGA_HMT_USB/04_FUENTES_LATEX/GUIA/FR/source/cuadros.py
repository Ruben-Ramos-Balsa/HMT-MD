"""Active table authority: translated, reviewed JSON. Historical generators remain in the immutable predecessor."""
from pathlib import Path
import json
TABLES=json.loads((Path(__file__).resolve().parent/"tablas_editoriales.json").read_text())["tables"]
