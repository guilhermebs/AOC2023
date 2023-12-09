import os
import time

def solve():
    input_file_contents = open(os.path.join("input", "day09")).read().rstrip()
    sol_part1 = 0
    sol_part2 = 0
    for line in input_file_contents.splitlines():
        sequence = [int(s) for s in line.split()]
        start, end = extrapolate_value(sequence)
        sol_part1 += end
        sol_part2 += start

    print("Part 1:", sol_part1)
    print("Part 2:", sol_part2)


def extrapolate_value(sequence):
    start = 0
    end = 0
    i = 1
    while any(n != 0 for n in sequence):
        end += sequence[-1]
        start = sequence[0] - start
        sequence = [n2 - n1 for n1, n2 in zip(sequence, sequence[1:])]
        i += 1
    return (-1)**i * start, end

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
