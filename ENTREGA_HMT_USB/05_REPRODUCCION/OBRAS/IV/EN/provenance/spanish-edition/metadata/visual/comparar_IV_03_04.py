#!/usr/bin/env python3
"""Read-only IV 03-to-04 comparison; writes only a new QA record."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import pdfplumber

ROOT = Path("/Users/ruben/Documents/ChatGPT/jueces y controles/EDICION_PUBLICACION_IV_V_20260914")
HELPER = ROOT / "gestion/visual_V/comparar_cortes_02_03.py"
spec = importlib.util.spec_from_file_location("qa_previous_helper", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
paths = [
    ROOT / "IV_MOONSHINE_DUALIDAD_TEORIA_M/fuentes/output/edicion_publicacion_03/MOONSHINE_DUALIDAD_T_Y_TEORIA_M.pdf",
    ROOT / "IV_MOONSHINE_DUALIDAD_TEORIA_M/fuentes/output/edicion_publicacion_04/MOONSHINE_DUALIDAD_T_Y_TEORIA_M.pdf",
]
expected = [
    "c4ce2a25893533c4e28f8cb2647b4bd4f04a82e727febd6b73f0949430072356",
    "82393a736fd59293713edea96bd11ced426fc2e795193cd3bd5d0635318013e2",
]
out = ROOT / "gestion/visual_IV/COMPARACION_IV_03_04.json"
if out.exists():
    raise SystemExit("Refusing to overwrite the comparison.")
records, bibliographies = [], []
for path, digest in zip(paths, expected):
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("PDF identity mismatch: " + str(path))
    pages, bibliography = [], []
    with pdfplumber.open(path) as pdf:
        for n, page in enumerate(pdf.pages, 1):
            pages.append(helper.signature(page, n))
            if n >= 150:
                bibliography.append("".join(c["text"] for c in page.chars
                    if 60 < c["top"] < page.height - 50))
            page.close()
    records.append(pages)
    bibliographies.append("".join(bibliography))
old, new = records
if (len(old), len(new)) != (151, 150):
    raise ValueError("Unexpected page counts.")
mapping = []
for n in range(1, 150):
    a, b = old[n-1], new[n-1]
    mapping.append({"old_page": n, "new_page": n,
        "same_text": a["text"] == b["text"],
        "same_glyphs_and_geometry": a["glyphs"] == b["glyphs"],
        "same_page_size": a["size"] == b["size"]})
same = lambda r: r["same_text"] and r["same_glyphs_and_geometry"] and r["same_page_size"]
norm = lambda s: re.sub(r"\s+", "", s)
result = {
    "scope": "Read-only text and glyph-geometry comparison; visual inspection recorded separately.",
    "pdfs": [{"path": str(p), "sha256": h} for p,h in zip(paths, expected)],
    "page_counts": [151,150],
    "coordinate_rounding_decimals": 5,
    "helper": str(HELPER),
    "footer_exclusion": "Only validated central page-number glyphs, as in helper.signature.",
    "mapped_pages": mapping,
    "unchanged_new_pages": [r["new_page"] for r in mapping if same(r)],
    "different_new_pages": [r["new_page"] for r in mapping if not same(r)],
    "merged_bibliography": {
        "old_pages": [150,151], "new_pages": [150],
        "same_character_stream_ignoring_whitespace": norm(bibliographies[0]) == norm(bibliographies[1]),
        "labels_old": re.findall(r"\[(\d+)\]", bibliographies[0]),
        "labels_new": re.findall(r"\[(\d+)\]", bibliographies[1]),
        "header_footer_excluded": "Keep glyphs with 60 < top < height-50 for this comparison only.",
    },
    "new_pages_requiring_visual_by_change": sorted(set([r["new_page"] for r in mapping if not same(r)] + [150])),
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k:result[k] for k in ("page_counts","different_new_pages","merged_bibliography","new_pages_requiring_visual_by_change")}, ensure_ascii=False))
