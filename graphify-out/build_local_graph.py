import json
import re
from pathlib import Path

from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.detect import detect
from graphify.export import to_graphml, to_html, to_json, to_svg
from graphify.extract import collect_files, extract
from graphify.report import generate
from graphify.wiki import to_wiki


ROOT = Path(".")
OUT = Path("graphify-out")
EXCLUDED_PREFIXES = ("graphify-out/", "frontend/coverage/")
_write_text = Path.write_text


def write_text_utf8(self, data, encoding=None, errors=None, newline=None):
    return _write_text(self, data, encoding=encoding or "utf-8", errors=errors, newline=newline)


Path.write_text = write_text_utf8


def community_labels(graph, communities):
    labels = {}
    for cid, nodes in communities.items():
        raw = ", ".join(graph.nodes[n].get("label", n) for n in nodes[:3])
        clean = re.sub(r"[^A-Za-z0-9_, .-]+", "", raw).strip(" ,.-")
        labels[cid] = f"Community {cid}: {clean[:80]}" if clean else f"Community {cid}"
    return labels


def is_excluded(path_name):
    normalized = path_name.replace("\\", "/").lower()
    return normalized.startswith(EXCLUDED_PREFIXES)


def filter_detection(detection):
    files = detection.get("files", {})
    filtered = {}
    for kind, file_names in files.items():
        filtered[kind] = [name for name in file_names if not is_excluded(name)]
    detection["files"] = filtered
    detection["total_files"] = sum(len(names) for names in filtered.values())
    detection["total_words"] = estimate_words(filtered)
    return detection


def estimate_words(files):
    total = 0
    for kind in ("code", "document", "paper"):
        for file_name in files.get(kind, []):
            path = Path(file_name)
            if path.is_file():
                try:
                    total += len(re.findall(r"\w+", path.read_text(encoding="utf-8", errors="ignore")))
                except OSError:
                    pass
    return total


def main():
    OUT.mkdir(exist_ok=True)

    detection = filter_detection(detect(ROOT))
    (OUT / ".graphify_detect.json").write_text(json.dumps(detection, indent=2), encoding="utf-8")

    code_files = []
    for file_name in detection.get("files", {}).get("code", []):
        path = Path(file_name)
        code_files.extend(collect_files(path, root=ROOT) if path.is_dir() else [path])

    ast = extract(code_files, cache_root=ROOT) if code_files else {
        "nodes": [],
        "edges": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }
    ast.setdefault("hyperedges", [])
    (OUT / ".graphify_ast.json").write_text(json.dumps(ast, indent=2), encoding="utf-8")
    (OUT / ".graphify_extract.json").write_text(json.dumps(ast, indent=2), encoding="utf-8")

    graph = build_from_json(ast)
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    labels = community_labels(graph, communities)
    gods = god_nodes(graph)
    surprises = surprising_connections(graph, communities)
    questions = suggest_questions(graph, communities, labels)

    analysis = {
        "communities": {str(k): v for k, v in communities.items()},
        "cohesion": {str(k): v for k, v in cohesion.items()},
        "community_labels": {str(k): v for k, v in labels.items()},
        "gods": gods,
        "surprises": surprises,
        "suggested_questions": questions,
    }
    (OUT / ".graphify_analysis.json").write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    token_cost = {
        "input": ast.get("input_tokens", 0),
        "output": ast.get("output_tokens", 0),
    }
    report = generate(
        graph,
        communities,
        cohesion,
        labels,
        gods,
        surprises,
        detection,
        token_cost,
        str(ROOT),
        questions,
    )
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")

    to_json(graph, communities, str(OUT / "graph.json"))
    to_html(graph, communities, str(OUT / "graph.html"), labels)
    to_svg(graph, communities, str(OUT / "graph.svg"), labels)
    to_graphml(graph, communities, str(OUT / "graph.graphml"))
    to_wiki(graph, communities, OUT / "wiki", labels, cohesion, gods)

    print(f"Corpus: {detection.get('total_files', 0)} files, ~{detection.get('total_words', 0)} words")
    print(f"Skipped sensitive: {len(detection.get('skipped_sensitive', []))}")
    print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"Communities: {len(communities)}")
    print("Wrote: graphify-out/graph.html, graph.json, GRAPH_REPORT.md, graph.svg, graph.graphml, wiki/")


if __name__ == "__main__":
    main()
