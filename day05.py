import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day05")).read().rstrip()

    blocks = input_file_contents.split("\n\n")
    seeds = [int(s) for s in blocks[0].split(':')[1].split(" ") if len(s) > 0]
    print(seeds)

    transformations = [Transformation(b) for b in blocks[1:]]

    transformed = list(seeds)
    for t in transformations:
        transformed = [t.get_destination(n) for n in transformed]

    sol_part1 = min(transformed)
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


class Transformation():
    def __init__(self, block: str):
        self.ranges = []
        for line in block.splitlines()[1:]:
            self.ranges.append([int(n) for n in line.split(' ')])

    def get_destination(self, n):
        for (dest, src, l) in self.ranges:
            if src <= n < src + l:
                return dest + (n - src)
        return n

    def get_source(self, n):
        for (dest, src, l) in self.ranges:
            if dest <= n < dest + l:
                return src + (n - src)
        return n


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
