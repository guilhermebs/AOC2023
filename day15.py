import os
import time

EXAMPLE = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

def solve():
    input_file_contents = open(os.path.join("input", "day15")).read().rstrip()
    #input_file_contents = EXAMPLE

    sol_part1 = sum(hash(step) for step in input_file_contents.split(","))
    print("Part 1:", sol_part1)

    boxes = [{} for _ in range(256)]
    for instruction in input_file_contents.split(","):
        if "=" in instruction:
            label, focal = instruction.split("=")
            boxes[hash(label)][label] = int(focal)
        elif instruction.endswith("-"):
            label = instruction[:-1]
            if label in boxes[hash(label)]:
                boxes[hash(label)].pop(label)

    sol_part2 = sum(sum((bn + 1) * (ln + 1) * focal for ln, focal in enumerate(box.values())) for bn, box in enumerate(boxes))
    print("Part 2:", sol_part2)


def hash(input: str):
    result = 0
    for c in input:
        result += ord(c)
        result *= 17
        result %= 256

    return result


if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
