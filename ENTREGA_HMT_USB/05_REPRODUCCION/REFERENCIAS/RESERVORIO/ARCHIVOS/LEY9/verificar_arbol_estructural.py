"""Valida enlaces y coherencia del árbol documental; no certifica teoremas HMT."""
import argparse
import hashlib
import json
from pathlib import Path

def validate_graph(graph):
    nodes = graph["nodes"]
    ids = [node["id"] for node in nodes]
    if len(set(ids)) != len(ids):
        raise ValueError("Identificadores de nodos repetidos")
    id_set = set(ids)
    sources = graph["sources"]
    adjacency = {node_id: [] for node_id in ids}
    indegree = {node_id: 0 for node_id in ids}
    for item in [*nodes, *graph["edges"]]:
        if not item.get("source_refs"):
            raise ValueError("Objeto sin fuentes")
        if any(ref not in sources for ref in item["source_refs"]):
            raise ValueError("Referencia de fuente desconocida")
    for edge in graph["edges"]:
        if edge["from"] not in id_set or edge["to"] not in id_set:
            raise ValueError("Arista con extremo desconocido")
        if edge["type"] != "compatibilidad_por_verificar":
            adjacency[edge["from"]].append(edge["to"])
            indegree[edge["to"]] += 1
    ready = sorted(k for k, degree in indegree.items() if degree == 0)
    order = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for target in adjacency[current]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    if len(order) != len(ids):
        raise ValueError("Ciclo en las dependencias de esta vista expositiva")
    if graph["scientific_proof_certificate"] or graph["all_edges_end_to_end_executed"]:
        raise ValueError("Este comprobador documental no puede certificar pruebas")
    continuum = next(node for node in nodes if node["id"] == "CONTINUUM")
    if continuum["atomic_inseparable_aspects"] != ["sp", "sol", "gau", "coh", "det"]:
        raise ValueError("Se ha alterado el nodo conjunto del continuo")
    for recovery in graph.get("sector_recovery", []):
        if recovery["node"] not in id_set:
            raise ValueError("Reconstrucción sectorial con nodo desconocido")
        if not all(key in recovery for key in ("domain", "codomain", "forward", "inverse")):
            raise ValueError("Ficha sectorial incompleta")
        if not recovery.get("source_refs") or any(ref not in sources for ref in recovery["source_refs"]):
            raise ValueError("Reconstrucción sectorial sin fuente válida")
    return order

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=Path(__file__).with_name("ARBOL_ESTRUCTURAL_NUCLEO.json"))
    parser.add_argument("--package-root", type=Path)
    args = parser.parse_args()
    raw = args.graph.read_bytes()
    graph = json.loads(raw)
    order = validate_graph(graph)
    root = (args.package_root or Path(graph["package_root"])).resolve()
    source_checks = {}
    for source_id, source in graph["sources"].items():
        relative = Path(source["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("La fuente debe ser relativa al paquete")
        path = root / relative
        if not path.resolve().is_relative_to(root):
            raise ValueError("Fuente enlazada fuera del paquete")
        data = path.read_bytes()
        lines = data.decode("utf-8").splitlines()
        if not 1 <= source["line"] <= len(lines):
            raise ValueError("Localizador fuera de la fuente: " + source_id)
        source_checks[source_id] = {
            "path": source["path"], "line": source["line"],
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()
        }
    broken = json.loads(raw)
    broken["edges"][0]["to"] = "EXTREMO_INEXISTENTE"
    try:
        validate_graph(broken)
    except ValueError:
        negative_control = True
    else:
        raise ValueError("No se detectó el control negativo")
    result = {
        "status": "VALIDACION_DOCUMENTAL_CORRECTA",
        "scientific_proof_certificate": False,
        "meaning": "Valida sintaxis, extremos, fuentes locales y orden documental; no ejecuta ni demuestra las derivaciones.",
        "graph_sha256": hashlib.sha256(raw).hexdigest(),
        "nodes": len(graph["nodes"]), "relations": len(graph["edges"]),
        "sector_recovery_records": len(graph.get("sector_recovery", [])),
        "sources": source_checks,
        "expository_order": order,
        "negative_control_unknown_endpoint_rejected": negative_control,
        "originals_modified": False,
        "new_decimal_campaign": False
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
