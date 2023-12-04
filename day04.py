import os
import time
import re


def solve():
    input_file_contents = open(os.path.join("input", "day04")).read().rstrip()
    cards = []
    sol_part1 = 0
    for line in input_file_contents.splitlines():
        match = re.match(r"Card\s+\d+:((?:\s+\d+)+)\s+\|((?:\s+\d+)+)", line)
        winning_numbers = set(int(n) for n in match.group(1).replace("  ", " ").strip().split(" "))
        card_numbers = set(int(n) for n in match.group(2).replace("  ", " ").strip().split(" "))
        n_matches = len(winning_numbers.intersection(card_numbers))
        cards.append((winning_numbers, card_numbers, n_matches))
        if n_matches > 0:
            sol_part1 += 2**(n_matches - 1)

    print("Part 1:", sol_part1)

    cards_have = [1] * len(cards)
    for i, (_, _, n_matches) in enumerate(cards):
        number_of_cards = cards_have[i]
        for j in range(n_matches):
            cards_have[i + j + 1] += number_of_cards

    sol_part2 = sum(cards_have)
    print("Part 2:", sol_part2)


def recursive_win(cards, cards_have):
    f



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
