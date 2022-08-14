from collections import deque
from typing import Sequence


IP = int
DisallowedRange = tuple[IP, IP]
DisallowedRangeIterable = Sequence[DisallowedRange]


def file_io(filepath) -> deque[DisallowedRange]:
    with open(filepath, "r") as f:
        firewall_data: list[DisallowedRange] = []
        for line in f.readlines():
            l_val, r_val = line.split("-")
            min_ip_range: IP = int(l_val)
            max_ip_range: IP = int(r_val)
            ip_range: DisallowedRange = (min_ip_range, max_ip_range)
            firewall_data.append(ip_range)
    firewall_data.sort(key=lambda x: x[0])
    return deque(firewall_data)


def consolidate_ranges(disallowed: DisallowedRangeIterable) -> deque[DisallowedRange]:
    if not isinstance(disallowed, deque):
        disallowed = deque(disallowed)

    new_disallowed_iterable = deque()
    while disallowed:
        current = disallowed.popleft()
        current_min = min(current)
        current_max = max(current)
        if not disallowed or min(disallowed[0]) >= (current_max + 1):
            new_disallowed_iterable.append((current_min, current_max))
            continue
        else:
            while disallowed and min(disallowed[0]) <= (current_max + 1):
                next_range = disallowed.popleft()
                if max(next_range) <= current_max:
                    continue
                else:
                    current_max = max(next_range)
            new_disallowed_iterable.append((current_min, current_max))
    return new_disallowed_iterable


def total_allowed_ip_address(
    disallowed: deque[DisallowedRange], min_ip: IP = 0, max_ip: IP = 4294967295
) -> int:
    if not disallowed:
        return 0
    allowed = 0
    current_ip = disallowed.popleft()
    if min(current_ip) > min_ip:
        allowed += min(current_ip) - min_ip - 1
    while disallowed:
        next_ip = disallowed.popleft()
        allowed +=  min(next_ip) - max(current_ip) - 1
        current_ip = next_ip
    if max(current_ip) < max_ip:
        allowed += max_ip - max(current_ip) - 1
    return allowed


def part_a():
    fp = r"data/day20.txt"
    data = file_io(fp)
    new_ranges = consolidate_ranges(data)
    return max(new_ranges[0]) + 1


def part_b():
    fp = r"data/day20.txt"
    data = file_io(fp)
    new_ranges = consolidate_ranges(data)
    return total_allowed_ip_address(new_ranges, 0, 23923783)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
