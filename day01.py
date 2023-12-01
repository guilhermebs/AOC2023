import os
import time
import re

DIGITS = [str(i) for i in range(10)]
DIGITS_WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def solve():
    input_file_contents = open(os.path.join("input", "day01")).read().rstrip()
    sol_part1 = 0
    for line in input_file_contents.splitlines():
        first_digit = None
        last_digit = None
        for c in line:
            if c in DIGITS:
                if first_digit is None:
                    first_digit = int(c)
                last_digit = int(c)
        print(first_digit, last_digit)
        sol_part1 += 10 * first_digit + last_digit
    print("Part 1:", sol_part1)

    sol_part2 = 0
    regex = re.compile(rf"(?=(\d|{'|'.join(DIGITS_WORDS)}))")
    for line in input_file_contents.splitlines():
        matches = re.findall(regex, line)
        matches_int = [string2int(ds) for ds in matches]
        print(matches, matches_int)
        sol_part2 += 10 * matches_int[0] + matches_int[-1]

    print("Part 2:", sol_part2)

def string2int(ds):
    try:
        return int(ds)
    except ValueError:
        return DIGITS_WORDS.index(ds)

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
