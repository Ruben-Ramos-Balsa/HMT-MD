"""Controles finitos del arranque IV; no sustituyen las pruebas generales.

Sólo biblioteca estándar. Verifica las seis copias contra hashes explícitos,
las cuatro secciones propias, identidades de dualidad en muestras racionales y
minimización de clases. Coteja los originales sólo cuando están disponibles;
su ausencia no se presenta como un cotejo satisfactorio.
No usa valores físicos objetivo ni genera una conclusión global de teoría M.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import re
import runpy

ROOT = Path(__file__).resolve().parent
ARTICLE_ROOT = ROOT.parent
FOCAL_SECTIONS = (
    "01_hilbert_nonadico.tex",
    "02_dualidad_t.tex",
    "03_pantallas_coordinadas.tex",
    "04_accion_realizacion.tex",
)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--receipt", type=Path, help="Guardar además el recibo JSON en esta ruta")
parser.add_argument("--source-root", type=Path, help="Raíz alternativa de originales; no altera el registro")
args = parser.parse_args()
registry_path = ROOT / "REGISTRO_PROCEDENCIA.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
source_root_value = args.source_root or registry.get("source_root")
source_root = Path(source_root_value).expanduser().resolve() if source_root_value else None
checks = []
failures = []
source_results = []
section_results = []


def check(name, condition):
    checks.append(name)
    if not condition:
        failures.append(name)


sources = registry["original_sources"]
check("seis_propietarios_declarados", len(sources) == 6)
check("identificadores_propietarios_unicos", len({s["id"] for s in sources}) == len(sources))
for source in sources:
    copy_path = ROOT / source["copy"]
    expected = source["sha256"]
    check("hash_explicito_" + source["id"], bool(re.fullmatch(r"[0-9a-f]{64}", expected)))
    copy = copy_path.read_bytes() if copy_path.is_file() else None
    copy_hash = sha256(copy).hexdigest() if copy is not None else None
    check("copia_disponible_" + source["id"], copy is not None)
    check("hash_copia_" + source["id"], copy_hash == expected)
    original_path = source_root / source["path"] if source_root else None
    row = {
        "id": source["id"],
        "copy": str(copy_path.relative_to(ARTICLE_ROOT)),
        "expected_sha256": expected,
        "copy_sha256": copy_hash,
        "copy_matches_expected": copy_hash == expected,
        "original_path": str(original_path) if original_path else None,
        "original_compared": False,
        "original_sha256": None,
        "original_matches_copy": None,
    }
    if original_path is not None and original_path.is_file():
        original = original_path.read_bytes()
        original_hash = sha256(original).hexdigest()
        check("hash_original_" + source["id"], original_hash == expected)
        check("cotejo_original_" + source["id"], original == copy)
        row.update({
            "original_status": "COMPARADO",
            "original_compared": True,
            "original_sha256": original_hash,
            "original_matches_copy": original == copy,
        })
    else:
        row["original_status"] = "NO_DISPONIBLE" if original_path else "RAIZ_NO_DECLARADA"
    source_results.append(row)

texts = []
for name in FOCAL_SECTIONS:
    section_path = ARTICLE_ROOT / "sections" / name
    data = section_path.read_bytes() if section_path.is_file() else None
    check("seccion_disponible_" + name, data is not None)
    content = data.decode("utf-8") if data is not None else ""
    texts.append((name, content))
    section_results.append({
        "path": str(section_path.relative_to(ARTICLE_ROOT)),
        "sha256": sha256(data).hexdigest() if data is not None else None,
        "words": len(content.split()),
    })
text = "\n".join(t for _, t in texts)
helpers = runpy.run_path(str(ROOT / 'compilar_iv.py'), run_name='iv_focal_source_helpers')
graph = helpers['source_graph']()
check('grafo_activo_local_resuelto', not graph['errors'])
combined = '\n'.join(helpers['strip_comments']((ARTICLE_ROOT / row['path']).read_text()) for row in graph['tex'])
labels = re.findall(r"\\label\s*\{([^}]+)\}", combined)
refs = set()
for item in re.findall(r"\\(?:eqref|ref|cref|Cref)\s*\{([^}]+)\}", combined):
    refs.update(part.strip() for part in item.split(','))
check("cuatro_cuerpos_reales", len(texts) == 4 and all(t.strip() and r'\begin{proof}' in t for _, t in texts))
check("etiquetas_unicas_ensamblado", len(labels) == len(set(labels)))
check("remisiones_ensamblado_resueltas", not (refs - set(labels)))
historical = {'eq:dualidad-normalizada-k': 'iv:eq:energia-t',
              'prop:dualidad-radios-k': 'iv:thm:t-unitaria',
              'eq:dualidad-cociente-k': 'iv:eq:energia-cociente',
              'eq:k-mapa-pantallas': 'iv:eq:rm-alg',
              'thm:k-pantallas-coordinadas': 'iv:thm:pantallas-isomorfas'}
focal_labels = re.findall(r"\\label\s*\{([^}]+)\}", text)
check("prefijo_local_o_etiqueta_trasladada", all(label.startswith('iv:') or label in historical for label in focal_labels))
check('destinos_etiquetas_historicas', all(target in labels for target in historical.values()))


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

original_count = sum(row["original_compared"] for row in source_results)
result = {
    "schema": "HMT_CONTROLES_FOCALES_IV_V2",
    "status": "FAIL_CONTROLES_FOCALES_IV" if failures else "PASS_CONTROLES_FOCALES_IV",
    "checks": checks,
    "count": len(checks),
    "passed_count": len(checks) - len(failures),
    "failures": failures,
    "rational_samples": len(radii) * len(pairs),
    "source_copies": len(source_results),
    "source_copies_verified": sum(row["copy_matches_expected"] for row in source_results),
    "source_originals_compared": original_count,
    "source_originals_unavailable": len(source_results) - original_count,
    "source_verification_mode": (
        "HASHES_Y_ORIGINALES" if original_count == len(source_results)
        else "HASHES_Y_COTEJO_PARCIAL" if original_count else "SOLO_HASHES_DECLARADOS"
    ),
    "source_root": str(source_root) if source_root else None,
    "source_root_origin": "CLI_OVERRIDE" if args.source_root else "REGISTRO",
    "source_details": source_results,
    "registry_sha256": sha256(registry_path.read_bytes()).hexdigest(),
    "verifier_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    "active_sections": section_results,
    "local_labels": len(labels),
    "unresolved_active_labels": sorted(refs - set(labels)),
    "historical_label_destinations": historical,
    "active_graph_sha256": graph['active_graph_sha256'],
    "active_sources": graph['tex'],
    "scope": "Cuatro secciones propias con residencia probatoria, seis copias con hashes, remisiones del ensamblado activo y controles finitos. Las extensiones y fusiones conservan etiquetas o destinos explícitos. No es una verificación matemática global ni una clausura física de teoría M.",
}
serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
if args.receipt:
    args.receipt.write_text(serialized, encoding="utf-8")
print(serialized, end="")
raise SystemExit(1 if failures else 0)
