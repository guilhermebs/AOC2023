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
    input_file_contents = EXAMPLE

    lagoon = dig_lagoon(input_file_contents)
    lagoon_area_v2(lagoon)
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

def lagoon_area_v2(lagoon):
    vertical_edges = sorted(tuple(sorted(edge, key=lambda e: e[1])) for edge in zip(lagoon, lagoon[1:]) if edge[0][0] == edge[1][0])
    y_min, y_max = min(b[1] for b in lagoon),  max(b[1] for b in lagoon)
    crossings = [((y_min, y_max), None)]
    area = 0
    for e in vertical_edges:
        new_crossings = []
        print(crossings)
        breakpoint()
        for s, prev_x in crossings:
            # this section is completely outside the crossing
            if s[0] >= e[1][1] or s[1] <= e[0][1]:
                new_crossings.append((s, prev_x))
            else:
                # partial overlap
                overlap_start, overlap_end = max(e[0][1] + 1, s[0]), min(e[1][1], s[1])
                non_overlap = [((s[0], overlap_start), prev_x), ((overlap_end, s[1]), prev_x)]
                new_crossings.extend(no for no in non_overlap if no[0][0] != no[0][1])
                if prev_x is not None:
                    area += (overlap_end - overlap_start) * (e[0][0] - prev_x)
                    new_crossings.append(((overlap_start, overlap_end), None))
                else:
                    new_crossings.append(((overlap_start, overlap_end), e[0][0] + 1))
        crossings = new_crossings
    
    print(area)

def lagoon_area(lagoon):
    inside_area = 0.5 * sum((p1[1] + p2[1]) * (p1[0] - p2[0]) for p1, p2 in zip(lagoon, lagoon[1:]))
    border_area = sum(abs(p1[i] - p2[i]) for i in range(2) for p1, p2 in zip(lagoon, lagoon[1:]))
    x_min, x_max = min(b[0] for b in lagoon),  max(b[0] for b in lagoon)
    y_min, y_max = min(b[1] for b in lagoon),  max(b[1] for b in lagoon)
    inside = set()
    border = set()
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            crossings = 0
            for n1, n2 in zip(lagoon, lagoon[1:]):
                if n1[1] == n2[1] == y and min(n1[0], n2[0]) <= x <= max(n1[0], n2[0]): # horizontal edge
                    border.add((x, y))
                if n1[0] == n2[0] == x and min(n1[1], n2[1]) <= y <= max(n1[1], n2[1]):  # vertical edge
                    border.add((x, y))
                elif n1[0] == n2[0] < x:  # inside
                    crossings += 1 if min(n1[1], n2[1]) <= y < max(n1[1], n2[1]) else 0
            if crossings % 2 == 1: 
                inside.add((x, y))
            
    total = inside | border
    print(inside.intersection(border))
    image = "\n".join("".join("#" if (x, y) in border else "." for x in range(x_min, x_max + 1)) for y in range(y_min, y_max+1)) 
    print(image)
    print("Double counted")
    image = "\n".join("".join("#" if (x, y) in inside.intersection(border) else "." for x in range(x_min, x_max + 1)) for y in range(y_min, y_max+1)) 
    print(image)
    print(len(inside), len(border), len(border - inside), len(total))
    print(inside_area, border_area, inside_area + border_area)
    return len(total)
        

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
