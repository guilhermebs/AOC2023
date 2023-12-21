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
    #input_file_contents = EXAMPLE

    region_map = input_file_contents.splitlines()
    for j, row in enumerate(region_map):
        if (i := row.find("S")) != -1:
            start = (i, j)
            row.replace('S', '.')

    print(start)
    
    sol_part1 = can_reach(region_map, start, 64)
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def can_reach(region_map, start_pos, n_steps):
    mi, mj = len(region_map[0]), len(region_map)
    positions = set([start_pos])
    for _ in range(n_steps):
        next_positions = set()
        for pi, pj in positions:
            for ni, nj in [(pi + 1, pj), (pi - 1, pj), (pi, pj + 1), (pi, pj - 1)]:
                if 0 <= ni < mi and 0 <= nj < mj and region_map[nj][ni] in ".S":
                    next_positions.add((ni, nj))
        positions = next_positions
    print(positions)
    return len(positions)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
