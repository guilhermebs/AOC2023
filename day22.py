from itertools import chain
import os
import time

EXAMPLE = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day22")).read().rstrip()
    #input_file_contents = EXAMPLE

    bricks = []
    for line in input_file_contents.splitlines():
        start, end = line.split("~")
        bricks.append(
            (tuple(int(i) for i in start.split(",")),
             tuple(int(i) for i in end.split(",")))
        )

    bricks_after_fall, supported_by = simulate_fall(sorted_by_z(bricks))
    # can be disintegrated = every time it shows up in a set, the set has len > 2
    cannot_desintegrate = set(chain.from_iterable(bi for bi in supported_by if len(bi) == 1))
    all_bricks = set(i for i, _ in enumerate(bricks))
    sol_part1 = len(all_bricks - cannot_desintegrate)
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def sorted_by_z(bricks):
    return sorted(bricks, key=lambda b: b[1][2])


def simulate_fall(bricks):
    max_x = max(b[1][0] for b in bricks)
    max_y = max(b[1][1] for b in bricks)
    floor_z = [[1 for i in range(max_x + 1)] for j in range(max_y + 1)]
    floor_brick = [[None for i in range(max_x + 1)] for j in range(max_y + 1)]
    supported_by = [set() for _ in bricks]
    new_brick_positions = []
    for bi, b in enumerate(sorted_by_z(bricks)):
        bsx, bex = b[0][0], b[1][0]
        bsy, bey = b[0][1], b[1][1]
        bsz, bez = b[0][2], b[1][2]
        new_z_bot = 0
        # fall to the floor
        for i in range(bsx, bex + 1):
            for j in range(bsy, bey + 1):
                new_z_bot = max(floor_z[j][i], new_z_bot)

        # identify supporting bricks
        for i in range(bsx, bex + 1):
            for j in range(bsy, bey + 1):
                if floor_z[j][i] == new_z_bot:
                    supported_by[bi].add(floor_brick[j][i])

        # raise the floor
        new_z_top = new_z_bot + (bez - bsz)
        for i in range(bsx, bex + 1):
            for j in range(bsy, bey + 1):
                floor_z[j][i] = new_z_top + 1
                floor_brick[j][i] = bi

        new_brick_positions.append((
            (bsx, bsy, new_z_bot), (bex, bey, new_z_top)
        ))

    return new_brick_positions, supported_by


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
