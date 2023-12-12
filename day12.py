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

    print(count_possible("?????#?#???#? 1,1,3,1"))
    #  #?#??###???#?
    #  #??#?###???#?
    #  ?#?#?###???#?
    #  #????#?###?#?
    #  ?#???#?###?#?
    #  ??#??#?###?#?
    #  ???#?#?###?#?
    #count_possible("???????? 4,1,1")
    sol_part1 = sum(count_possible(line) for line in input_file_contents.splitlines())
    #sol_part1 = None
    print("Part 1:", sol_part1)

    sol_part2 = None
    print("Part 2:", sol_part2)


def count_possible(line):
    pipes, groups = line.split(" ")
    groups = tuple(int(i) for i in groups.split(","))
    n = number_possible(pipes + ".", groups)
    print(line, n)
    return n


#@functools.cache
def number_possible(pipes, groups):
    count = 0
    for i in range(len(pipes) - groups[0]):
        if all(p in ("?", "#") for p in pipes[i:i+groups[0]]) and pipes[i+groups[0]] in ("?", "."):
            if len(groups) == 1:
                # No more unnacounted "#" ahead
                if all(p in ("?", ".") for p in pipes[i+groups[0]:]):
                    count += 1
                else:
                    continue
            else:
                n_pos = number_possible(pipes[i+groups[0]+1:], groups[1:])
                #print(pipes[:i+groups[0]+1], pipes[i+groups[0]+1:], groups, n_pos)
                count += n_pos
        if pipes[i] == "#":
            break
    return count


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
