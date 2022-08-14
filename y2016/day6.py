from collections import Counter


def file_io(filename) -> list[str]:
    with open(filename, "r") as f:
        data = f.read().split("\n")
    return data


def part_a() -> str:
    input_file = r"data/day6.txt"
    data = file_io(input_file)
    per_column = [[*v] for v in zip(*data)]
    most_frequent = [Counter(column).most_common(1)[0] for column in per_column]
    answer = ''.join([x[0] for x in most_frequent])
    return answer


def part_b() -> str:
    input_file = r"data/day6.txt"
    data = file_io(input_file)
    per_column = [[*v] for v in zip(*data)]
    least_frequent = [Counter(column).most_common()[-1] for column in per_column]
    answer = ''.join([x[0] for x in least_frequent])
    return answer


if __name__ == '__main__':
    print(part_a())
    print(part_b())
