import os
import time

EXAMPLE = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".strip()


def solve():
    input_file_contents = open(os.path.join("input", "day21")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "day21_expanded")).read().rstrip()
    #input_file_contents = EXAMPLE

    region_map = input_file_contents.splitlines()
    start = None
    for j, row in enumerate(region_map):
        if (i := row.find("S")) != -1:
            start = (i, j)


    sol_part1 = can_reach(region_map, start, 64)
    print("Part 1:", sol_part1)

    x = [0, 1, 2, 3, 4]
    y = [
        can_reach_infinite(region_map, start, 65 + 131 * xi)
        for xi in x
    ]

    # quadratic fit
    c = y[0]
    b = (y[1] * 4 - y[2] - 3*c) // 2
    a = y[1] - b - c
    assert all(yi == a * xi**2 + b * xi + c for yi, xi in zip(y, x))
    # extrapolate
    target = 26501365
    x_t = (target - 65) // 131
    assert (target - 65) % 131 == 0
    print("Part 2:", a * x_t**2 + b * x_t + c)



def can_reach(region_map, start_pos, n_steps):
    mi, mj = len(region_map[0]), len(region_map)
    positions = set([start_pos])
    for i in range(n_steps):
        next_positions = set()
        for pi, pj in positions:
            for ni, nj in [(pi + 1, pj), (pi - 1, pj), (pi, pj + 1), (pi, pj - 1)]:
                if 0 <= ni < mi and 0 <= nj < mj and region_map[nj][ni] in ".S":
                    next_positions.add((ni, nj))
        positions = next_positions

    #open("tmp", "w").write(map_str(region_map, positions))
    return len(positions)


def can_reach_infinite(region_map, start_pos, n_steps):
    mi, mj = len(region_map[0]), len(region_map)
    prev_edge = set()
    edge = set([start_pos])
    bulk = [0, 0]
    for i in range(n_steps):
        next_step = set()
        for pi, pj in edge:
            for ni, nj in [(pi + 1, pj), (pi - 1, pj), (pi, pj + 1), (pi, pj - 1)]:
                if region_map[nj % mj][ni % mi] in ".S":
                    next_step.add((ni, nj))
        next_edge = next_step - prev_edge
        bulk[i % 2] += len(prev_edge)
        prev_edge = edge
        edge = next_edge

    return bulk[i % 2] + len(edge)


def map_str(region_map, positions):
    return "\n".join(
        "".join("O" if (i, j) in positions else c for i, c in enumerate(row))
        for j, row in enumerate(region_map))


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
