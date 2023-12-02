import os
import time
import functools


def solve():
    input_file_contents = open(os.path.join("input", "day02")).read().rstrip()

    limits = {"red": 12, "green": 13, "blue": 14}
    sol_part1 = 0
    for i, line in enumerate(input_file_contents.splitlines()):
        _, balls = line.split(":")
        is_possible = True
        for sets in balls.split(";"):
            for ball_info in sets.strip().split(","):
                n, color = ball_info.strip().split(" ")
                if int(n) > limits[color]:
                    is_possible = False
        if is_possible:
            sol_part1 += i+1

    print("Part 1:", sol_part1)

    sol_part2 = 0
    for i, line in enumerate(input_file_contents.splitlines()):
        _, balls = line.split(":")
        required = {"red": 0, "blue": 0, "green": 0}
        for sets in balls.split(";"):
            for ball_info in sets.strip().split(","):
                n, color = ball_info.strip().split(" ")
                required[color] = max(required[color], int(n))
        sol_part2 += functools.reduce(lambda x, y: x * y, required.values())


    print("Part 2:", sol_part2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
