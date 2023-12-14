import os
import time

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
    platform = [list(row) for row in input_file_contents.splitlines()]

    for j, row in enumerate(platform):
        for i, element in enumerate(row):
            if element == "O":
                jj = j
                while platform[jj-1][i] == "." and jj > 0:
                    jj -= 1
                platform[j][i] = "."
                platform[jj][i] = "O"

    sol_part1 = sum(sum((len(platform) - j) for element in row if element == "O") for j, row in enumerate(platform))
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def print_plaftorm(platform):
    print("\n".join("".join(row) for row in platform))


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
