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

    sol_part1 = path_search(heat_map, 1, 3)
    print("Part 1:", sol_part1)

    sol_part2 = path_search(heat_map, 4, 10)
    print("Part 2:", sol_part2)


def path_search(heat_map, min_seq, max_seq):
    start_state = ((0, 0), (0, 0))
    heap = [(0, start_state)]
    heapq.heapify(heap)
    costs = {start_state: 0}
    map_dims = (len(heat_map[0]), len(heat_map))
    objective = (len(heat_map[0]) - 1, len(heat_map) - 1)
    t = 0
    while len(heap) > 0:
        t += 1
        f, state = heapq.heappop(heap)
        if state[0] == objective:
            return costs[state]
        for d_row in descendents(map_dims, state, min_seq, max_seq):
            if len(d_row) == 0:
                continue
            new_cost = costs[state]
            for i in range(1, min_seq):
                new_cost += heat_map[state[0][0] + d_row[0][1][0] * i][state[0][1] + d_row[0][1][1] * i]
            for d in d_row:
                new_cost += heat_map[d[0][0]][d[0][1]]
                f = heuristic(d, objective) + new_cost
                if d not in costs or new_cost < costs[d]:
                    heapq.heappush(heap, (f, d))
                    costs[d] = new_cost

    return None


def descendents(map_dims, state, min_seq, max_seq):
    pos, dir_ = state
    pos = complex(*pos)
    east = complex(1, 0)
    west = complex(-1, 0)
    north = complex(0, -1)
    south = complex(0, 1)
    new_dir = {
        (1, 0): (north, south),
        (-1, 0): (north, south),
        (0, -1): (east, west),
        (0, 1): (east, west),
        (0, 0): (north, south, east, west)
    }

    def is_ok(d, i):
        return (
            0 <= (d*i + pos).real < map_dims[0] and
            0 <= (d*i + pos).imag < map_dims[1])

    return [
        [(cmp2tup(d*i + pos), cmp2tup(d)) for i in range(min_seq, max_seq+1) if is_ok(d, i)]
        for d in new_dir[dir_]
    ]


def heuristic(state, objective):
    pos, _ = state
    return abs(pos[0] - objective[0]) + abs(pos[1] - objective[1])


def cmp2tup(cmp):
    return (int(cmp.real), int(cmp.imag))

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
