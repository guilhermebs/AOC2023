import functools
import os
import time

EXAMPLE = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".strip()


def solve():
    input_file_contents = open(os.path.join("input", "day12")).read().rstrip()
    #input_file_contents = EXAMPLE


    sol_part1 = sum(count_possible(line) for line in input_file_contents.splitlines())
    print("Part 1:", sol_part1)

    sol_part2 = sum(count_pt2(line) for line in input_file_contents.splitlines())
    print("Part 2:", sol_part2)


def count_possible(line):
    pipes, groups = line.split(" ")
    groups = tuple(int(i) for i in groups.split(","))
    n = number_possible(pipes + ".", groups)
    return n


def count_pt2(line):
    pipes, groups = line.split(" ")
    groups = tuple(int(i) for i in groups.split(",")) * 5
    n = number_possible("?".join([pipes]*5) + ".", groups)
    return n


@functools.cache
def number_possible(pipes, groups):
    count = 0
    if len(groups) == 0:
        return int(not ("#" in pipes))
    for i in range(len(pipes) - groups[0]):
        if all(p in ("?", "#") for p in pipes[i:i+groups[0]]) and pipes[i+groups[0]] in ("?", "."):
            count += number_possible(pipes[i+groups[0]+1:], groups[1:])
        if pipes[i] == "#":
            break
    return count


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
