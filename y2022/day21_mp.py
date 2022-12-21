import multiprocessing
from functools import cache
from typing import Callable
import operator
import psutil


Monkey = str
MonkeyMap = dict[Monkey, list[Monkey] | int]
MonkeyOps = dict[Monkey, Callable[[int, int], int]]

add = operator.add
sub = operator.sub
mul = operator.mul
div = operator.floordiv
eq = operator.eq

ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "=": eq,
}


def parse_file(
    filepath,
) -> tuple[MonkeyMap, MonkeyOps]:
    global ops
    monkeys: MonkeyMap = {}
    monkey_ops: MonkeyOps = {}
    with open(filepath, "r") as f:
        for line in f.readlines():
            match line.split():
                case [monkey, number]:
                    monkeys[monkey[:4]] = int(number)
                case [monkey, left_monkey, op, right_monkey]:
                    monkeys[monkey[:4]] = [left_monkey, right_monkey]
                    monkey_ops[monkey[:4]] = ops[op]

    return monkeys, monkey_ops


def part_one(filepath):
    monkeys, monkey_ops = parse_file(filepath)

    @cache
    def dfs(monkey) -> int:
        if type(monkeys[monkey]) is int:
            return monkeys[monkey]
        left_monkey, right_monkey = monkeys[monkey]
        return monkey_ops[monkey](dfs(left_monkey), dfs(right_monkey))

    return dfs("root")


def calculate(monkeys, monkey_ops):
    @cache
    def dfs(monkey) -> int:
        if type(monkeys[monkey]) is int:
            return monkeys[monkey]
        left_monkey, right_monkey = monkeys[monkey]
        return monkey_ops[monkey](dfs(left_monkey), dfs(right_monkey))
    lm, rm = monkeys["root"]
    return monkey_ops["root"](dfs(lm), dfs(rm))


def mp_calculate(monkeys, monkey_ops, start, multiple, return_dict, run):
    while run.is_set():
        monkeys["humn"] = start
        while calculate(monkeys, monkey_ops) is False:
            monkeys["humn"] += multiple
        return_dict[start] = monkeys["humn"]
        run.clear()


def mp_part_two(filepath) -> int:
    monkeys, monkey_ops = parse_file(filepath)
    monkey_ops["root"] = ops["="]
    processes = []
    manager = multiprocessing.Manager()
    return_code = manager.dict()
    run = manager.Event()
    run.set()
    n_cpus = multiprocessing.cpu_count()
    for i in range(n_cpus):
        mp_monkeys = dict(monkeys)
        process = multiprocessing.Process(
            target=mp_calculate, args=(mp_monkeys, monkey_ops, i, n_cpus, return_code, run)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(return_code.values())




def part_two(filepath) -> int:
    monkeys, monkey_ops = parse_file(filepath)
    monkey_ops["root"] = ops["="]
    monkeys["humn"] = 0
    while calculate(monkeys, monkey_ops) is False:
        monkeys["humn"] += 1

    return monkeys["humn"]


if __name__ == "__main__":
    data = r"C:\Users\Emily\PycharmProjects\advent_of_code\y2022\data\day21.txt"
    example = (
        r"C:\Users\Emily\PycharmProjects\advent_of_code\y2022\data\day21_example.txt"
    )
    print(part_one(example))  # 152
    print(part_one(data))  # 169525884255464
    # print(part_two(example)) # 301
    # print(part_two(data))  #
    mp_part_two(example)
