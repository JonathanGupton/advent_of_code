from ast import literal_eval
from collections import deque


def parse_input(filepath):
    with open(filepath, "r") as f:
        snailfish_numbers = [
            literal_eval(line.strip()) for line in f.readlines()
        ]
    return snailfish_numbers


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


def is_list(snailfish_number) -> bool:
    return isinstance(snailfish_number, list)


def explode(snailfish_number):
    num = snailfish_number.copy()
    left = 0
    right = 0
    path = []

    def _set_index(snailfish, path):
        pass

    def _explode(snailfish_number, depth=0):
        nonlocal num, left, right
        match (is_list(snailfish_number[0]), is_list(snailfish_number[1])):
            case (True, True):
                _explode(snailfish_number[0], depth+1)
            case (True, False):
                _explode(snailfish_number[0], depth+1)
            case (False, True):
                _explode(snailfish_number[1], depth+1)
            case (False, False):
                left, right = snailfish_number[0], snailfish_number[1]
                print(left, right, depth, sep="\t")

    _explode(snailfish_number, depth=0)


def split(snailfish_number):
    return snailfish_number


# fp = r"data/day18.txt"
# data = parse_input(fp)
# explode(data[0])

to_explode = [[[[[9, 8], 1], 2], 3], 4]
exploded = explode(to_explode)
# print(explode(to_explode) == "[[[[0, 9], 2], 3], 4]")
#
# to_explode = "[7, [6, [5, [4, [3, 2]]]]]"
# print(explode(to_explode) == "[7, [6, [5, [7, 0]]]]")
#
# to_explode = "[[6, [5, [4, [3, 2]]]], 1]"
# print(explode(to_explode) == "[[6, [5, [7, 0]]], 3]")
#
# to_explode = "[[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]"
# print(explode(to_explode) == "[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]")
#
# to_explode = "[[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]"
# print(explode(to_explode) == "[[3, [2, [8, 0]]], [9, [5, [7, 0]]]]")
