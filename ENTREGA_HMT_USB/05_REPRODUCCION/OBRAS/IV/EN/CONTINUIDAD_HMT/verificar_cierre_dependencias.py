#!/usr/bin/env python3
"""Comprueba cobertura documental, no la validez de teoremas ni del grafo.

Las rutas relativas de evidencia se resuelven respecto del JSON de entrada.
No se ejecutan fuentes, se modifican artefactos ni se certifican documentos PDF.
"""

import argparse
import hashlib
import json
from pathlib import Path

ROLES = {"definition", "operation", "result", "interpretation", "check"}
MODES = {"body", "appendix", "import", "deferred"}


def verify(data, base_dir=".", affected=None):
    """Devuelve un informe serializable; ``ok`` exige ausencia de pendientes."""
    errors, pending, impact = [], [], []
    base = Path(base_dir)

    def error(message):
        if message not in errors:
            errors.append(message)

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def records(key, optional=False):
        values = data.get(key, [] if optional else None)
        result = {}
        if not isinstance(values, list):
            error(f"{key}: se requiere una lista")
            return result
        for i, value in enumerate(values):
            if not isinstance(value, dict) or not nonempty(value.get("id")):
                error(f"{key}[{i}]: id no válido")
            elif value["id"] in result:
                error(f"{key}: id duplicado {value['id']}")
            else:
                result[value["id"]] = value
        return result

    def references(value, universe, where):
        if not isinstance(value, list):
            error(f"{where}: se requiere una lista de identificadores")
            return []
        valid = []
        for ref in value:
            if not nonempty(ref) or ref not in universe:
                error(f"{where}: referencia desconocida {ref!r}")
            elif ref in valid:
                error(f"{where}: referencia duplicada {ref}")
            else:
                valid.append(ref)
        return valid

    if not isinstance(data, dict):
        data = {}
        error("La raíz JSON debe ser un objeto")
    nodes, articles = records("nodes"), records("articles")
    if not nodes or not articles:
        error("La comprobación requiere al menos un nodo y un artículo")
    series_mode = data.get("series_autonomy_required", False)
    if type(series_mode) is not bool:
        error("series_autonomy_required debe ser booleano")
    blocks = records("shared_blocks", optional=True)
    if series_mode and not blocks:
        error("La serie autosuficiente requiere un núcleo común declarado en shared_blocks")
    shared_report = []
    for block_id, block in blocks.items():
        copies, source = block.get("copies"), block.get("source")
        if not isinstance(copies, dict) or not nonempty(source):
            error(f"{block_id}: source o copies no válido")
            continue
        try:
            origin = hashlib.sha256((base / source).read_bytes()).hexdigest()
        except (OSError, ValueError):
            error(f"{block_id}: fuente común inexistente o ilegible")
            continue
        if series_mode:
            for article_id in articles:
                if article_id not in copies:
                    error(f"{block_id}: falta copia del núcleo en {article_id}")
        for article_id, path in copies.items():
            if article_id not in articles or not nonempty(path):
                error(f"{block_id}: artículo o ruta de copia no válido")
                continue
            try:
                actual = hashlib.sha256((base / path).read_bytes()).hexdigest()
            except (OSError, ValueError):
                actual = None
            identical = actual == origin
            shared_report.append({"block": block_id, "article": article_id,
                                  "source_sha256": origin, "copy_sha256": actual,
                                  "identical": identical})
            if not identical:
                error(f"{block_id}/{article_id}: núcleo ausente o distinto de la fuente común")
    dependencies = {}
    for node_id, node in nodes.items():
        if not nonempty(node.get("title")) or not isinstance(node.get("role"), str) or node["role"] not in ROLES:
            error(f"{node_id}: título o role no válido")
        dependencies[node_id] = references(node.get("requires"), nodes, f"{node_id}.requires")

    colors, stack = {}, []

    def visit(node_id):
        if colors.get(node_id) == 1:
            cycle = stack[stack.index(node_id):] + [node_id]
            error("Ciclo de dependencia probatoria: " + " -> ".join(cycle))
            return
        if colors.get(node_id) == 2:
            return
        colors[node_id] = 1
        stack.append(node_id)
        for dep in dependencies[node_id]:
            visit(dep)
        stack.pop()
        colors[node_id] = 2

    for node_id in nodes:
        visit(node_id)

    closures, placements = {}, {}
    for article_id, article in articles.items():
        if not nonempty(article.get("title")) or type(article.get("self_contained")) is not bool:
            error(f"{article_id}: título o self_contained no válido")
        if series_mode and article.get("self_contained") is not True:
            error(f"{article_id}: la serie exige artículos autónomos y autosuficientes")
        todo = references(article.get("targets"), nodes, f"{article_id}.targets")
        closure = set()
        while todo:
            node_id = todo.pop()
            if node_id not in closure:
                closure.add(node_id)
                todo.extend(dependencies[node_id])
        closures[article_id] = closure
        places = article.get("placements")
        if not isinstance(places, dict):
            error(f"{article_id}.placements: se requiere un objeto")
            places = {}
        placements[article_id] = places
        for node_id, place in places.items():
            where = f"{article_id}/{node_id}"
            if node_id not in nodes:
                error(f"{where}: nodo desconocido")
            if not isinstance(place, dict):
                error(f"{where}: ubicación no válida")
                continue
            mode = place.get("mode")
            if not isinstance(mode, str) or mode not in MODES or not nonempty(place.get("location")):
                error(f"{where}: mode no válido o location vacía")
            if mode == "deferred" and node_id not in closure and not nonempty(place.get("reason")):
                error(f"{where}: deferred no requerido exige reason")
            if mode == "import":
                origin = place.get("from_article")
                if not isinstance(origin, str) or origin not in articles or origin == article_id:
                    error(f"{where}: origen de importación no válido")
                if article.get("self_contained"):
                    error(f"{where}: un artículo autosuficiente no admite import")

    used = set().union(*closures.values()) if closures else set()
    for node_id in sorted(used):
        source = nodes[node_id].get("source")
        if not isinstance(source, dict) or not nonempty(source.get("locator")):
            error(f"{node_id}: source.locator vacío o ausente")
        path = source.get("path") if isinstance(source, dict) else None
        if not nonempty(path):
            error(f"{node_id}: source.path vacío o ausente")
        else:
            try:
                if not (base / path).is_file():
                    error(f"{node_id}: evidencia inexistente {path}")
            except (OSError, ValueError):
                error(f"{node_id}: ruta de evidencia no válida")

    resolved, active = {}, []

    def resolve(article_id, node_id):
        key = (article_id, node_id)
        if key in resolved:
            return resolved[key]
        if key in active:
            cycle = active[active.index(key):] + [key]
            error("Ciclo de resolución/importación: " + " -> ".join(f"{a}/{n}" for a, n in cycle))
            return False
        active.append(key)
        where, valid = f"{article_id}/{node_id}", True
        place = placements[article_id].get(node_id)
        mode = place.get("mode") if isinstance(place, dict) else None
        if not isinstance(place, dict):
            error(f"{where}: dependencia requerida omitida")
            valid = False
        elif not nonempty(place.get("location")):
            valid = False
        elif isinstance(mode, str) and mode in {"body", "appendix"}:
            for dep in dependencies[node_id]:
                valid = resolve(article_id, dep) and valid
        elif place.get("mode") == "import":
            origin = place.get("from_article")
            if articles[article_id].get("self_contained") or not isinstance(origin, str) or origin not in articles or origin == article_id:
                valid = False
            else:
                valid = resolve(origin, node_id)
                if not valid:
                    error(f"{where}: el nodo no queda resuelto en {origin}")
        else:
            error(f"{where}: dependencia requerida no satisfecha ({place.get('mode')})")
            valid = False
        active.pop()
        resolved[key] = valid
        return valid

    coverage = {}
    for article_id, closure in closures.items():
        results = [resolve(article_id, node_id) for node_id in sorted(closure)]
        coverage[article_id] = {"closure": sorted(closure), "covered": all(results)}
    for change_id, change in records("changes", optional=True).items():
        changed = set(references(change.get("changed_nodes"), nodes, f"{change_id}.changed_nodes"))
        settled = set(references(change.get("resolved_articles"), articles, f"{change_id}.resolved_articles"))
        impacted = sorted(a for a, closure in closures.items() if changed & closure)
        outstanding = sorted(set(impacted) - settled)
        impact.append({"change": change_id, "affected_articles": impacted, "pending_articles": outstanding})
        pending.extend({"change": change_id, "article": a} for a in outstanding)
    affected_articles = None
    if affected is not None:
        if affected not in nodes:
            error(f"--affected: nodo desconocido {affected}")
        else:
            affected_articles = sorted(a for a, closure in closures.items() if affected in closure)
    return {"ok": not errors and not pending, "errors": errors, "pending": pending,
            "articles": coverage, "changes": impact, "affected_articles": affected_articles,
            "coverage_declared": data.get("coverage", "unspecified"),
            "shared_blocks": shared_report,
            "scope": "Cobertura documental del grafo declarado y existencia de evidencias; no prueba teoremas, contenido de localizadores ni completitud del grafo."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON de dependencias y artículos")
    parser.add_argument("--affected", metavar="NODE", help="consulta de impacto sin modificar archivos")
    args = parser.parse_args()
    try:
        with args.manifest.open(encoding="utf-8") as stream:
            data = json.load(stream)
        report = verify(data, args.manifest.resolve().parent, args.affected)
    except (OSError, ValueError, RecursionError) as exc:
        report = {"ok": False, "errors": [str(exc)], "pending": []}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
