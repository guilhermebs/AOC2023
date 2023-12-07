import os
import time

CARDS_MAPPING = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
CARDS_MAPPING_PT2 = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, 'J': 1}


def solve():
    input_file_contents = open(os.path.join("input", "day07")).read().rstrip()
    hands = sorted([Hand(line) for line in input_file_contents.splitlines()])
    sol_part1 = sum((i+1) * h.bid for i, h in enumerate(hands))

    print("Part 1:", sol_part1)

    hands = sorted([HandPt2(line) for line in input_file_contents.splitlines()])
    sol_part2 = sum((i+1) * h.bid for i, h in enumerate(hands))
    print("Part 2:", sol_part2)


class Hand:
    def __init__(self, line: str):
        cards_str, bid = line.split(" ")
        self.cards = [CARDS_MAPPING[c] if c in CARDS_MAPPING else int(c) for c in cards_str]
        self.bid = int(bid)
        repetitions = sorted([(self.cards.count(c), c) for c in set(self.cards)], reverse=True)
        if repetitions[0][0] == 1:
            self.hand_type = 1
        elif repetitions[0][0] == 2 and repetitions[1][0] == 1:
            self.hand_type = 2
        elif repetitions[0][0] == 2 and repetitions[1][0] == 2:
            self.hand_type = 3
        elif repetitions[0][0] == 3 and repetitions[1][0] == 1:
            self.hand_type = 4
        elif repetitions[0][0] == 3 and repetitions[1][0] == 2:
            self.hand_type = 5
        elif repetitions[0][0] == 4:
            self.hand_type = 6
        elif repetitions[0][0] == 5:
            self.hand_type = 7
        else:
            raise ValueError("Something went wrong!")

    def __repr__(self):
        return f"(cards: {self.cards}, bid: {self.bid})"

    def __gt__(self, other):
        if self.hand_type == other.hand_type:
            return self.cards > other.cards
        else:
            return self.hand_type > other.hand_type


class HandPt2:
    def __init__(self, line: str):
        cards_str, bid = line.split(" ")
        self.cards = [CARDS_MAPPING_PT2[c] if c in CARDS_MAPPING_PT2 else int(c) for c in cards_str]
        jokers = self.cards.count(1)
        repetitions = sorted([(self.cards.count(c), c) for c in set(self.cards)], reverse=True)
        if len(repetitions) > 1:
            if repetitions[0][1] == 1:
                repetitions[1], repetitions[0] = repetitions[0], repetitions[1]
            repetitions[0] = (repetitions[0][0] + jokers, repetitions[0][1])
            # remove the joker
            repetitions = [r for r in repetitions if r[1] != 1]

        self.bid = int(bid)
        # All joker copies become copies of the most frequent card
        if repetitions[0][0] == 1:
            self.hand_type = 1
        elif repetitions[0][0] == 2 and repetitions[1][0] == 1:
            self.hand_type = 2
        elif repetitions[0][0] == 2 and repetitions[1][0] == 2:
            self.hand_type = 3
        elif repetitions[0][0] == 3 and repetitions[1][0] == 1:
            self.hand_type = 4
        elif repetitions[0][0] == 3 and repetitions[1][0] == 2:
            self.hand_type = 5
        elif repetitions[0][0] == 4:
            self.hand_type = 6
        elif repetitions[0][0] == 5:
            self.hand_type = 7
        else:
            raise ValueError("Something went wrong!")

    def __repr__(self):
        return f"(cards: {self.cards}, bid: {self.bid})"

    def __gt__(self, other):
        if self.hand_type == other.hand_type:
            return self.cards > other.cards
        else:
            return self.hand_type > other.hand_type



if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
