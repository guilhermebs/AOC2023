from collections import defaultdict
from copy import deepcopy
import os
import random
import time


def solve():
    input_file_contents = open(os.path.join("input", "day25")).read().rstrip()
    
    graph = defaultdict(set)
    for line in input_file_contents.splitlines():
        from_, to_ = line.split(": ")
        to_ = to_.split(" ")
        graph[from_] |= set(to_)
        for t in to_:
            graph[t].add(from_)

    while True:
        edges_cut, g1, g2 = karger(deepcopy(graph))
        if len(edges_cut) == 3:
            sol_part1 = len(g1) * len(g2)
            break
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def contract(graph, node1, node2):
    new_node = f"{node1},{node2}"
    removed = set([node1, node2])
    for n in graph:
        if len(removed.intersection(graph[n])) > 0:
            graph[n] -= removed
            if n not in removed:
                graph[n].add(new_node)
    graph[new_node] = graph[node1] | graph[node2]
    graph[new_node]
    del graph[node1]
    del graph[node2]


def karger(graph):
    original_graph = graph
    graph = deepcopy(graph)
    while len(graph) > 2:
        edges = list((n1, n2) for n1 in graph for n2 in graph[n1])
        contract(graph, *random.choice(edges))
    g1, g2 = list(graph.keys())
    g1 = set(g1.split(","))
    g2 = set(g2.split(","))
    edges_cut = []
    for n1 in g1:
        for n2 in original_graph[n1].intersection(g2):
            edges_cut.append("/".join(sorted([n1, n2])))
    return edges_cut, g1, g2



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
