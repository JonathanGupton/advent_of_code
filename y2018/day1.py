

def part_a(file_location):
    pattern = r"-?\d+"
    with open(file_location, "r") as f:
        data = [int(val) for val in f]
    return sum(data)


def part_b(file_location):

    frequency = 0
    found_frequencies: set[int] = {frequency}
    while True:
        with open(file_location, "r") as f:
            for val in f:
                frequency += int(val)
                if frequency in found_frequencies:
                    return frequency
                else:
                    found_frequencies.add(frequency)


if __name__ == '__main__':
    pass