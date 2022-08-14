IPADDRESS = str


def is_autonomous_bridge_bypass_annotation(four_char_str: str) -> bool:
    if all(
        [
            four_char_str[0] == four_char_str[3],
            four_char_str[1] == four_char_str[2],
            four_char_str[0] != four_char_str[1],
        ]
    ):
        return True
    return False


def is_area_broadcast_accessor(three_char_str: str) -> bool:
    if all(
        [three_char_str[0] == three_char_str[2], three_char_str[0] != three_char_str[1]]
    ):
        return True
    return False


def supports_transport_layer_snooping(ip_address: IPADDRESS) -> bool:
    abba_found = False
    hypernet_sequence_flag = False

    for i, char in enumerate(ip_address[:-3]):
        if char == "[":
            hypernet_sequence_flag = True
            continue
        if char == "]":
            hypernet_sequence_flag = False
            continue
        if is_autonomous_bridge_bypass_annotation(ip_address[i : i + 4]):
            if hypernet_sequence_flag:
                return False
            else:
                abba_found = True

    return abba_found


def supports_super_secret_listening(ip_address: IPADDRESS) -> bool:
    area_broadcast_accessors = []
    byte_allocation_blocks = []
    hypernet_sequence_flag = False

    for i, char in enumerate(ip_address[:-2]):
        if char == "[":
            hypernet_sequence_flag = True
            continue
        if char == "]":
            hypernet_sequence_flag = False
            continue

        candidate_string = ip_address[i : i + 3]

        if is_area_broadcast_accessor(candidate_string):
            if hypernet_sequence_flag:
                byte_allocation_blocks.append(candidate_string)
            else:
                area_broadcast_accessors.append(candidate_string)

    for aba in area_broadcast_accessors:
        bab = aba[1] + aba[0] + aba[1]
        if bab in byte_allocation_blocks:
            return True
    return False


def part_a() -> int:
    tls_support_count = 0
    with open(r"data/day7.txt") as f:
        for line in f.readlines():
            ip_address = line.strip()
            if supports_transport_layer_snooping(ip_address):
                tls_support_count += 1
    return tls_support_count


def part_b() -> int:
    ssl_support_count = 0
    with open(r"data/day7.txt") as f:
        for line in f.readlines():
            ip_address = line.strip()
            if supports_super_secret_listening(ip_address):
                ssl_support_count += 1
    return ssl_support_count


if __name__ == "__main__":
    print(part_a())
    print(part_b())
