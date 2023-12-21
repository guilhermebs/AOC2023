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
    input_file_contents = EXAMPLE

    region_map = input_file_contents.splitlines()
    start = None
    for j, row in enumerate(region_map):
        if (i := row.find("S")) != -1:
            start = (i, j)


    sol_part1 = can_reach(region_map, start, 6)
    print("Part 1:", sol_part1)

    sol_part2 = can_reach_infinite(region_map, start, 5000)
    print("Part 2:", sol_part2)


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
        print(i+1, len(positions))

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
        #breakpoint()
        next_edge = next_step - prev_edge
        bulk[i % 2] += len(prev_edge)
        prev_edge = edge
        edge = next_edge
        if i%100 == 0:
            print(len(edge))

    return bulk[i % 2] + len(edge)


def print_map(region_map, positions):
    for j, row in enumerate(region_map):
        print("".join("O" if (i, j) in positions else c for i, c in enumerate(row)))


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
