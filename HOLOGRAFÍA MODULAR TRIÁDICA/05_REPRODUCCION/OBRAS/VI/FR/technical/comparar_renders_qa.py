#!/usr/bin/env python3
"""Comparación material de PNG de páginas, sin modificar ninguno de los PDF."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("previous", type=Path)
p.add_argument("current", type=Path)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
old = {p.name: p for p in a.previous.glob("page-*.png")}
new = {p.name: p for p in a.current.glob("page-*.png")}
report = {
    "scope": "IMAGE_PIXEL_COMPARISON_NOT_SCIENTIFIC_CERTIFICATION",
    "previous": str(a.previous.resolve()),
    "current": str(a.current.resolve()),
    "previous_pages": len(old),
    "current_pages": len(new),
    "missing_from_current": sorted(set(old) - set(new)),
    "new_pages": sorted(set(new) - set(old)),
    "identical": [],
    "changed": [],
}
for name in sorted(set(old) & set(new)):
    first, second = Image.open(old[name]).convert("RGB"), Image.open(new[name]).convert("RGB")
    ordinal = int(name.split("-")[-1].split(".")[0])
    if first.size != second.size:
        report["changed"].append({"page": ordinal, "size_before": first.size, "size_after": second.size})
        continue
    bbox = ImageChops.difference(first, second).getbbox()
    if bbox:
        report["changed"].append({"page": ordinal, "difference_bbox": bbox})
    else:
        report["identical"].append(ordinal)
a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"identical": len(report["identical"]), "changed": len(report["changed"]), "report": str(a.output)}, ensure_ascii=False))
