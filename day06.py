import time
import math


def solve():
    times = [47, 70, 75, 66]
    distances = [282, 1079, 1147, 1062]

    sol_part1 = 1
    for tl, d in zip(times, distances):
        a, b = time_button_pressed(tl, d)
        sol_part1 *= (math.ceil(b) - math.floor(a) - 1)

    print("Part 1:", sol_part1)

    a, b = time_button_pressed(47707566, 282107911471062)
    sol_part2 = math.ceil(b) - math.floor(a) - 1
    print("Part 2:", sol_part2)


def distance_traveled(tl, tb):
    return tb * (tl - tb)


def time_button_pressed(tl, d):
    # d = tb * (tl - tb)
    # -tb**2 + tb*tl - d = 0
    return ((tl - math.sqrt(tl**2-4*d))/2, (tl + math.sqrt(tl**2-4*d))/2)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
