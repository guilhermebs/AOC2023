import copy
from math import prod
import os
import time
import operator

CATEGORIES = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}

def solve():
    input_file_contents = open(os.path.join("input", "day19")).read().rstrip()
    rules_str, parts_str = input_file_contents.split("\n\n")
    rules = {}
    for line in rules_str.splitlines():
        name, rule = line.split("{")
        rule = rule[:-1].split(",")
        final_workflow = rule[-1]
        rules[name] = [
           (CATEGORIES[r[0]], operator.gt if r[1] == '>' else operator.lt, int(r[2:].split(":")[0]), r[2:].split(":")[1])
           for r in rule[:-1]
        ] + [final_workflow]

    parts = [tuple(int(c[2:]) for c in line[1:-1].split(",")) for line in parts_str.splitlines()]

    sol_part1 = sum(sum(p) for p in parts if apply_rules(p, rules))
    print("Part 1:", sol_part1)

    sol_part2 = pt2(rules)
    print("Part 2:", sol_part2)


def apply_rules(part, rules):
    rule_name = 'in'
    while rule_name not in ('A', 'R'):
        for r in rules[rule_name][:-1]:
            if r[1](part[r[0]], r[2]):
                rule_name = r[3]
                break
        else:
            rule_name = rules[rule_name][-1]

    return rule_name == 'A'

def pt2(rules):
    to_process = [['in', [(1, 4000)]*4]]
    accepted = []
    rejected = []
    rule_name = 'in'

    while len(to_process) > 0:
        rule_name, interval = to_process.pop()
        if rule_name == 'A':
            accepted.append(interval)
            continue
        elif rule_name == 'R':
            rejected.append(interval)
            continue
        for r in rules[rule_name][:-1]:
            if r[1] == operator.lt:
                # Interval is totaly outside the limit
                if interval[r[0]][0] >= r[2]:
                    continue
                # Interval is totaly inside the limit
                elif interval[r[0]][1] < r[2]:
                    to_process.append([r[3], interval])
                    break
                # interval partially within the limit
                else:
                    interval_in_limit = copy.deepcopy(interval)
                    interval_in_limit[r[0]] = (interval[r[0]][0], r[2] - 1) 
                    to_process.append([r[3], interval_in_limit])
                    interval[r[0]] = (r[2], interval[r[0]][1]) 
            if r[1] == operator.gt:
                # Interval is totaly outside the limit
                if interval[r[0]][1] <= r[2]:
                    continue
                # Interval is totaly inside the limit
                elif interval[r[0]][0] > r[2]:
                    to_process.append([r[3], interval])
                    break
                # interval partially within the limit
                else:
                    interval_in_limit = copy.deepcopy(interval)
                    interval_in_limit[r[0]] = (r[2] + 1, interval[r[0]][1])
                    to_process.append([r[3], interval_in_limit])
                    interval[r[0]] = (interval[r[0]][0], r[2])

        else:
            to_process.append([rules[rule_name][-1], interval])

    return sum(prod(e - s + 1 for s, e in interval) for interval in accepted)



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
