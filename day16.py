import os
import time
import multiprocessing
import functools

EXAMPLE = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day16")).read().rstrip()
    #input_file_contents = EXAMPLE
    cave = input_file_contents.splitlines()
    sol_part1 = count_energized(cave,((0, 0), ">"))
    print("Part 1:", sol_part1)

    starting_positions = []
    for j, direction in ((0, "v"), (len(cave) - 1, "^")):
        starting_positions.extend(((i, j), direction) for i, _ in enumerate(cave[0]))

    for i, direction in ((0, ">"), (len(cave[0]) - 1, "<")):
        starting_positions.extend(((i, j), direction) for j, _ in enumerate(cave))

    with multiprocessing.Pool(8) as p:
        results = p.map(functools.partial(count_energized, cave), starting_positions)

    sol_part2 = max(results)
    print("Part 2:", sol_part2)


def count_energized(cave, start):
    energized = propagate_beam(cave, start)
    return len(set(p for p, _ in energized))


def propagate_beam(cave, start):
    beam_fronts = [start]
    seen = set()
    while len(beam_fronts) > 0:
        bf = beam_fronts.pop()
        seen.add(bf)
        for d in descendents(bf, cave):
            if d not in seen:
                beam_fronts.append(d)
    return seen


def descendents(beam_front, cave):
    result = []
    imax = len(cave[0]) - 1
    jmax = len(cave) - 1
    (i, j), direction = beam_front
    match (cave[j][i], direction):
        case (".", ">") | ("-", ">"):
            result = [((i+1, j), ">")]
        case (".", "<") | ("-", "<"):
            result = [((i-1, j), "<")]
        case (".", "^") | ("|", "^"):
            result = [((i, j-1), "^")]
        case (".", "v") | ("|", "v"):
            result = [((i, j+1), "v")]
        case ("/", ">"):
            result = [((i, j-1), "^")]
        case ("/", "<"):
            result = [((i, j+1), "v")]
        case ("/", "^"):
            result = [((i+1, j), ">")]
        case ("/", "v"):
            result = [((i-1, j), "<")]
        case ("\\", ">"):
            result = [((i, j+1), "v")]
        case ("\\", "<"):
            result = [((i, j-1), "^")]
        case ("\\", "^"):
            result = [((i-1, j), "<")]
        case ("\\", "v"):
            result = [((i+1, j), ">")]
        case ("|", ">") | ("|", "<"):
            result = [((i, j+1), "v"), ((i, j-1), "^")]
        case ("-", "^") | ("-", "v"):
            result = [((i-1, j), "<"), ((i+1, j), ">")]
        case _:
            raise ValueError("Invalid!")

    return [r for r in result if (0 <= r[0][0] <= imax and 0 <= r[0][1] <= jmax)]


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
