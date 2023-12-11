import os
import time
import copy

EXAMPLE = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day11")).read().rstrip()
    #input_file_contents = EXAMPLE
    galaxies = [
        [i, j] for j, line in enumerate(input_file_contents.splitlines())
        for i, c in enumerate(line) if c == "#"]

    galaxies_exp = expand_universe(galaxies, 1)

    sol_part1 = sum((abs(gi[0] - gj[0]) + abs(gi[1] - gj[1]) for i, gi in enumerate(galaxies_exp) for gj in galaxies_exp[i:]))
    print("Part 1:", sol_part1)

    galaxies_exp = expand_universe(galaxies, 1_000_000 - 1)
    #galaxies_exp = expand_universe(galaxies, 100 - 1)
    sol_part2 = sum((abs(gi[0] - gj[0]) + abs(gi[1] - gj[1]) for i, gi in enumerate(galaxies_exp) for gj in galaxies_exp[i:]))
    print("Part 2:", sol_part2)


def expand_universe(galaxies, factor):
    galaxies = copy.deepcopy(galaxies)
    for dim in (0, 1):
        max_dim = max(g[dim] for g in galaxies)
        to_expand = [i for i in range(max_dim) if not any(g[dim] == i for g in galaxies)]
        for g in galaxies:
            g[dim] += sum(factor if c < g[dim] else 0 for c in to_expand)
    return galaxies


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
