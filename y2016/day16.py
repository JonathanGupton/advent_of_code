

def generate_random_data(initial_state: str) -> str:
    b = "".join(["1" if char == "0" else "0" for char in initial_state[::-1]])
    return initial_state + "0" + b


def fill_disk_space(disk_value: str, disk_space: int) -> str:
    while len(disk_value) < disk_space:
        disk_value = generate_random_data(initial_state=disk_value)
    return disk_value[:disk_space]


def grouper(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def compress_data(input_data: str) -> str:
    return ''.join("1" if group[0] == group[1] else "0" for group in grouper(input_data, 2))


def calculate_checksum(data: str) -> str:
    while len(data) % 2 == 0:
        data = compress_data(data)
    return data


def part_a():
    pseudo_data = fill_disk_space("01000100010010111", 272)
    checksum = calculate_checksum(pseudo_data)
    return checksum

def part_b():
    pseudo_data = fill_disk_space("01000100010010111", 35651584)
    checksum = calculate_checksum(pseudo_data)
    return checksum


# print(generate_random_data("1"))
# print(generate_random_data("0"))
# print(generate_random_data("11111"))
# print(generate_random_data("111100001010"))
#
#
# print(generate_random_data("1") == "100")
# print(generate_random_data("0") == "001")
# print(generate_random_data("11111") == "11111000000")
# print(generate_random_data("111100001010") == "1111000010100101011110000")
# print(fill_disk_space("10000", 20) == "10000011110010000111")
# print(calculate_checksum("10000011110010000111") == "01100")

if __name__ == '__main__':
    print(part_a())
    print(part_b())
