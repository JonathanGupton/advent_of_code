from functools import reduce


def file_io(source):
    with open(source, 'r') as f:
        return f.read()


def clean(s):
    s = s[1:-1]  # remove outer quotes
    n = 0
    ptr = 0
    while ptr < len(s):
        if s[ptr] == '\\':
            if s[ptr + 1] == "x":
                n += 1
                ptr += 4
            elif s[ptr + 1] in '\\"':
                n += 1
                ptr += 2
        else:
            n += 1
            ptr += 1

    return n



def unclean(s):
    s = s[1:-1]  # remove outer quotes
    n = 6  # backslash for each "
    ptr = 0
    while ptr < len(s):
        if s[ptr] == '\\':
            if s[ptr + 1] == "x":
                n += 5
                ptr += 4
            elif s[ptr + 1] in '\\"':
                n += 4
                ptr += 2
        else:
            n += 1
            ptr += 1

    return n



def part_a(file_loc):
    d = file_io(file_loc)
    d = d.split('\n')
    total_length = reduce(lambda a, b: a + len(b), d, 0)
    string_length = reduce(lambda a, b: a + clean(b), d, 0)
    code_minus_memory = total_length - string_length
    return code_minus_memory


def part_b(file_loc):
    d = file_io(file_loc)
    d = d.split('\n')
    total_length = reduce(lambda a, b: a + len(b), d, 0)
    unclean_total_length = reduce(lambda a, b: a + unclean(b), d, 0)
    return unclean_total_length - total_length


if __name__ == '__main__':
    file_in = r"data\day08.txt"
    # file_in = r"data\day08_example_a.txt"
    print(part_a(file_in))
    print(part_b(file_in))
