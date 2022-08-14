def decompress_string_v1(compressed: str) -> str:
    ptr = 0
    decompressed = ""
    while ptr < len(compressed):
        if compressed[ptr] == "(":
            decompression_value = ""
            ptr += 1
            while compressed[ptr] != ")":
                decompression_value += compressed[ptr]
                ptr += 1
            ptr += 1
            subsequent_char_range, n_repeats = decompression_value.split("x")
            subsequent_char_range = int(subsequent_char_range)
            n_repeats = int(n_repeats)
            decompressed += compressed[ptr : ptr + subsequent_char_range] * n_repeats
            ptr += subsequent_char_range
        else:
            decompressed += compressed[ptr]
            ptr += 1
    return decompressed


def decompress_string_v2(compressed: str) -> int:
    ptr = 0
    decompressed_length = 0
    while ptr < len(compressed):
        if compressed[ptr] == "(":
            decompression_value = ""
            ptr += 1
            while compressed[ptr] != ")":
                decompression_value += compressed[ptr]
                ptr += 1
            ptr += 1
            subsequent_char_range, n_repeats = decompression_value.split("x")
            subsequent_char_range = int(subsequent_char_range)
            n_repeats = int(n_repeats)
            decompressed_length += decompress_string_v2(compressed[ptr : ptr + subsequent_char_range]) * n_repeats
            ptr += subsequent_char_range
        else:
            decompressed_length += 1
            ptr += 1
    return decompressed_length



def part_a() -> int:
    with open(r"data/day9.txt", "r") as f:
        text = f.read().strip()
    decompressed_string = decompress_string_v1(text)
    return len(decompressed_string)


def part_a_test() -> None:
    print(decompress_string_v1("ADVENT"))
    print(decompress_string_v1("A(1x5)BC"))
    print(decompress_string_v1("(3x3)XYZ"))
    print(len(decompress_string_v1("A(2x2)BCD(2x2)EFG")))  # 11
    print(len(decompress_string_v1("(6x1)(1x3)A")))  # 6
    print(len(decompress_string_v1("X(8x2)(3x3)ABCY")))  # 18


def part_b() -> int:
    with open(r"data/day9.txt", "r") as f:
        text = f.read().strip()
    return decompress_string_v2(text)


def part_b_test() -> None:
    print(decompress_string_v2("(3x3)XYZ"))  # 9
    print(decompress_string_v2("XABCABCABCABCABCABCY"))  # 20
    print(decompress_string_v2("(27x12)(20x12)(13x14)(7x10)(1x12)A"))  # 241920
    print(decompress_string_v2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"))  # 445


if __name__ == "__main__":
    print(part_a())
    print(part_b())
