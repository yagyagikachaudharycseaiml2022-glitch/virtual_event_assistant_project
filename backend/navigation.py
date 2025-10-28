from typing import Dict, List, Optional
import heapq

def build_graph(nodes: List[dict], edges: List[dict]) -> Dict[str, Dict[str, float]]:
    graph = {n['id']: {} for n in nodes}
    for e in edges:
        a, b = e['from'], e['to']
        d = float(e.get('distance_m', 1.0))
        graph.setdefault(a, {})[b] = d
        graph.setdefault(b, {})[a] = d
    return graph

def dijkstra(graph: Dict[str, Dict[str, float]], start: str, goal: str) -> Optional[dict]:
    if start not in graph or goal not in graph:
        return None
    pq = [(0.0, start, [])]
    visited = set()
    while pq:
        dist, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return {"distance_m": dist, "path": path}
        for nb, w in graph.get(node, {}).items():
            if nb not in visited:
                heapq.heappush(pq, (dist + w, nb, path))
    return None
