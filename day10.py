import os
import time
from collections import deque


EXAMPLE = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".strip()

EXAMPLE2 = """
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".strip()

EXAMPLE3 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".strip()

EXAMPLE4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".strip()

EXAMPLE5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip()


def solve():
    input_file_contents = open(os.path.join("input", "day10")).read().rstrip()
    #input_file_contents = EXAMPLE5
    pipes = {
        (i, j): get_neighbours((i, j), c) for j, line in enumerate(input_file_contents.splitlines())
        for i, c in enumerate(line.strip()) if c != "."
    }
    start_pipe = [k for k, v in pipes.items() if v is None][0]
    pipes[start_pipe] = tuple(k for k, v in pipes.items() if k is not start_pipe and start_pipe in v)
    pipes = {k: set(v).intersection(pipes.keys()) for k, v in pipes.items()}
    sol_part1, loop = find_loop(pipes, start_pipe)
    n_rows = len(input_file_contents.splitlines())
    n_cols = len(input_file_contents.splitlines()[0])
    print("Part 1:", sol_part1)
    area_map = [[False] * 2*n_cols for i in range(2*n_rows)]
    for i, j in loop:
        area_map[2*j][2*i] = True
        area_map[2*j + 1][2*i] = (i, j + 1) in pipes[(i, j)]
        area_map[2*j][2*i + 1] = (i + 1, j) in pipes[(i, j)]

    area_map_debug = [["P" if c else "." for c in row] for row in area_map]
    inside = set()
    for j, row in enumerate(area_map):
        if j == 0:
            continue
        crossings = 0
        in_border = False
        has_above = False
        has_below = False
        try:
            max_col = max(i for i, v in enumerate(row) if v)
        except ValueError:
            continue
        for i in range(max_col):
            e = row[i]
            # we are in the border
            if e:
                in_border = True
                has_above = has_above or area_map[j-1][i]
                has_below = has_below or area_map[j+1][i]
            # we are no longer in a border region
            else:
                # increment crossing
                if in_border and has_above and has_below:
                    crossings += 1
                in_border = False
                has_above = False
                has_below = False
                if crossings % 2 == 1 and i % 2 == 0 and j % 2 == 0:
                    inside.add((i//2, j//2))
                area_map_debug[j][i] = str(crossings % 2)

    #print("\n".join("".join(row) for row in area_map_debug))
    debug = [list(line) for line in input_file_contents.splitlines()]
    for (i, j) in inside:
        debug[j][i] = "I"
    debug = '\n'.join(''.join(line) for line in debug)
    #print(debug)
    print("Part 2:", len(inside))


def get_neighbours(pos, pipe):
    if pipe == "|":
        return (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)
    elif pipe == "-":
        return (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])
    elif pipe == "L":
        return (pos[0], pos[1] - 1), (pos[0] + 1, pos[1])
    elif pipe == "J":
        return (pos[0], pos[1] - 1), (pos[0] - 1, pos[1])
    elif pipe == "7":
        return (pos[0], pos[1] + 1), (pos[0] - 1, pos[1])
    elif pipe == "F":
        return (pos[0], pos[1] + 1), (pos[0] + 1, pos[1])
    elif pipe == "S":
        return None 
    elif pipe == ".":
        return ()
    else:
        raise ValueError(f"Unexpectd pipe: {pipe}")


def find_loop(pipes, start_pipe):
    queue = deque([(start_pipe, 0, [start_pipe])])
    seen = {}
    seen[start_pipe] = (0, [start_pipe])
    while len(queue) > 0:
        position, i, visited = queue.popleft()
        for n in pipes[position]:
            if n not in pipes:
                continue
            if n not in seen:
                queue.append((n, i+1, visited + [n]))
                seen[n] = (i + 1, visited + [n])
            elif seen[n][0] == i + 1:
                return i + 1, set(visited) | set(seen[n][1])


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
