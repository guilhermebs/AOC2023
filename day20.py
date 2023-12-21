import math
import time
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
import os

EXAMPLE1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".strip()

EXAMPLE2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".strip()


def solve():
    input_file_contents = open(os.path.join("input", "day20")).read().rstrip()
    #input_file_contents = EXAMPLE2

    modules: dict[str, Module] = {}
    for line in input_file_contents.splitlines():
        if line.startswith("%"):
            module = FlipFlopModule.from_string(line)
        elif line.startswith("&"):
            module = ConjunctionModule.from_string(line)
        else:
            module = Module.from_string(line)
        modules[module.name] = module

    for m in modules.values():
        if isinstance(m, ConjunctionModule):
            m.add_initial_state(modules)

    modules_init = deepcopy(modules)

    counts = {Signal.LOW: 0, Signal.HIGH: 0}
    for _ in range(1000):
        push_count = push_button(modules)
        counts[Signal.LOW] += push_count[Signal.LOW]
        counts[Signal.HIGH] += push_count[Signal.HIGH]

    sol_part1 = counts[Signal.LOW] * counts[Signal.HIGH]
    print("Part 1:", sol_part1)

    modules = modules_init
    #while not activate_rx(modules):
    #    if count % 10000 == 0:
    #        print(count)
    #    count += 1

    sol_part2 = solve_pt2(modules)
    print("Part 2:", sol_part2)


def solve_pt2(modules):
    high_inputs = {k: []  for k in modules['jz'].prev_inputs.keys()}

    for n_presses in range(1, 100000):
        to_process = deque([("broadcaster", Signal.LOW, None)])
        while len(to_process) > 0:
            dest, signal, source = to_process.pop()
            if dest in modules:
                for s in modules[dest].handle_signal(signal, source):
                    if dest == "jz":
                        for k, v in modules["jz"].prev_inputs.items():
                            if v == Signal.HIGH and n_presses not in high_inputs[k]:
                                high_inputs[k].append(n_presses)
                    to_process.appendleft(s)
    periods = {k: [h1 - h0 for h0, h1 in zip(v, v[1:])] for k, v in high_inputs.items()}
    print(periods)
    return math.lcm(*[p[0] for p in periods.values()])


class Signal(Enum):
    LOW = 1
    HIGH = 2


@dataclass
class Module:
    name: str
    destinations: list[str]

    @classmethod
    def from_string(cls, string: str):
        name, destinations = string.split(" -> ")
        return cls(
            name=name.strip(" &%"),
            destinations=destinations.split(", "),
        )

    def handle_signal(self, signal: Signal, source: str):
        return [(dest, signal, self.name) for dest in self.destinations]

    #def __repr__(self) -> str:
    #    return f"{self.name} -> " + ",".join(self.destinations)


@dataclass
class FlipFlopModule(Module):
    state: bool = False

    def handle_signal(self, signal: Signal, source: str):
        if signal == Signal.HIGH:
            return []
        elif self.state:
            new_signal = Signal.LOW
        else:
            new_signal = Signal.HIGH

        self.state = not self.state
        return [(dest, new_signal, self.name) for dest in self.destinations]


@dataclass
class ConjunctionModule(Module):
    prev_inputs: dict[str, Signal] = field(default_factory=dict)

    def add_initial_state(self, modules):
        for m in modules.values():
            if self.name in m.destinations:
                self.prev_inputs[m.name] = Signal.LOW

    def handle_signal(self, signal: Signal, source: str):
        self.prev_inputs[source] = signal
        if all(s == Signal.HIGH for s in self.prev_inputs.values()):
            new_signal = Signal.LOW
        else:
            new_signal = Signal.HIGH

        return [(dest, new_signal, self.name) for dest in self.destinations]


def push_button(modules):
    counts = {Signal.LOW: 0, Signal.HIGH: 0}
    to_process = deque([("broadcaster", Signal.LOW, None)])

    while len(to_process) > 0:
        dest, signal, source = to_process.pop()
        counts[signal] += 1
        if dest in modules:
            for s in modules[dest].handle_signal(signal, source):
                to_process.appendleft(s)

    return counts




if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
