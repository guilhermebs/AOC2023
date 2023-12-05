import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day05")).read().rstrip()

    blocks = input_file_contents.split("\n\n")
    seeds = [int(s) for s in blocks[0].split(':')[1].split(" ") if len(s) > 0]

    transformations = [Transformation(b) for b in blocks[1:]]

    transformed = list(seeds)
    for t in transformations:
        transformed = [t.get_destination(n) for n in transformed]

    sol_part1 = min(transformed)
    print("Part 1:", sol_part1)

    transformed_ranges = list(zip(seeds[0::2], seeds[1::2]))

    for t in transformations:
        transformed_ranges = [
            r for rg in transformed_ranges for r in t.get_destination_ranges(*rg)
        ]

    breakpoint()

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

    def get_destination_ranges(self, n, ln):
        destination_ranges = []
        handled = []
        for (dest, src, l) in self.ranges:
            # the start of the interval is inside "src"
            if src <= n < src + l:
                destination_ranges.append((
                    dest + (n - src), min(ln, l - (n - src))
                ))
                handled.append((n, min(ln, l - (n - src))))
            # Some other part of the interval is inside "src"
            if n <= src < n + ln:
                destination_ranges.append((
                    dest, min(l, ln - (src - n))
                ))
                handled.append((src, min(l, ln - (src - n))))
        print(ln, sum(dr[1] for dr in destination_ranges))
        handled = sorted(handled)
        handled.append((n + ln, 0))
        for i, (s, ns) in enumerate(handled[:-1]):
            next_s, _ = handled[i + 1]
            if s + ns != next_s:
                print("Adding")
                destination_ranges.append((s + ns, next_s - (s + ns)))
        print(ln, sum(dr[1] for dr in destination_ranges))
        return destination_ranges


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
