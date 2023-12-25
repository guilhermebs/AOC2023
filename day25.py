from collections import Counter
from copy import deepcopy
import os
import time
import networkx as nx


def solve():
    input_file_contents = open(os.path.join("input", "day25")).read().rstrip()
    
    graph = nx.Graph()
    for line in input_file_contents.splitlines():
        from_, to_ = line.split(": ")
        for t in to_.split(" "):
            graph.add_edge(from_, t)

    cut_value, partition = nx.stoer_wagner(graph)
    assert cut_value == 3
    sol_part1 = len(partition[0]) * len(partition[1])
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
