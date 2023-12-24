import z3
import os
import time

def solve():
    input_file_contents = open(os.path.join("input", "day24")).read().rstrip()

    hail_stones = []
    for line in input_file_contents.splitlines():
        p_str, v_str = line.split("@")
        hail_stones.append((
            tuple(int(p) for p in p_str.split(",")),
            tuple(int(v) for v in v_str.split(",")),
        ))

    sol_part1 = 0
    area_min = 200000000000000
    area_max = 400000000000000
    for a, (pa, va) in enumerate(hail_stones):
        for pb, vb in hail_stones[a + 1:]:
            pc = find_intersection(pa, va, pb, vb)
            if pc is not None and \
               (pc[0] - pa[0]) / va[0] > 0 and\
               (pc[0] - pb[0]) / vb[0] > 0 and \
               all(area_min < p < area_max for p in pc):
                sol_part1 += 1

    print("Part 1:", sol_part1)

    sol_part2 = part2_z3(hail_stones)
    print("Part 2:", sol_part2)


def find_intersection(pa, va, pb, vb):
    pa2 = tuple(p + 10 * v for p, v in zip(pa, va))
    pb2 = tuple(p + 10 * v for p, v in zip(pb, vb))
    den = (pa[0] - pa2[0]) * (pb[1] - pb2[1]) - (pa[1] - pa2[1]) * (pb[0] - pb2[0])
    if den == 0:
        return None
    return (
        ((pa[0] * pa2[1] - pa[1] * pa2[0]) * (pb[0] - pb2[0]) - (pb[0] * pb2[1] - pb[1] * pb2[0]) * (pa[0] - pa2[0])) / den,
        ((pa[0] * pa2[1] - pa[1] * pa2[0]) * (pb[1] - pb2[1]) - (pb[0] * pb2[1] - pb[1] * pb2[0]) * (pa[1] - pa2[1])) / den,
    )


def part2_z3(hail_stones):
    s = z3.Solver()
    stone_p = (z3.Int('sx'), z3.Int('sy'), z3.Int('sz'))
    stone_v = (z3.Int('vsx'), z3.Int('vsy'), z3.Int('vsz'))
    for p, v in hail_stones:
        s.add((stone_p[0] - p[0]) * (v[1] - stone_v[1]) == (stone_p[1] - p[1]) * (v[0] - stone_v[0]))
        s.add((stone_p[0] - p[0]) * (v[2] - stone_v[2]) == (stone_p[2] - p[2]) * (v[0] - stone_v[0]))
    
    print(s.check())
    m = s.model()
    print("position:", ", ".join(str(m.evaluate(p)) for p in stone_p))
    print("velocity:", ", ".join(str(m.evaluate(v)) for v in stone_v))
    return sum(m.evaluate(p).as_long() for p in stone_p)


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
