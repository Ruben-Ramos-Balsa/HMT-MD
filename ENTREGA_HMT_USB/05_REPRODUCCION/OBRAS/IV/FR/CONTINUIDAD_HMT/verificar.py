#!/usr/bin/env python3
"""Contrato portátil de lectura y reproducción; no es un demostrador matemático.

Conserva archivos y dependencias declaradas, admite prueba textual, programa o
construcción conjunta. No impone 108 filas ni prohíbe símbolos por su nombre.
No ejecuta código del paquete salvo petición explícita con run --execute.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

SCHEMA = "HMT_EXPORT_CONTINUITY_V1"
PROTOCOL = "CONTINUIDAD_HMT"
GUIDE = "LEER_PRIMERO_CONTINUIDAD_HMT.md"
ROOT_GUIDE = "LEER_PRIMERO_HMT.md"
FOUNDATIONS = ("APP", "TRIT", "TPK", "estado_enriquecido", "continuo_conjunto")
KINDS = {"active", "historical", "comparison", "test", "documentation"}
PHASES = {"construction", "proof_tool", "recognition", "comparison", "check"}
INPUT_ROLES = {"primitive", "internal_output", "proof_tool", "external_target"}
STATUSES = {"established", "candidate", "pending", "rejected"}
IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache"}
SCOPE = ("Integridad, portabilidad y cobertura de las dependencias DECLARADAS. "
         "No demuestra teoremas, no descubre todas las dependencias ocultas y "
         "no fuerza la interpretación de una IA externa.")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Clave JSON duplicada: " + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique)


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local(root, name):
    require(isinstance(name, str) and bool(name), "Ruta relativa vacía")
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in name
            and p.as_posix() == name and ":" not in name,
            "Ruta no portátil: " + name)
    base = Path(root).resolve()
    path = base
    for part in p.parts:
        path = path / part
        require(not path.is_symlink(), "Enlace simbólico: " + name)
    require(path.resolve().is_relative_to(base), "Ruta fuera del paquete: " + name)
    return path


def inventory(root):
    root = Path(root)
    managed = (root / PROTOCOL / "PLAN.json").is_file() and (root / PROTOCOL / "MANIFEST.json").is_file()
    if not managed:
        reserved = [p for p in root.rglob("*") if
                    not IGNORED_DIRS.intersection(p.relative_to(root).parts)
                    and (p.relative_to(root).parts[0] == PROTOCOL or p.name in {GUIDE, ROOT_GUIDE})]
        require(not reserved, "Colisión con nombres del contrato: conservar esos originales como antecedentes "
                "antes de preparar la copia; no se omiten ni sobrescriben: " + str(reserved[:3]))
    result = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if IGNORED_DIRS.intersection(rel.parts) or rel.parts[0] == PROTOCOL:
            continue
        if p.name in {GUIDE, ROOT_GUIDE} or p.suffix == ".pyc":
            continue
        require(not p.is_symlink(), "Enlace simbólico en la fuente: " + rel.as_posix())
        if p.is_file():
            result.append({"path": rel.as_posix(), "sha256": sha(p), "bytes": p.stat().st_size})
    return result


def closure_checker():
    source = Path(__file__).with_name("verificar_cierre_dependencias.py")
    spec = importlib.util.spec_from_file_location("hmt_dependency_closure", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def validate(plan, root):
    """No ejecuta programas ni interpreta la verdad de las pruebas citadas."""
    root = Path(root).resolve()
    require(isinstance(plan, dict) and plan.get("schema") == SCHEMA, "Esquema de continuidad no válido")
    require(plan.get("delivery") in {"publication", "work"}, "Declarar delivery: publication o work")
    require(isinstance(plan.get("package_id"), str) and plan["package_id"].strip(), "package_id ausente")
    require(isinstance(plan.get("scope"), str) and plan["scope"].strip(), "Alcance del paquete ausente")
    graph = plan.get("dependency_map")
    require(isinstance(graph, dict), "Falta dependency_map; recuperar el mapa existente, no inferirlo de nombres")
    # Comprobación portátil antes de llamar al control de cobertura compartido.
    for node in graph.get("nodes", []):
        local(root, node.get("source", {}).get("path"))
    for block in graph.get("shared_blocks", []):
        local(root, block.get("source"))
        for path in block.get("copies", {}).values():
            local(root, path)
    base = closure_checker()(graph, root)
    require(not base["errors"], "Cobertura documental: " + "; ".join(base["errors"]))
    nodes = {n["id"]: n for n in graph["nodes"]}
    order, ancestors = [], {}

    def visit(key):
        if key in ancestors:
            return ancestors[key]
        parents = set()
        for dep in nodes[key]["requires"]:
            parents |= visit(dep) | {dep}
        ancestors[key] = parents
        order.append(key)
        return parents
    for key in nodes:
        visit(key)
    for key, node in nodes.items():
        require(node.get("phase") in PHASES, key + ": phase no válida")
        require(node.get("method") in {"textual", "program", "joint"}, key + ": método no declarado")
        require(node.get("status") in STATUSES, key + ": estatuto no declarado")
        for field in ("domain", "codomain", "operation"):
            require(isinstance(node.get(field), str) and node[field].strip(), key + ": falta " + field)
        require(isinstance(node.get("preserves"), list), key + ": declarar información conservada")
        outputs = node.get("outputs")
        require(isinstance(outputs, list) and outputs and all(isinstance(x, str) and x for x in outputs)
                and len(set(outputs)) == len(outputs), key + ": salidas no declaradas o duplicadas")
        inputs = node.get("inputs")
        require(isinstance(inputs, list), key + ": inputs debe ser lista, incluso vacía")
        for inp in inputs:
            role, producer = inp.get("causal_role"), inp.get("from")
            require(role in INPUT_ROLES, key + ": rol de entrada no válido")
            require(producer in ancestors[key], key + ": entrada sin antecedente declarado: " + str(producer))
            require(inp.get("output") in nodes[producer]["outputs"], key + ": salida del antecedente no localizada")
            if role == "internal_output":
                require(nodes[producer]["phase"] == "construction", key + ": origen no interno")
            if role == "proof_tool":
                require(nodes[producer]["phase"] == "proof_tool", key + ": herramienta no tipada")
            if role == "external_target":
                require(node["phase"] in {"comparison", "recognition", "check"},
                        key + ": valor objetivo usado en la construcción")
        if node["phase"] == "construction":
            bad = [x for x in ancestors[key] if nodes[x]["phase"] in {"recognition", "comparison", "check"}]
            require(not bad, key + ": reconocimiento/comparación retroalimenta la construcción: " + str(bad))
        # Una construcción conjunta es un nodo con evidencia propia, no un ciclo
        # de justificación. Sus iteraciones internas permanecen en la prueba fuente.
        if node["method"] == "joint":
            require(isinstance(node.get("joint_contract"), str) and node["joint_contract"].strip(),
                    key + ": declarar existencia, determinación y compatibilidades en joint_contract")
        run = node.get("run")
        if run is not None:
            require(isinstance(run, dict) and run.get("runtime") in {"python", "lean"}, key + ": runtime no válido")
            require(local(root, run.get("script")).is_file(), key + ": programa no incluido")
            require(isinstance(run.get("args", []), list) and
                    all(isinstance(x, str) for x in run.get("args", [])), key + ": args no válido")
            require(isinstance(run.get("timeout_seconds", 300), int) and
                    1 <= run.get("timeout_seconds", 300) <= 3600, key + ": timeout no válido")

    foundations = plan.get("foundations", {})
    require(isinstance(foundations, dict) and set(foundations) == set(FOUNDATIONS), "Falta la residencia del núcleo común")
    previous = None
    for name in FOUNDATIONS:
        key = foundations[name]
        require(key in nodes and nodes[key]["phase"] == "construction", "Fundamento sin residencia: " + name)
        require(previous is None or previous == key or previous in ancestors[key],
                "Orden de fundamentos sin enlace: " + name)
        previous = key
    used = set().union(*(set(a["closure"]) for a in base["articles"].values()))
    require(set(foundations.values()) <= used, "Núcleo presente pero ajeno a los resultados anunciados")
    for article in graph["articles"]:
        for key in article["targets"]:
            cut = nodes[key].get("lineage_cut", "continuo_conjunto")
            require(cut in foundations, key + ": punto de corte genealógico no válido")
            require(foundations[cut] in ancestors[key] | {key}, key + ": resultado sin antecedente HMT declarado")
    pending = [x for x in order if x in used and nodes[x]["status"] != "established"]
    pending += ["cambio:" + x["change"] + "/" + x["article"] for x in base["pending"]]
    if plan["delivery"] == "publication":
        require(not pending, "Integración documental pendiente en: " + ", ".join(pending)
                + ". No es un dictamen de falsedad matemática; conservar como work o completar su incorporación.")

    rows = plan.get("files")
    require(isinstance(rows, list), "Falta inventario de archivos")
    indexed = {}
    for row in rows:
        path = row.get("path")
        require(path not in indexed, "Archivo duplicado: " + str(path))
        p = local(root, path)
        require(p.is_file() and sha(p) == row.get("sha256"), "Archivo ausente o modificado: " + path)
        require(row.get("role") in KINDS, "Rol documental ausente: " + path)
        refs = row.get("nodes", [])
        require(isinstance(refs, list) and all(x in nodes for x in refs), "Nodos de archivo inválidos: " + path)
        require(bool(refs) or bool(row.get("reason")), "Archivo sin función declarada: " + path)
        indexed[path] = row
    actual = {r["path"] for r in inventory(root)}
    excluded = plan.get("excluded_files", [])
    require(isinstance(excluded, list), "excluded_files debe ser una lista")
    exclusions = set()
    for row in excluded:
        path = row.get("path")
        local(root, path)
        require(path not in exclusions and row.get("reason"), "Exclusión duplicada o sin motivo")
        exclusions.add(path)
    require(not (set(indexed) & exclusions), "Un archivo está incluido y excluido a la vez")
    require(actual == set(indexed) | exclusions, "Inventario incompleto o desfasado: "
            + str(sorted(actual ^ (set(indexed) | exclusions))))
    for key, node in nodes.items():
        paths = [node["source"]["path"]]
        if node.get("run"):
            paths.append(node["run"]["script"])
        for path in paths:
            require(path in indexed and key in indexed[path].get("nodes", []),
                    key + ": fuente/programa sin vínculo en inventario: " + path)
    for block in graph.get("shared_blocks", []):
        for path in [block["source"], *block["copies"].values()]:
            require(path in indexed, "Fuente común excluida del paquete: " + path)
    return {"ok": True, "status": "PASS_CONTINUIDAD_DOCUMENTAL_EXPORTACION",
            "scope": SCOPE, "package_id": plan["package_id"], "delivery": plan["delivery"],
            "order": order, "pending": pending, "files": len(rows),
            "execution_order": [x for x in order if x in used],
            "mathematical_truth_certified": False, "programs_executed": False}


def guide(plan, report):
    lines = ["# Lectura y reproducción consecuentes del paquete HMT", "",
             "Empiece aquí, aunque el paquete se entregue sin los otros artículos.", "",
             "APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo.", "",
             "Una salida interna construida puede alimentar la etapa posterior. Conserve su procedencia;",
             "no la trate como valor convencional inyectado. Tampoco use el valor buscado para seleccionarse a sí mismo.",
             "La construcción puede ser conjunta o coinductiva: el orden siguiente es de dependencias,",
             "no una exigencia de una única implementación, 108 filas o cálculo simultáneo.", "",
             "## Alcance de esta entrega", "", plan["scope"], "",
             "Modo: `" + plan["delivery"] + "`. " + SCOPE, "",
             "## Orden de lectura y ejecución", ""]
    nodes = {n["id"]: n for n in plan["dependency_map"]["nodes"]}
    for pos, key in enumerate(report["order"], 1):
        n = nodes[key]
        source = n["source"]
        lines += [f"{pos}. **{n['title']}** (`{key}`; {n['method']}; {n['status']}).",
                  f"   Fuente: [{source['path']}]({source['path']}), {source['locator']}.",
                  "   Antecedentes: " + (", ".join(n["requires"]) or "primitivas declaradas") + ".",
                  "   Operación: " + n["operation"], "   Salidas: " + ", ".join(n["outputs"]) + ".", ""]
    lines += ["## Comandos", "", "Desde la carpeta que contiene este archivo:", "", "```text",
              "python3 -I -S CONTINUIDAD_HMT/verificar.py verify --root .",
              "python3 -I -S CONTINUIDAD_HMT/verificar.py show --root .", "```", "",
              "Tras revisar los programas, puede ejecutar en una copia temporal la secuencia declarada:", "", "```text",
              "python3 -I -S CONTINUIDAD_HMT/verificar.py run --root . --execute", "```", "",
              "Las pruebas textuales no se fuerzan a convertirse en Python. Lean sólo se declara ejecutado",
              "cuando se ha lanzado el comprobador correspondiente. Se registran errores y salidas por paso;",
              "no se reutiliza un recibo cuya fuente cambió ni se llama cierre a un candidato.", "",
              "Un error de integridad, localización o cobertura describe este paquete. No demuestra que",
              "el resultado no exista en el corpus. Busque primero el propietario y la composición conservada.", "",
              "No promueva el PASS de exportación a aprobación matemática. El grafo requiere contraste semántico.", ""]
    if report["pending"]:
        lines += ["Pendientes documentales declarados: " + ", ".join(report["pending"]), ""]
    return "\n".join(lines)


def prepare_copy(root, plan, destination):
    """Copia sucesora; nunca escribe en root ni sobrescribe destination."""
    root, destination = Path(root).resolve(), Path(destination)
    require(not destination.resolve().is_relative_to(root), "La copia sucesora debe quedar fuera de la fuente")
    if (root / PROTOCOL).exists():
        check_export(root)
    report = validate(plan, root)
    require(not destination.exists(), "El destino existe; no se sobrescribe")
    destination.mkdir(parents=True)
    for row in plan["files"]:
        src, dst = local(root, row["path"]), destination / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        require(sha(dst) == row["sha256"] == sha(src), "Cambio durante la copia: " + row["path"])
    # Detectar también altas/bajas y cambios de archivos ya copiados, no sólo
    # la huella del archivo que se acaba de copiar.
    validate(plan, root)
    portable = json.loads(json.dumps(plan))
    portable["excluded_files"] = []  # Los excluidos no residen en la copia.
    protocol = destination / PROTOCOL
    protocol.mkdir()
    save(protocol / "PLAN.json", portable)
    shutil.copy2(__file__, protocol / "verificar.py")
    shutil.copy2(Path(__file__).with_name("verificar_cierre_dependencias.py"), protocol / "verificar_cierre_dependencias.py")
    (destination / ROOT_GUIDE).write_text(guide(portable, report), encoding="utf-8")
    dirs = {Path(r["path"]).parent for r in plan["files"]
            if Path(r["path"]).suffix.lower() in {".py", ".lean", ".json", ".tex"}}
    for directory in dirs:
        if directory == Path("."):
            continue
        relative = os.path.relpath(destination / ROOT_GUIDE, destination / directory)
        (destination / directory / GUIDE).write_text(
            "# Continuidad del paquete\n\nAntes de interpretar estos archivos, lea [el orden común]("
            + relative + ").\n\nEl inventario `CONTINUIDAD_HMT/PLAN.json` vincula cada archivo con sus "
            "operaciones, antecedentes y salidas. No se cambia su rol causal por leerlo aisladamente.\n",
            encoding="utf-8")
    control_files = [p for p in destination.rglob("*") if p.is_file()]
    save(protocol / "MANIFEST.json", {"schema": SCHEMA, "scope": SCOPE,
         "files": [{"path": p.relative_to(destination).as_posix(), "sha256": sha(p)} for p in sorted(control_files)]})
    check_export(destination)
    return report


def check_export(root):
    """API de empaquetadores: exige contrato material, no crea o altera fuentes."""
    root = Path(root).resolve()
    protocol = root / PROTOCOL
    for name in ("PLAN.json", "verificar.py", "verificar_cierre_dependencias.py", "MANIFEST.json"):
        require((protocol / name).is_file(), "Paquete sin continuidad portable: " + PROTOCOL + "/" + name)
    require((root / ROOT_GUIDE).is_file(), "Falta " + ROOT_GUIDE)
    manifest = load(protocol / "MANIFEST.json")
    require(manifest.get("schema") == SCHEMA, "Manifiesto de continuidad inválido")
    seen = set()
    for row in manifest.get("files", []):
        path = row["path"]
        require(path not in seen, "Manifest duplicado: " + path)
        seen.add(path)
        require(sha(local(root, path)) == row["sha256"], "Huella de entrega distinta: " + path)
    required = {ROOT_GUIDE, PROTOCOL + "/PLAN.json", PROTOCOL + "/verificar.py",
                PROTOCOL + "/verificar_cierre_dependencias.py"}
    require(required <= seen, "El manifiesto no cubre el contrato portátil")
    plan = load(protocol / "PLAN.json")
    report = validate(plan, root)
    require({row["path"] for row in plan["files"]} <= seen, "Archivos sin huella de entrega")
    # Las guías son parte de la entrega, aunque no sean fuentes matemáticas.
    for p in root.rglob(GUIDE):
        require(p.relative_to(root).as_posix() in seen, "Guía sin huella")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
              and not IGNORED_DIRS.intersection(p.relative_to(root).parts) and p.suffix != ".pyc"}
    require(actual == seen | {PROTOCOL + "/MANIFEST.json"},
            "Archivos fuera del manifiesto de entrega: " + str(sorted(actual ^ (seen | {PROTOCOL + "/MANIFEST.json"}))))
    return report


def export_zip(root, plan, archive):
    archive = Path(archive).resolve()
    require(archive.suffix == ".zip" and not archive.exists(), "ZIP existente o nombre no válido")
    require(not archive.is_relative_to(Path(root).resolve()), "El ZIP sucesor debe quedar fuera de la fuente")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hmt_exportacion_") as tmp:
        folder = Path(tmp) / "paquete"
        report = prepare_copy(root, plan, folder)
        candidate = Path(tmp) / "entrega.zip"
        with zipfile.ZipFile(candidate, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(folder.rglob("*")):
                if p.is_file():
                    zf.write(p, "paquete/" + p.relative_to(folder).as_posix())
        with zipfile.ZipFile(candidate) as zf:
            require(zf.testzip() is None, "Error CRC del ZIP")
            zf.extractall(Path(tmp) / "extraido")  # Miembros creados arriba, sólo relativos seguros.
        extracted = Path(tmp) / "extraido/paquete"
        check_export(extracted)
        r = subprocess.run([sys.executable, "-I", "-S", str(extracted / PROTOCOL / "verificar.py"),
                            "verify", "--root", str(extracted)], capture_output=True, text=True)
        require(r.returncode == 0, "Verificador portátil: " + r.stdout + r.stderr)
        validate(plan, root)
        with archive.open("xb") as target, candidate.open("rb") as source:
            shutil.copyfileobj(source, target)
    return {**report, "archive": str(archive), "sha256": sha(archive), "temporary_extraction_verified": True}


def run_sequence(root, execute=False):
    report = check_export(root)
    require(execute, "Revise los scripts; para ejecutarlos use --execute")
    plan = load(Path(root) / PROTOCOL / "PLAN.json")
    nodes = {n["id"]: n for n in plan["dependency_map"]["nodes"]}
    steps = []
    with tempfile.TemporaryDirectory(prefix="hmt_reproduccion_") as tmp:
        cwd = Path(tmp).resolve() / "paquete"
        shutil.copytree(root, cwd)
        for key in report["execution_order"]:
            node, outcome = nodes[key], {"id": key, "executed": False}
            run = node.get("run")
            if run is not None:
                runtime = sys.executable if run["runtime"] == "python" else shutil.which("lean")
                require(runtime, "Lean no instalado; no se marca su prueba como ejecutada")
                # No imponer -I/-S a productores que importan módulos hermanos o
                # bibliotecas declaradas; el ejecutor de infraestructura sí es aislable.
                flags = ["-B"] if run["runtime"] == "python" else []
                cmd = [runtime, *flags, str(local(cwd, run["script"])), *run.get("args", [])]
                try:
                    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True,
                                       timeout=run.get("timeout_seconds", 300))
                    outcome.update(executed=True, returncode=r.returncode,
                                   stdout=r.stdout, stderr=r.stderr)
                except subprocess.TimeoutExpired:
                    outcome.update(executed=True, returncode=124, stderr="Tiempo de ejecución agotado")
                steps.append(outcome)
                if outcome["returncode"]:
                    return {**report, "ok": False, "status": "ERROR_EJECUCION_LOCAL",
                            "programs_executed": True, "steps": steps}
            else:
                outcome["reason"] = "Prueba/lectura textual; no exige un programa equivalente"
                steps.append(outcome)
    return {**report, "status": "SECUENCIA_DECLARADA_EJECUTADA", "steps": steps,
            "programs_executed": any(s["executed"] for s in steps)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("inventory", "verify", "show", "run", "prepare", "export"))
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--plan", type=Path)
    p.add_argument("--destination", type=Path)
    p.add_argument("--zip", type=Path)
    p.add_argument("--execute", action="store_true")
    args = p.parse_args()
    try:
        if args.command == "inventory":
            result = {"files": inventory(args.root), "scope": "Inventario sin roles causales inferidos"}
        elif args.command == "verify":
            result = validate(load(args.plan), args.root) if args.plan else check_export(args.root)
        elif args.command == "show":
            result = check_export(args.root)
            print(guide(load(args.root / PROTOCOL / "PLAN.json"), result))
            return 0
        elif args.command == "run":
            result = run_sequence(args.root, args.execute)
        else:
            require(args.plan is not None, "Se requiere --plan")
            if args.command == "prepare":
                require(args.destination is not None, "Se requiere --destination")
                result = prepare_copy(args.root, load(args.plan), args.destination)
            else:
                require(args.zip is not None, "Se requiere --zip")
                result = export_zip(args.root, load(args.plan), args.zip)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok", True) else 1
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({"ok": False, "status": "ERROR_CONTRATO_DOCUMENTAL",
                          "error": str(exc), "scope": SCOPE}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
