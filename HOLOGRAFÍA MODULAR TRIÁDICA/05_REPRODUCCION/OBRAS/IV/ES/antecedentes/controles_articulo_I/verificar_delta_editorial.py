#!/usr/bin/env python3
"""Control material del delta editorial, con biblioteca estándar.

No compila TeX, no modifica fuentes y no certifica un cierre matemático.
Recorre inclusiones literales desde main.tex; no es un intérprete de TeX.
Ejemplo:
  python3 -I -S technical/verificar_delta_editorial.py \
    --base /ruta/ARTICULO_REVISION_LECTOR_FRONTERA_20260909 \
    --root /ruta/ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909 \
    --receipt /ruta/technical/DELTA_EDITORIAL_VERIFICADO.json

Las autorizaciones se enumeran por etiqueta y bloque, nunca mediante una
sustitución global de J o s. Las ecuaciones repetidas pueden condensarse:
se exige una residencia activa de su contenido, no la misma multiplicidad.
Los cinco bloques de incidencia y el bloque H5 reciben además comparación
textual completa. Las restantes diferencias narrativas sólo se inventarían.
"""

import argparse
from collections import Counter, defaultdict
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys


LABEL = re.compile(r"\\label\s*\{([^{}]+)\}")
INCLUDE = re.compile(
    r"\\(?P<cmd>input|include|includegraphics)\*?"
    r"\s*(?:\[[^\]]*\]\s*)?\{(?P<arg>[^{}]+)\}"
)
DISPLAY = re.compile(
    r"\\\[(?P<bracket>.*?)\\\]"
    r"|\\begin\{(?P<env>equation\*?|align\*?|gather\*?|multline\*?"
    r"|flalign\*?|alignat\*?|eqnarray\*?|displaymath)\}"
    r"(?P<body>.*?)\\end\{(?P=env)\}"
    r"|\$\$(?P<dollar>.*?)\$\$",
    re.S,
)
TOKEN = re.compile(r"\\[A-Za-z]+|\\.|[0-9]+(?:\.[0-9]+)?|[^\s]")
LAYOUT = re.compile(r"\\(?:begin|end)\{(?:aligned|alignedat|split|gathered)\}")
SOURCE_SUFFIXES = {".tex", ".sty", ".cls", ".bib"}
EXCLUDED_PARTS = {"output", "qa", ".git", "__pycache__"}
INCIDENCE = (
    ("inc-ampl-articulacion", "incidencia_registro.tex"),
    ("inc-ampl-clausura", "incidencia_normalizacion.tex"),
    ("inc-ampl-bandera", "incidencia_bandera.tex"),
    ("inc-ampl-reticulo", "incidencia_reticulo.tex"),
    ("inc-ampl-automorfismos", "incidencia_automorfismos.tex"),
)
AUTHORIZATIONS = [
    {"id": "swap_operator", "scope": "eq:el-bisagra",
     "rule": r"J(x,y) y J involutivo -> \mathscr S_{\pi\varphi}; no afecta J matricial"},
    {"id": "alpha_signed_balance", "scope": "eq:alpha-recurrencia",
     "rule": r"Z_j:=P_j+E_j-\Phi_j-K_j; s_j=Z_j+c_{j+1}; expansión exacta"},
    {"id": "incidence_signed_balance", "scope": "inc-ampl-normalizacion y bloque inc-ampl-clausura",
     "rule": r"s_j previo -> Z_j; s_0 -> Z_0; suma entrante s_j=Z_j+c_{j+1} explícita"},
    {"id": "initial_signed_vector", "scope": "sections/excepcional.tex",
     "rule": "s_0 -> Z_0; sólo vector de balance inicial y diagrama que lo reutiliza"},
    {"id": "incidence_relocation", "scope": [x[0] for x in INCIDENCE],
     "rule": "Cinco párrafos completos trasladados a inclusiones activas propias"},
    {"id": "h5_relocation", "scope": "sec:revision-planck",
     "rule": "Bloque completo anterior a Continuación regional trasladado a electron.tex"},
    {"id": "narrative_condensation", "scope": "narrativa general y ecuaciones repetidas",
     "rule": "No se exige identidad integral de prosa; ecuaciones originales conservadas en una residencia activa"},
    {"id": "repeated_support_formula", "scope": "revision_incidencia_argumento.tex -> exc:bk",
     "rule": "B_K={j:K_j>=729}={4,6,9,10}: renombrado ligado j -> i y reiteración contenida en la igualdad de exc:bk con intersección adicional; plantilla exacta"},
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def without_comments(text):
    """Preserva saltos de línea/localizadores; reconoce porcentajes escapados."""
    lines = []
    for line in text.splitlines(keepends=True):
        end = len(line)
        for i, char in enumerate(line):
            if char != "%":
                continue
            k = i - 1
            while k >= 0 and line[k] == "\\":
                k -= 1
            if (i - 1 - k) % 2 == 0:
                end = i
                break
        lines.append(line[:end] + ("\n" if end < len(line) and line.endswith("\n") else ""))
    return "".join(lines)


def compact(text):
    return re.sub(r"\s+", "", without_comments(text))


def location(path, text, offset):
    return {"path": path, "line": text.count("\n", 0, offset) + 1}


class Document:
    def __init__(self, root):
        self.root = root
        self.raw = {}
        self.text = {}
        self.active = []
        self.errors = []
        self.figures = []
        self.labels = defaultdict(list)
        self.equations = []
        self.read(Path("main.tex"), ())
        for path in self.active:
            text = self.text[path]
            for match in LABEL.finditer(text):
                self.labels[match[1]].append(location(path, text, match.start()))
            for match in DISPLAY.finditer(text):
                body = next(match[g] for g in ("bracket", "body", "dollar") if match[g] is not None)
                self.equations.append({
                    **location(path, text, match.start()),
                    "labels": LABEL.findall(body), "body": body,
                    "environment": match["env"] or ("display" if match["bracket"] is not None else "$$"),
                })

    def load(self, relative):
        name = relative.as_posix()
        if name not in self.raw:
            data = (self.root / relative).read_bytes()
            self.raw[name] = data
            self.text[name] = without_comments(data.decode("utf-8"))
        return self.text[name]

    def resolve(self, parent, arg, graphics=False):
        suffixes = ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg") if graphics else ("", ".tex")
        for folder in (Path("."), parent):
            for suffix in suffixes:
                candidate = (self.root / folder / (arg + suffix)).resolve()
                if candidate.is_file():
                    try:
                        return candidate.relative_to(self.root)
                    except ValueError:
                        self.errors.append({"kind": "external_dependency", "path": str(candidate)})
                        return None
        self.errors.append({"kind": "unresolved_inclusion", "source_directory": str(parent), "argument": arg})
        return None

    def read(self, relative, stack):
        name = relative.as_posix()
        if name in stack:
            self.errors.append({"kind": "inclusion_cycle", "chain": list(stack) + [name]})
            return
        if not (self.root / relative).is_file():
            self.errors.append({"kind": "missing_source", "path": name})
            return
        text = self.load(relative)
        self.active.append(name)
        for match in INCLUDE.finditer(text):
            arg, cmd = match["arg"], match["cmd"]
            if "\\" in arg or "#" in arg:
                self.errors.append({**location(name, text, match.start()),
                                    "kind": "dynamic_inclusion_not_supported", "argument": arg})
                continue
            target = self.resolve(relative.parent, arg, cmd == "includegraphics")
            if target is None:
                continue
            if cmd == "includegraphics" or "figures" in target.parts:
                self.figures.append({
                    **location(name, text, match.start()), "target": target.as_posix(),
                    "command": compact(match[0]), "sha256": sha((self.root / target).read_bytes()),
                })
            if cmd != "includegraphics":
                self.read(target, stack + (name,))


def normalize_math(body, path="", labels=()):
    """Normaliza maquetación; conserva signos, números, orden y celdas matriciales."""
    text = LABEL.sub("", without_comments(body))
    if "eq:el-bisagra" in labels:
        text = re.sub(r"\\mathscr\s*S_\{\\pi\\varphi\}", " SWAP ", text)
        text = re.sub(r"(?<![A-Za-z\\])J(?![A-Za-z])", " SWAP ", text)
    if "eq:alpha-recurrencia" in labels:
        text = text.replace("Z_j", r"P_j+E_j-\Phi_j-K_j")
    if "inc-ampl-normalizacion" in labels:
        # La suma entrante nueva se conserva explícitamente en la comprobación
        # textual del bloque. Aquí se compara su expansión con la fórmula previa.
        if "Z_j" in text:
            text = re.sub(r"A_j\s*=\s*s_j\s*-\s*1000c_j\s*=", "A_j=", text)
        else:
            text = text.replace("s_j", "Z_j")
    if path == "sections/excepcional.tex":
        text = text.replace("s_0", "Z_0")
    text = LAYOUT.sub("", text)
    text = re.sub(r"\\(?:quad|qquad|enspace|thinspace|medspace|thickspace)\b|\\[,;!:]", "", text)
    text = re.sub(r"\\(?:left|right)\b", "", text)
    # Sólo separadores de alineación exteriores. Dentro de matrices/casos
    # permanecen tanto & como \\; no se aplana el contenido matricial.
    bits, depth, cursor = [], 0, 0
    structural = re.compile(r"\\(?P<edge>begin|end)\{(?P<env>[^{}]+)\}|\\\\(?:\[[^\]]*\])?|&")
    for match in structural.finditer(text):
        bits.append(text[cursor:match.start()])
        if match["edge"]:
            if match["edge"] == "begin":
                depth += 1
            bits.append(match[0])
            if match["edge"] == "end":
                depth -= 1
        elif depth:
            bits.append(match[0])
        cursor = match.end()
    bits.append(text[cursor:])
    text = "".join(bits)
    text = re.sub(r"([\^_])\s*\{\s*([A-Za-z0-9])\s*\}", r"\1\2", text)
    return tuple(TOKEN.findall(text))


def brief(tokens):
    return " ".join(tokens)


def source_inventory(root):
    result = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_file() and not EXCLUDED_PARTS.intersection(rel.parts):
            if path.suffix.lower() in SOURCE_SUFFIXES or rel.parts[0] == "figures":
                result[rel.as_posix()] = sha(path.read_bytes())
    return result


def extract_paragraphs(text):
    starts = list(re.finditer(r"\\paragraph\{", text))
    result = {}
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[match.start():end]
        labels = LABEL.findall(block)
        if labels:
            result[labels[0]] = (block, text.count("\n", 0, match.start()) + 1)
    return result


def expected_incidence(block, label):
    """Reescritura autorizada explícita, sin aceptar otra alteración del bloque."""
    if label == "inc-ampl-clausura":
        old = r"$s_j=P_j+E_j-\Phi_j-K_j^{\mathrm{per}}$. La normalización"
        new = (r"$Z_j=P_j+E_j-\Phi_j-K_j^{\mathrm{per}}$ y el balance con cociente entrante "
               r"es $s_j=Z_j+c_{j+1}$. La normalización")
        block = re.sub(re.escape(old).replace(r"\ ", r"\s+"), lambda _: new, block)
        block = block.replace("A_j=s_j+c_{j+1}-1000c_j",
                              "A_j=s_j-1000c_j=Z_j+c_{j+1}-1000c_j")
    return block.replace("s_0", "Z_0")


def mismatch(expected, actual):
    a, b = compact(expected), compact(actual)
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [{"operation": tag, "expected": a[max(0, i-60):min(len(a), j+60)],
             "actual": b[max(0, k-60):min(len(b), l+60)]}
            for tag, i, j, k, l in matcher.get_opcodes() if tag != "equal"][:12]


def self_check():
    assert normalize_math("a&=b", labels=()) == normalize_math("a=b")
    assert normalize_math("a=b+2") != normalize_math("a=b+3")
    assert normalize_math(r"\begin{pmatrix}1&2\\3&4\end{pmatrix}") != normalize_math(
        r"\begin{pmatrix}1&2&3\\4\end{pmatrix}")
    assert normalize_math("J^2=I", labels=("eq:el-bisagra",)) == normalize_math(
        r"\mathscr S_{\pi\varphi}^{\,2}&=I", labels=("eq:el-bisagra",))
    assert normalize_math(r"\mathcal R\circ J", labels=("eq:el-bisagra",)) == normalize_math(
        r"\mathcal R\circ\mathscr S_{\pi\varphi}", labels=("eq:el-bisagra",))
    assert normalize_math("J^2=-I") != normalize_math(r"\mathscr S_{\pi\varphi}^2=-I")
    assert normalize_math(r"s_j=P_j+E_j-\Phi_j-K_j+c_{j+1}", labels=("eq:alpha-recurrencia",)) == normalize_math(
        r"s_j=Z_j+c_{j+1}", labels=("eq:alpha-recurrencia",))


def check(base, root):
    self_check()
    before, after = Document(base), Document(root)
    inv0, inv1 = source_inventory(base), source_inventory(root)
    failures = []
    failures.extend({"check": "base_inclusion_graph", **x} for x in before.errors)
    failures.extend({"check": "root_inclusion_graph", **x} for x in after.errors)
    removed = sorted(set(inv0) - set(inv1))
    changed = [p for p in inv0 if p in inv1 and inv0[p] != inv1[p]]
    failures.extend({"check": "source_inventory", "kind": "removed", "path": p} for p in removed)
    figure_changes = [p for p in changed if p.startswith("figures/")]
    failures.extend({"check": "figure_bytes", "kind": "changed", "path": p,
                     "base_sha256": inv0[p], "root_sha256": inv1[p]} for p in figure_changes)
    fig0, fig1 = Counter(x["command"] for x in before.figures), Counter(x["command"] for x in after.figures)
    for cmd, count in (fig0 - fig1).items():
        failures.append({"check": "figure_inclusions", "command": cmd, "missing_occurrences": count,
                         "base_locations": [x for x in before.figures if x["command"] == cmd]})
    missing_labels = sorted(set(before.labels) - set(after.labels))
    failures.extend({"check": "labels", "kind": "missing", "label": label,
                     "base_locations": before.labels[label]} for label in missing_labels)
    duplicates = {key: value for key, value in after.labels.items() if len(value) > 1}
    failures.extend({"check": "labels", "kind": "duplicate_active_label", "label": label,
                     "locations": locs} for label, locs in duplicates.items())

    new_by_tokens, new_by_label = defaultdict(list), defaultdict(list)
    for equation in after.equations:
        tokens = normalize_math(equation["body"], equation["path"], equation["labels"])
        new_by_tokens[tokens].append(equation)
        for label in equation["labels"]:
            new_by_label[label].append(equation)
    equation_matches = []
    for equation in before.equations:
        tokens = normalize_math(equation["body"], equation["path"], equation["labels"])
        mode = "same_display_content_after_declared_notation"
        if equation["labels"]:
            candidates = [x for x in new_by_label[equation["labels"][0]]
                          if normalize_math(x["body"], x["path"], x["labels"]) == tokens]
        else:
            candidates = new_by_tokens[tokens]
        # Una reiteración concreta del preámbulo se retiró al condensarlo.
        # Se comprueban ambos lados completos de la transformación autorizada:
        # no se aplica equivalencia alfa de índices ni inclusión de subcadenas
        # indiscriminadamente a las demás ecuaciones.
        old_support = normalize_math(r"B_K=\{j:K_j\geq729\}=\{4,6,9,10\}.")
        new_support = normalize_math(r"B_K=\{i:K_i\geq729\}=\{4,6,9,10\}=H_e\cap P_\pi.")
        if not candidates and equation["path"] == "sections/revision_incidencia_argumento.tex" and tokens == old_support:
            candidates = [x for x in new_by_label["exc:bk"]
                          if normalize_math(x["body"], x["path"], x["labels"]) == new_support]
            mode = "declared_reiteration_in_exc_bk_with_bound_index_renaming"
        entry = {k: equation[k] for k in ("path", "line", "labels", "environment")}
        if candidates:
            entry["matches"] = [{k: x[k] for k in ("path", "line", "labels")} for x in candidates]
            entry["normalized_sha256"] = sha(brief(tokens).encode())
            entry["preservation_mode"] = mode
        else:
            actual = new_by_label[equation["labels"][0]] if equation["labels"] else []
            entry.update(check="equations", kind="content_not_preserved", expected=brief(tokens),
                         actual=[{**{k: x[k] for k in ("path", "line")},
                                  "content": brief(normalize_math(x["body"], x["path"], x["labels"]))}
                                 for x in actual])
            failures.append(entry.copy())
        equation_matches.append(entry)
    # La abreviación mediante Z es válida sólo si su definición está presente.
    alpha_definition = any(compact(x["body"]) in {
        r"Z_j:=P_j+E_j-\Phi_j-K_j", r"Z_j:=P_j+E_j-\Phi_j-K_j."
    } for x in after.equations if x["path"] == "sections/alpha.tex")
    if not alpha_definition:
        failures.append({"check": "authorized_notation", "kind": "missing_exact_Z_definition",
                         "path": "sections/alpha.tex"})

    blocks = []
    source = "sections/incidencia_articulacion.tex"
    original_blocks = extract_paragraphs(before.load(Path(source)))
    for label, filename in INCIDENCE:
        dest = "sections/" + filename
        original, line = original_blocks.get(label, ("", 0))
        actual = after.load(Path(dest)) if (root / dest).is_file() else ""
        expected = expected_incidence(original, label)
        ok = bool(original) and compact(expected) == compact(actual) and dest in after.active
        item = {"id": label, "source": {"path": source, "line": line},
                "target": {"path": dest, "line": 1}, "active": dest in after.active,
                "preserved_after_declared_notation": ok,
                "expected_sha256": sha(compact(expected).encode()),
                "actual_sha256": sha(compact(actual).encode())}
        if not ok:
            item["differences"] = mismatch(expected, actual)
            failures.append({"check": "incidence_blocks", **item})
        blocks.append(item)

    before.load(Path("sections/revision_planck.tex"))
    planck = before.raw["sections/revision_planck.tex"].decode("utf-8")
    marker = r"\subsubsection{Continuación regional y ecuación de renovación}"
    old_h5, separator, suffix = planck.partition(marker)
    after.load(Path("sections/electron.tex"))
    electron = after.raw["sections/electron.tex"].decode("utf-8")
    h5_start = electron.find(r"\subsubsection{Carácter de acción y procedencia de sus coeficientes}")
    h5_end = electron.find("Sobre esta base, el carácter de quinto orden", h5_start)
    new_h5 = electron[h5_start:h5_end] if h5_start >= 0 and h5_end >= h5_start else ""
    h5_ok = bool(separator) and old_h5 == new_h5 and "sections/electron.tex" in after.active
    after.load(Path("sections/revision_planck.tex"))
    suffix_ok = after.raw["sections/revision_planck.tex"].decode("utf-8") == marker + suffix
    h5 = {"source": {"path": "sections/revision_planck.tex", "line": 1},
          "target": location("sections/electron.tex", electron, max(0, h5_start)),
          "byte_identical_block": h5_ok, "remaining_suffix_identical": suffix_ok}
    if not h5_ok or not suffix_ok:
        failures.append({"check": "h5_relocation", **h5, "differences": mismatch(old_h5, new_h5)})
    # Impide dar por vigente un recibo obtenido mientras el editor cambiaba entradas.
    concurrent = []
    for doc, title in ((before, "base"), (after, "root")):
        for path, data in doc.raw.items():
            if (doc.root / path).read_bytes() != data:
                concurrent.append({"tree": title, "path": path})
    failures.extend({"check": "snapshot_consistency", **x} for x in concurrent)
    counts0 = Counter(normalize_math(x["body"], x["path"], x["labels"]) for x in before.equations)
    counts1 = Counter(normalize_math(x["body"], x["path"], x["labels"]) for x in after.equations)
    condensed = [{"normalized_sha256": sha(brief(tokens).encode()),
                  "base_occurrences": count, "root_occurrences": counts1[tokens],
                  "retained_locations": [{k: x[k] for k in ("path", "line", "labels")}
                                         for x in new_by_tokens[tokens]]}
                 for tokens, count in counts0.items() if 0 < counts1[tokens] < count]
    return {
        "schema": "hmt.local-editorial-delta.v1",
        "status": "VERIFIED_LOCAL_EDITORIAL_PRESERVATION" if not failures else "DIFFERENCES_REQUIRING_REVIEW",
        "scope": "Preservación material focal; no cierre matemático, no compilación, no QA visual.",
        "base": str(base), "root": str(root),
        "authorizations": AUTHORIZATIONS,
        "summary": {
            "source_and_figure_files_base": len(inv0),
            "source_and_figure_files_root": len(inv1),
            "removed_files": len(removed),
            "base_figure_files": sum(p.startswith("figures/") for p in inv0),
            "changed_figure_files": len(figure_changes),
            "active_figure_inclusions_base": len(before.figures),
            "active_figure_inclusions_root": len(after.figures),
            "active_labels_base": len(before.labels), "active_labels_root": len(after.labels),
            "display_equations_base": len(before.equations),
            "display_equations_root": len(after.equations),
            "display_equations_preserved": sum("matches" in x for x in equation_matches),
            "incidence_blocks_preserved": sum(x["preserved_after_declared_notation"] for x in blocks),
            "h5_block_preserved": h5_ok, "h5_suffix_preserved": suffix_ok,
            "failures": len(failures),
        },
        "inventories": {"base": inv0, "root": inv1},
        "active_sources": {"base": before.active, "root": after.active},
        "changed_source_files": [p for p in changed if not p.startswith("figures/")],
        "new_files": sorted(set(inv1) - set(inv0)),
        "new_labels": sorted(set(after.labels) - set(before.labels)),
        "figure_inclusions": {"base": before.figures, "root": after.figures},
        "equation_matches": equation_matches,
        "condensed_repeated_equations": condensed,
        "incidence_blocks": blocks, "h5_relocation": h5,
        "failures": failures,
        "limitations": [
            "Análisis estático de inclusiones literales; no expande macros, condicionales ni código TeX.",
            "Ecuaciones: entornos display, equation, align, gather, multline, flalign, alignat, eqnarray y variantes; no todo fragmento inline narrativo.",
            "Las repeticiones de una ecuación sin etiqueta pueden reunirse en una residencia activa idéntica.",
            "Normalización de maquetación no es simplificación algebraica; sólo reescrituras autorizadas enumeradas.",
            "Fuera de los cinco bloques y H5 no se exige identidad integral de narrativa ni se acredita su equivalencia semántica.",
            "Una huella o este resultado no acredita autosuficiencia matemática ni presencia visual en un PDF.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    base, root = args.base.resolve(), args.root.resolve()
    if base == root:
        parser.error("--base y --root deben ser árboles distintos")
    try:
        result = check(base, root)
    except (OSError, UnicodeError, AssertionError) as exc:
        result = {"schema": "hmt.local-editorial-delta.v1", "status": "CHECK_ERROR",
                  "base": str(base), "root": str(root),
                  "scope": "Error del control estático, sin veredicto matemático.",
                  "failures": [{"kind": type(exc).__name__, "message": str(exc)}]}
    result["verifier_sha256"] = sha(Path(__file__).read_bytes())
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    print(json.dumps(result.get("summary", {}), ensure_ascii=False, indent=2))
    for item in result["failures"]:
        print(json.dumps(item, ensure_ascii=False))
    print("Recibo:", args.receipt.resolve())
    return 0 if not result["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
