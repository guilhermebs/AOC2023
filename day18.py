import os
import time

EXAMPLE = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day18")).read().rstrip()
    #input_file_contents = EXAMPLE

    lagoon = dig_lagoon(input_file_contents)
    sol_part1 = lagoon_area(lagoon)
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def dig_lagoon(instructions):
    lagoon_nodes = [complex(0, 0)]
    directions = {
        "R": complex(1, 0),
        "D": complex(0, 1),
        "L": complex(-1, 0),
        "U": complex(0, -1),
    }
    for line in instructions.splitlines():
        dir_, n, _ = line.split()
        next_node = lagoon_nodes[-1] + (int(n)) * directions[dir_]
        lagoon_nodes.append(next_node)
    
    assert lagoon_nodes[-1] == lagoon_nodes[0]
    return [(int(b.real), int(b.imag)) for b in lagoon_nodes]


def lagoon_area(lagoon):
    x_min, x_max = min(b[0] for b in lagoon),  max(b[0] for b in lagoon)
    y_min, y_max = min(b[1] for b in lagoon),  max(b[1] for b in lagoon)
    inside = set()
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            crossings = 0
            for n1, n2 in zip(lagoon, lagoon[1:]):
                if n1[1] == n2[1] == y and min(n1[0], n2[0]) <= x <= max(n1[0], n2[0]): # horizontal edge
                    inside.add((x, y))
                if n1[0] == n2[0] == x and min(n1[1], n2[1]) <= y <= max(n1[1], n2[1]):  # vertical edge
                    inside.add((x, y))
                elif n1[0] == n2[0] < x:  # inside
                    crossings += 1 if min(n1[1], n2[1]) <= y < max(n1[1], n2[1]) else 0
            if crossings % 2 == 1: 
                inside.add((x, y))
            
    return len(inside)
        

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
