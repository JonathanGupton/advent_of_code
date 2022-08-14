from ast import literal_eval
from collections import deque
from itertools import combinations
from math import ceil

def parse_input(filepath):
    with open(filepath, "r") as f:
        snailfish_numbers = [line.strip() for line in f.readlines()]
    return snailfish_numbers


def explode(num):
    new_num: deque[str] = deque()
    depth = -1
    num_len = len(num)
    ptr = 0
    exploded = False
    right_applied = False
    right = None
    while ptr < num_len:
        if num[ptr] == "[":
            new_num.append(num[ptr])
            depth += 1
            ptr += 1
        elif num[ptr] == "]":
            if depth >= 4 and not exploded:
                exploded = True
                temp = deque()
                while new_num[-1] != "[":
                    temp.appendleft(new_num.pop())
                new_num.pop()
                temp = ''.join(temp).split(",")
                left, right = int(temp[0]), int(temp[1])
                # Iterate left and find a number to add left to??
                new_num_left = deque()
                while new_num:
                    left_val = new_num.pop()
                    if left_val.isnumeric():
                        left_val = str(int(left) + int(left_val))
                        new_num.append(left_val)
                        break
                    else:
                        new_num_left.appendleft(left_val)
                new_num.extend(new_num_left)
                new_num.append("0")
            else:
                new_num.append(num[ptr])
            ptr += 1
            depth -= 1
        elif num[ptr] == ",":
            new_num.append(num[ptr])
            ptr += 1
        else:
            inner_num = []
            while num[ptr].isnumeric():
                inner_num.append(num[ptr])
                ptr += 1
            next_num = "".join(inner_num)
            if right and not right_applied:
                next_num = str(int(next_num) + int(right))
                right_applied = True
            new_num.append(next_num)
    return "".join(new_num)


def _test_to_explode():
    to_explode = "[[[[[9,8],1],2],3],4]"
    print(explode(to_explode) == "[[[[0,9],2],3],4]")

    to_explode = "[7,[6,[5,[4,[3,2]]]]]"
    print(explode(to_explode) == "[7,[6,[5,[7,0]]]]")

    to_explode = "[[6,[5,[4,[3,2]]]],1]"
    print(explode(to_explode) == "[[6,[5,[7,0]]],3]")

    to_explode = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
    print(explode(to_explode) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

    to_explode = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    print(explode(to_explode) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")


def split(num) -> str:
    new_num: deque[str] = deque()
    num_len = len(num)
    ptr = 0
    num_split = False
    while ptr < num_len:
        if num[ptr] in "[,]":
            new_num.append(num[ptr])
            ptr += 1
        else:
            inner_num = []
            while num[ptr].isnumeric():
                inner_num.append(num[ptr])
                ptr += 1
            next_num = "".join(inner_num)
            if not num_split and int(next_num) >= 10:
                next_num = int(next_num)
                left = next_num // 2
                right = ceil(next_num / 2)
                new_num.append(f"[{str(left)},{str(right)}]")
                num_split = True
            else:
                new_num.append(next_num)
    return "".join(new_num)


def _test_split():
    print(split("[10,1]") == "[[5,5],1]")
    print(split("[11,1]") == "[[5,6],1]")
    print(split("[12,1]") == "[[6,6],1]")
    print(split("[5,5]") == "[5,5]")


def reduce(num):
    while True:
        exploded_num = explode(num)
        if exploded_num != num:
            num = exploded_num
            continue
        split_num = split(num)
        if split_num != num:
            num = split_num
            continue
        return num


def add(num1, num2):
    new_num = f"[{num1},{num2}]"
    reduced_num = reduce(new_num)
    return reduced_num


def _test_add():
    l = "[[[[4,3],4],4],[7,[[8,4],9]]]"
    r = "[1,1]"
    n = add(l, r)
    out = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    print(n == out)


def _test_part_a1():
    fp = r"data/day18_example_a.txt"
    data = parse_input(fp)
    l, *r = data
    l = add(l, r[0])
    print(f"1. {l == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'}")

    l = add(l, r[1])
    print(f"2. {l == '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'}")

    l = add(l, r[2])
    print(f"3. {l == '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]'}")

    l = add(l, r[3])
    print(f"4. {l == '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]'}")

    l = add(l, r[4])
    print(f"5. {l == '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]'}")

    l = add(l, r[5])
    print(f"6. {l == '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]'}")

    l = add(l, r[6])
    print(f"7. {l == '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]'}")

    l = add(l, r[7])
    print(f"8. {l == '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]'}")

    l = add(l, r[8])
    print(f"9. {l == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'}")


def _test_part_a2():
    fp = r"data/day18_example_a.txt"
    data = parse_input(fp)
    l, *r = data
    for n in r:
        l = add(l, n)
    print(l == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")


def calculate_magnitude(num):
    if isinstance(num,str):
        num = literal_eval(num)
    match (isinstance(num[0], int), isinstance(num[1], int)):
        case (True, True):
            return num[0] * 3 + num[1] * 2
        case (True, False):
            return 3 * num[0] + 2 * calculate_magnitude(num[1])
        case (False, True):
            return 3 * calculate_magnitude(num[0]) + 2 * num[1]
        case (False, False):
            return 3 * calculate_magnitude(num[0]) + 2 * calculate_magnitude(num[1])

def _test_magnitude():
    print(calculate_magnitude([9,1]) == 29)
    print(calculate_magnitude([[9,1],[1,9]]) == 129)
    print(calculate_magnitude([[1,2],[[3,4],5]]) == 143)
    print(calculate_magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384)
    print(calculate_magnitude([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445)
    print(calculate_magnitude([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791)
    print(calculate_magnitude([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137)
    print(calculate_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488)


def _test_part_a3():
    fp = r"data/day18_example_b.txt"
    data = parse_input(fp)
    l, *r = data
    for n in r:
        l = add(l, n)
    m = calculate_magnitude(l)
    print(m == 4140)


def _test_part_b():
    fp = r"data/day18_example_b.txt"
    data = parse_input(fp)
    max_magnitude = float("-inf")
    for a, b in combinations(data, 2):
        c = calculate_magnitude(add(a, b))
        d = calculate_magnitude(add(b, a))
        max_magnitude = max(max_magnitude, c, d)
    print(int(max_magnitude) == 3993)


def part_a():
    fp = r"data/day18.txt"
    data = parse_input(fp)
    l, *r = data
    for n in r:
        l = add(l, n)
    m = calculate_magnitude(l)
    return m


def part_b():
    fp = r"data/day18.txt"
    data = parse_input(fp)
    data = parse_input(fp)
    max_magnitude = float("-inf")
    for a, b in combinations(data, 2):
        c = calculate_magnitude(add(a, b))
        d = calculate_magnitude(add(b, a))
        max_magnitude = max(max_magnitude, c, d)
    return max_magnitude


if __name__ == '__main__':
    print(part_a())
    print(part_b())