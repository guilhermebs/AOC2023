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

    sol_part2 = None
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


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
