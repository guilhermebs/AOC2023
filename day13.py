import os
import time

EXAMPLE = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day13")).read().rstrip()
    #input_file_contents = EXAMPLE

    blocks = input_file_contents.split("\n\n")
    sol_part1 = sum(find_reflection(block) for block in blocks)
    print("Part 1:", sol_part1)

    sol_part2 = sum(find_reflection_with_smudge(block) for block in blocks)
    print("Part 2:", sol_part2)


def find_reflection(block: str):
    rocks = {(i, j) for j, line in enumerate(block.splitlines())
             for i, c in enumerate(line) if c == "#"}

    bounds = (len(block.splitlines()[0]), len(block.splitlines()))

    for dim in range(2):
        for l in range(0, bounds[dim] - 1):
            if is_reflection(rocks, bounds, l, dim):
                return (l + 1) * (100 if dim == 1 else 1)


def find_reflection_with_smudge(block: str):
    rocks = {(i, j) for j, line in enumerate(block.splitlines())
             for i, c in enumerate(line) if c == "#"}

    bounds = (len(block.splitlines()[0]), len(block.splitlines()))
    original_reflection = find_reflection(block)
    for r in rocks:
        rocks_corrected = rocks - set((r,))
        for dim in range(2):
            for l in range(0, bounds[dim] - 1):
                if is_reflection(rocks_corrected, bounds, l, dim):
                    reflection = (l + 1) * (100 if dim == 1 else 1)
                    if reflection != original_reflection:
                        return (l + 1) * (100 if dim == 1 else 1)


def is_reflection(rocks: set, bounds, l: int, dim: int):
    rocks_not_reflected = {r for r in rocks if r[dim] <= l}
    reflection_expected = {r for r in rocks_not_reflected if r[dim] > 2 * l - bounds[dim] + 1}
    rocks_reflected = rocks.difference(rocks_not_reflected)
    reflected_positions = set()
    for r in rocks_reflected:
        p = list(r)
        p[dim] = l - (p[dim] - l - 1)
        if p[dim] >= 0:
            p = tuple(p)
            if p not in reflection_expected:
                return False
            else:
                reflected_positions.add(tuple(p))
    return reflection_expected == reflected_positions

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
