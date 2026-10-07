"""Controles finitos del arranque IV; no sustituyen las pruebas generales.

Sólo biblioteca estándar. Verifica seis copias originales, referencias locales,
identidades de dualidad en muestras racionales y minimización de clases.
No usa valores físicos objetivo ni genera una conclusión global de teoría M.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
registry = json.loads((ROOT / "REGISTRO_PROCEDENCIA.json").read_text())
source_root = Path(registry["source_root"])
checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


for source in registry["original_sources"]:
    original = (source_root / source["path"]).read_bytes()
    copy = (ROOT / source["copy"]).read_bytes()
    check("copia_" + source["id"], original == copy)
    check("hash_" + source["id"], sha256(copy).hexdigest() == source["sha256"])

texts = [(p.name, p.read_text()) for p in sorted((ROOT / "sections").glob("*.tex"))]
text = "\n".join(t for _, t in texts)
labels = re.findall(r"\\label\{([^}]+)\}", text)
refs = set(re.findall(r"\\(?:eqref|ref|cref)\{([^}]+)\}", text))
check("cuatro_cuerpos_reales", len(texts) == 4 and all(len(t.split()) > 1000 for _, t in texts))
check("etiquetas_unicas", len(labels) == len(set(labels)))
check("dependencias_externas_declaradas", refs - set(labels) == {"exc:k-direccion", "exc:leech"})
check("prefijo_local_iv", all(label.startswith("iv:") for label in labels))


def energy(m, w, r):
    return F(m * m) / (r * r) + F(w * w) * r * r


def minimum_on_line(m, w, r, v):
    a, b = v
    leading = F(a * a) / (r * r) + F(b * b) * r * r
    linear_half = F(a * m) / (r * r) + F(b * w) * r * r
    optimum = -linear_half / leading
    k = optimum.numerator // optimum.denominator
    return min(energy(m + j * a, w + j * b, r) for j in (k, k + 1))


radii = [F(1, 3), F(1, 2), F(1), F(2), F(3)]
pairs = [(m, w) for m in range(-15, 16, 3) for w in range(-15, 16, 3)]
check("dualidad_racional", all(energy(m, w, r) == energy(w, m, 1 / r) for r in radii for m, w in pairs))
check("involucion_radio", all(1 / (1 / r) == r for r in radii))
check("obstruccion_secciones", energy(9, 0, F(1)) != energy(0, 1, F(1)))
check("energia_clase_secciones", all(minimum_on_line(9, 0, r, (9, -1)) == minimum_on_line(0, 1, r, (9, -1)) for r in radii))
check("dualidad_clases", all(minimum_on_line(m, w, r, (9, -1)) == minimum_on_line(w, m, 1 / r, (-1, 9)) for r in radii for m, w in pairs))
check("invariancia_representante", all(minimum_on_line(m, w, r, (9, -1)) == minimum_on_line(m + 9, w - 1, r, (9, -1)) for r in radii for m, w in pairs))
check("minimo_dos_candidatos", all(minimum_on_line(m, w, r, (9, -1)) == min(energy(m + 9 * k, w - k, r) for k in range(-100, 101)) for r in radii for m, w in pairs))
check("hamming_radio_dos", 1 + 2 * 11 + 4 * (11 * 10 // 2) == 243)
check("particion_codigo", 3 ** 6 * 243 == 3 ** 11)
check("rangos_nonadicos", all(0 <= ((9 ** (d + 1) * a) // b) - 9 * ((9 ** d * a) // b) <= 8 for d in range(1, 7) for b in range(1, 31) for a in range(b + 1)))


def path_count(path, initial):
    direction, kind = initial
    a = b = 0
    for d, t in path:
        a += d != direction
        b += t != kind
        direction, kind = d, t
    return a, b


first = [("E", "+"), ("N", "+"), ("N", "x")]
second = [("S", "x"), ("E", "+")]
initial = ("E", "+")
total = path_count(first + second, initial)
a, b = path_count(first, initial), path_count(second, first[-1])
check("cociclo_frontera", total == (a[0] + b[0], a[1] + b[1]))
check("sin_cociclo_oculto", path_count([("E", "+"), ("N", "+")], ("E", "+"))[0] == 1)

print(json.dumps({
    "status": "PASS_CONTROLES_FOCALES_IV",
    "checks": checks,
    "count": len(checks),
    "rational_samples": len(radii) * len(pairs),
    "source_copies": len(registry["original_sources"]),
    "local_labels": len(labels),
    "scope": "Copias, referencias y controles finitos; no prueba general automatizada ni clausura física de teoría M"
}, ensure_ascii=False, indent=2))
