import os
import time
import re
import itertools
import math


def solve():
    input_file_contents = open(os.path.join("input", "day08")).read().rstrip()
    instructions, nodes_str = input_file_contents.split("\n\n")
    nodes = {
        match.group(1): (match.group(2), match.group(3))
        for match in re.finditer(r"(\w+) = \((\w+), (\w+)\)", nodes_str)
    }
    print("Part 1:", steps_to_z("AAA", nodes, instructions))

    steps_required = [steps_to_z(n, nodes, instructions) for n in nodes if n[-1] == "A"]

    print("Part 2:", math.lcm(*steps_required))


def steps_to_z(start_node, nodes, instructions):
    i = 0
    cur_node = start_node
    while cur_node[-1] != "Z":
        s = 0 if instructions[i % len(instructions)] == "L" else 1
        cur_node = nodes[cur_node][s]
        i += 1
    assert i % len(instructions) == 0
    return i


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
