from collections import deque
from copy import deepcopy
import os
import time

def solve():
    input_file_contents = open(os.path.join("input", "day23")).read().rstrip()
    input_file_contents = open(os.path.join("input", "day23_example")).read().rstrip()

    sol_part1 = longest_path(input_file_contents.split("\n"))
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def longest_path(map_trails: list[str]):
    active = {(1, 0): set()}
    size_x = len(map_trails[0])
    size_y = len(map_trails[1])
    max_path_size = 0

    while len(active) > 0:
        (i, j), path = active.popitem()
        path.add((i, j))
        if (i, j) == (size_x - 2, size_y - 1):
            print(len(path) - 1)
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
            if d in path:
                continue
            if d not in active or len(path) > len(active[d]):
                active[d] = deepcopy(path)

    return max_path_size


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
