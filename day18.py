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
    sol_part1 = lagoon_area([(0,0), (0, 2), (2, 2), (2, 0), (0, 0)])
    #######
    #.....#
    #.....#
    #.###.#
    #.#.#.#
    ###.###
    # answer: 40
    sol_part1 = lagoon_area([(0, 2), (0, 7), (2, 7), (2, 5), (4, 5), (4, 7), (6, 7), (6, 2), (0, 2)])
    #######
    #.....#
    #...###
    #...#..
    #...###
    #.....#
    #######
    # answer: 47
    sol_part1 = lagoon_area([(0,2), (0, 8), (6, 8), (6, 6), (4, 6), (4, 4), (6, 4), (6, 2), (0, 2)])
    sol_part1 = lagoon_area(lagoon[::-1])
    print("Part 1:", sol_part1)

    lagoon_pt2 = dig_lagoon_pt2(input_file_contents)
    sol_part2 = lagoon_area(lagoon_pt2[::-1])
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


def dig_lagoon_pt2(instructions):
    lagoon_nodes = [complex(0, 0)]
    directions = [
        complex(1, 0),
        complex(0, 1),
        complex(-1, 0),
        complex(0, -1),
    ]
    for line in instructions.splitlines():
        _, _, hex_ = line.split()
        dir_ = int(hex_[-2])
        n = int(hex_[2:-2], 16)
        next_node = lagoon_nodes[-1] + (int(n)) * directions[dir_]
        lagoon_nodes.append(next_node)
    
    assert lagoon_nodes[-1] == lagoon_nodes[0]
    return [(int(b.real), int(b.imag)) for b in lagoon_nodes]


def lagoon_area(lagoon):
    total_area = 0
    for p1, p2 in zip(lagoon, lagoon[1:]):
        if p1[0] == p2[0]:
            total_area += max(p1[1], p2[1]) + 1
        else:
            dx = p2[0] - p1[0]
            y = p1[1]
            if dx > 0:
                dx -= 1
                y += 1
            else:
                dx -= 1
                total_area -= 1
            total_area += dx * y
    total_area += 1
    return total_area


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
