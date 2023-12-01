import os
import argparse
import requests
from datetime import datetime
from textwrap import dedent

COOKIE = open("COOKIE").read()

INPUT_DIR = "input"
INPUT_FILE_FORMATTER = "day{day:02d}"

SCRIPTS_DIR = "."
SCRIPT_FILE_FORMATTER = "day{day:02d}.py"


def download_input(year, day):
    if not os.path.isdir(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": COOKIE},
        headers={"User-Agent": "github.com/guilhermebs/AOC2022 by guilhermebs"}
    )
    response.raise_for_status()

    with open(os.path.join(INPUT_DIR, INPUT_FILE_FORMATTER.format(day=day)), 'w') as f:
        f.write(response.content.decode())


def prepare_script(day):
    if not os.path.isdir(SCRIPTS_DIR):
        os.mkdir(SCRIPTS_DIR)
    
    fn_input = INPUT_FILE_FORMATTER.format(day=day)

    script = dedent(f"""
    import os
    import time


    def solve():
        input_file_contents = open(os.path.join("{INPUT_DIR}", "{fn_input}")).read().rstrip()

        sol_part1 = None
        print("Part 1:", sol_part1)

        sol_part2 = None
        print("Part 2:", sol_part2)


    if __name__ == "__main__":
        start = time.time()
        solve()
        print(f"Run time: {{time.time() - start:.3f}}s")
    """)[1:]

    fn_script = os.path.join(SCRIPTS_DIR, SCRIPT_FILE_FORMATTER.format(day=day))

    # This here is to avoid ruining the day's work!
    if os.path.exists(fn_script):
        raise ValueError(f"Script {fn_script} already exists!")
    
    with open(fn_script, "w") as f:
       f.write(script) 

def parse_args():
    parser = argparse.ArgumentParser(description='Download input and prepare script for AoC puzzle')
    parser.add_argument('--year', default=datetime.today().year, type=int,
                        help='Year of puzzle')
    parser.add_argument('--day', default=datetime.today().day, type=int,
                        help='Day of puzzle')
    return parser.parse_args() 


if __name__ == "__main__":
    args = parse_args()
    download_input(args.year, args.day)
    prepare_script(args.day)
    os.system(f"open https://adventofcode.com/{args.year}/day/{args.day} &")
