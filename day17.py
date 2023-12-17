import heapq
import os
import time

EXAMPLE = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".strip()

def solve():
    input_file_contents = open(os.path.join("input", "day17")).read().rstrip()
    #input_file_contents = EXAMPLE

    heat_map = [[int(c) for c in line] for line in input_file_contents.splitlines()]

    sol_part1 = path_search(heat_map)
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def path_search(heat_map):
    heap = [(0, ((0, 0), (0, 0), 0))]
    heapq.heapify(heap)
    seen = set()
    map_dims = (len(heat_map[0]), len(heat_map))
    objective = (len(heat_map[0]) - 1, len(heat_map) - 1)
    while len(heap) > 0:
        cost, state = heapq.heappop(heap)
        if state[0] == objective:
            return cost
        for d in descendents(map_dims, state):
            if d not in seen:
                seen.add(d)
                heapq.heappush(
                    heap,
                    (cost + heat_map[d[0][0]][d[0][1]], d)
                )

    return None


def descendents(map_dims, state):
    pos, dir_, n_prev = state
    east = (1, 0)
    west = (-1, 0)
    north = (0, -1)
    south = (0, 1)
    oposite = {
        east: west,
        west: east,
        north: south,
        south: north,
        (0, 0): None
    }

    def is_dir_ok(d):
        return (
            0 <= tuplesum(d, pos)[0] < map_dims[0] and
            0 <= tuplesum(d, pos)[1] < map_dims[1] and
            not (n_prev == 3 and d == dir_) and
            d != oposite[dir_])

    return [
        (tuplesum(d, pos), d, n_prev + 1 if d == dir_ else 1)
        for d in (east, west, north, south) if is_dir_ok(d)
    ]


def tuplesum(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
