import os
import time
import numpy as np

EXAMPLE="""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day14")).read().rstrip()
    #input_file_contents = EXAMPLE
    platform = np.array([list(row) for row in input_file_contents.splitlines()])
    roll(platform)
    sol_part1 = sum(sum((len(platform) - j) for element in row if element == "O") for j, row in enumerate(platform))
    print("Part 1:", sol_part1)

    platform = np.array([list(row) for row in input_file_contents.splitlines()])
    record = []
    n_cycles = 1000000000
    for nc in range(n_cycles):
        for _ in range(4):
            roll(platform)
            platform = np.rot90(platform, axes=(1, 0))
        platform_str = "\n".join("".join(row) for row in platform)
        if platform_str in record:
            cycling_start = record.index(platform_str)
            break
        record.append(platform_str)

    cycles = record[cycling_start:]
    cycles_remaining = n_cycles - nc - 1
    end_configuration = cycles[cycles_remaining % len(cycles)]
    sol_part2 = sum(sum((len(platform) - j) for element in row if element == "O") for j, row in enumerate(end_configuration.splitlines()))
    print("Part 2:", sol_part2)


def roll(platform):
    for j, row in enumerate(platform):
        for i, element in enumerate(row):
            if element == "O":
                jj = j
                while platform[jj-1][i] == "." and jj > 0:
                    jj -= 1
                platform[j][i] = "."
                platform[jj][i] = "O"


def print_plaftorm(platform):
    print("\n".join("".join(row) for row in platform), "\n")


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
