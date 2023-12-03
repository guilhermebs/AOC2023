import os
import time
import re

DIGITS = [str(i) for i in range(10)]


def solve():
    input_file_contents = open(os.path.join("input", "day03")).read().rstrip()
    grid = create_grid(input_file_contents)
    part_numbers = set()
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if isinstance(element, str):
                for ii in range(max(0, i-1), min(i+2, len(grid))):
                    for jj in range(max(0, j-1), min(j+2, len(row))):
                        if isinstance(grid[ii][jj], tuple):
                            part_numbers.add(grid[ii][jj])
    print(part_numbers) 
    sol_part1 = sum(p[0] for p in part_numbers)
    print("Part 1:", sol_part1)

    sol_part2 = 0
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if element == "*":
                adjacent_numbers = set()
                for ii in range(max(0, i-1), min(i+2, len(grid))):
                    for jj in range(max(0, j-1), min(j+2, len(row))):
                        if isinstance(grid[ii][jj], tuple):
                            adjacent_numbers.add(grid[ii][jj])
                if len(adjacent_numbers) == 2:
                    adjacent_numbers = list(adjacent_numbers)
                    sol_part2 += adjacent_numbers[0][0] * adjacent_numbers[1][0]

    print("Part 2:", sol_part2)


def create_grid(input_file_contents: str):
    grid = []

    def iter_numbers(row, i):
        for m in re.finditer(r"(\d+)", row):
            for j in range(m.span()[0], m.span()[1]):
                yield (int(m[0]), i, m.span()[0])

    for i, row in enumerate(input_file_contents.splitlines()):
        grid.append([])
        numbers_iter = iter_numbers(row, i)
        for j, element in enumerate(row):
            if element == ".":
                grid[-1].append(None)
            elif element in DIGITS:
                grid[-1].append(next(numbers_iter))
            else:
                grid[-1].append(element)

    return grid

        
if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
