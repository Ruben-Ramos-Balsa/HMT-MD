#!/usr/bin/env python3
"""Recalcula las incidencias publicadas desde las cien fronteras regionales."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--csv", required=True)
p.add_argument("--source", required=True)
p.add_argument("--receipt", required=True)
a = p.parse_args()
csv_path, source = Path(a.csv), Path(a.source)
rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
text = source.read_text(encoding="utf-8")
matrix = ((0,1,1,1,1,1),(1,0,1,1,2,2),(1,1,0,2,1,2),
          (1,1,2,0,2,1),(1,2,1,2,0,1),(1,2,2,1,1,0))
blocks = ("020022","222111","211201","021101","002001","020111",
          "200110","121012","010122","001001","221110","222110")

def require(test, message):
    if not test:
        raise RuntimeError(message)

def word(bands, coefficients):
    return "".join(str(sum(coefficients[i] * bands[i][j] for i in range(3)) % 3)
                   for j in range(6))

require(len(rows) == 100, "Se requieren las cien fronteras declaradas")
hits, all_output = [], set()
for row in rows:
    t = int(row["t"])
    bands = tuple(tuple(map(int, b)) for b in row["B"].split("|"))
    charges = {
        "r": tuple(sum(b) % 3 for b in bands),
        "d": tuple(sum(sum(b[i] * matrix[i][j] for i in range(6)) % 3
                       for j in range(6)) % 3 for b in bands),
    }
    require("".join(map(str, charges["r"])) == row["r"].zfill(3), "Carga visible")
    require("".join(map(str, charges["d"])) == row["dual"].zfill(3), "Carga dual")
    phase = (t - 1) % 3
    for charge_name, charge in charges.items():
        for delta in range(3):
            for epsilon in (-1, 1):
                co = tuple((epsilon if c == (phase + delta) % 3 else -epsilon) % 3
                           for c in charge)
                output = word(bands, co)
                all_output.add(output)
                if output in blocks:
                    hits.append((blocks.index(output)+1,t,charge_name,delta,epsilon,
                                 "".join(map(str,co)),output))
row30 = next(r for r in rows if int(r["t"]) == 30)
affine = word(tuple(tuple(map(int,b)) for b in row30["B"].split("|")), (2,0,1))
require(affine == "001001", "Incidencia afin t30")
require("001001" not in all_output, "Alcance del lector comparativo")
pattern = r"(?m)^([0-9]+)&([0-9]+)&\$([rd])\$&([0-2])&\s*(?:\$(-1)\$|(1))&([0-2]{3})&([0-2]{6})\\\\$"
printed = []
for m in re.finditer(pattern, text):
    j,t,c,delta,neg,pos,co,out = m.groups()
    printed.append((int(j),int(t),c,int(delta),int(neg or pos),co,out))
require(len(printed) == 19, "La tabla LaTeX debe contener 19 incidencias")
require(set(printed) == set(hits), "Diferencia entre calculo y tabla impresa")
position_outputs = {j: {h[-1] for h in hits if h[0] == j} for j in range(5,13)}
position_outputs[10].add(affine)
require(all(len(v) == 1 for v in position_outputs.values()), "Singleton por posicion")
recovered = tuple(next(iter(position_outputs[j])) for j in range(5,13))
require(recovered == blocks[4:], "Recuperacion exacta por posiciones")
receipt = {
    "status": "PASS_PRINTED_TERMINAL_INCIDENCE_TABLE",
    "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "boundaries": 100, "comparative_evaluations": 1200,
    "printed_incidences": 19, "affine_witness": {"time":30,"coefficients":[2,0,1],"output":affine},
    "recovered_positions": {str(j):next(iter(v)) for j,v in position_outputs.items()},
    "unordered_repertoire": sorted(int(w,3) for w in recovered),
    "scope": "Recuperacion desde incidencias con posiciones declaradas; seleccion del orden por el consumidor posterior.",
    "lean_recompiled": False,
}
Path(a.receipt).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(receipt["status"])
