from collections import deque
from copy import deepcopy
import os
import time

def solve():
    input_file_contents = open(os.path.join("input", "day23")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "day23_example")).read().rstrip()
    
    sol_part1 = longest_path(input_file_contents.split("\n"))
    print("Part 1:", sol_part1)

    sol_part2 = solve_pt2(input_file_contents.split("\n"))
    print("Part 2:", sol_part2)


def longest_path(map_trails: list[str]):
    active = deque([((1, 0), set())])
    size_x = len(map_trails[0])
    size_y = len(map_trails[1])
    max_path_size = 0

    while len(active) > 0:
        (i, j), path = active.pop()
        path.add((i, j))
        if (i, j) == (size_x - 2, size_y - 1):
            max_path_size = max(max_path_size, len(path) - 1)
        if map_trails[j][i] == ">":
            descendents = [(i+1, j)]
        elif map_trails[j][i] == "<":
            descendents = [(i-1, j)]
        elif map_trails[j][i] == "v":
            descendents = [(i, j+1)]
        elif map_trails[j][i] == "^":
            descendents = [(i, j-1)]
        else:
            descendents = [
                (ni, nj) for ni, nj in ((i+1, j), (i-1, j), (i, j+1), (i, j-1))
                if 0 <= ni < size_x and 0 <= nj < size_y and map_trails[nj][ni] != "#"
            ]
        for d in descendents:
            if d not in path:
                active.appendleft((d, deepcopy(path)))

    return max_path_size


def solve_pt2(map_trails: list[str]):
    size_x = len(map_trails[0])
    size_y = len(map_trails[1])
    start = (1, 0)
    end = (size_x - 2, size_y - 1)
    bifurcations = set([start, end])

    for j, row in enumerate(map_trails[:-1]):
        for i, c in enumerate(row[:-1]):
            if c != "#":
                antescendents = [
                    (ni, nj) for ni, nj in ((i+1, j), (i-1, j), (i, j+1), (i, j-1))
                    if 0 <= ni < size_x and 0 <= nj < size_y and map_trails[nj][ni] != "#"
                ]
                if len(antescendents) > 2:
                    bifurcations.add((i, j))

    def shortest_path(b1, b2):
        active = deque([(b1, 0)])
        seen = set()
        while len(active) > 0:
            (i, j), n = active.pop()
            seen.add((i, j))
            if (i, j) == b2:
                return n
            if (i, j) in bifurcations and (i, j) != b1:
                continue
            descendents = [
                (ni, nj) for ni, nj in ((i+1, j), (i-1, j), (i, j+1), (i, j-1))
                if 0 <= ni < size_x and 0 <= nj < size_y and map_trails[nj][ni] != "#"
                and (ni, nj) not in seen
            ]
            for d in descendents:
                active.appendleft((d, n + 1))
        return None

    bifurcations_map = {b: dict() for b in bifurcations}
    for bi, b1 in enumerate(list(bifurcations)):
        for b2 in list(bifurcations)[bi + 1:]:
            # Find shortest path between b1 and b2
            if (n := shortest_path(b1, b2)) is not None:
                bifurcations_map[b1][b2] = n
                bifurcations_map[b2][b1] = n
    
    active = deque([(start, set(), 0)])
    max_len = 0
    while len(active) > 0:
        b, prev, n = active.pop()
        if b == end:
            max_len = max(max_len, n)
        prev.add(b)
        for d, dn in bifurcations_map[b].items():
            if d not in prev:
                active.appendleft((d, deepcopy(prev), n + dn))
 
    return max_len

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
