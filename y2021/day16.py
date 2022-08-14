from __future__ import annotations
from enum import Enum, IntEnum
from functools import reduce


HexStr = str
PacketBinary = list[str]


def parse_input(filepath) -> str:
    with open(filepath, "r") as f:
        return f.read()


def make_hex_to_binary_map() -> dict[str, str]:
    hexbinmap: dict[str, str] = {}
    with open(r"data/hexbinref.txt", "r") as f:
        for line in f.readlines():
            hex, bin = line.strip().split(" = ")
            hexbinmap[hex] = bin
    return hexbinmap


HEX_BINARY_MAP = make_hex_to_binary_map()


class Converter:
    @staticmethod
    def bin_to_base_10(binary: str) -> int:
        return int(binary, 2)

    @staticmethod
    def hex_to_bin(hex_packet: HexStr) -> list[str]:
        global HEX_BINARY_MAP
        bin_format = []
        for char in hex_packet:
            bin_format.extend([*HEX_BINARY_MAP[char]])
        return bin_format


class TypeID(IntEnum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    IntLiteral = 4
    GreaterThan = 5
    LessThan = 6
    EqualTo = 7


class LenTypeID(str, Enum):
    TotalLenInBits = "0"
    NumOfSubPackets = "1"


class Packet:
    version_length = 3
    type_id_length = 3

    operations = {
        TypeID.Sum: lambda x: sum(x),
        TypeID.Product: lambda x: reduce(lambda a, b: a * b, x),
        TypeID.Minimum: lambda x: min(x),
        TypeID.Maximum: lambda x: max(x),
        TypeID.GreaterThan: lambda x: int(x[0] > x[1]),
        TypeID.LessThan: lambda x: int(x[0] < x[1]),
        TypeID.EqualTo: lambda x: int(x[0] == x[1]),
    }

    def __init__(self, packet: PacketBinary) -> None:
        self.packet: PacketBinary = packet
        self.current_position = 0
        self.version_sum: int = 0
        self.value = None

    def process(self):
        self.value = self.process_subpacket()

    def advance_position(self, n_positions: int = 1) -> None:
        self.current_position += n_positions

    def get_version(self) -> int:
        _version = self.packet[
            self.current_position : self.current_position + self.version_length
        ]
        return Converter.bin_to_base_10("".join(_version))

    def get_typeid(self) -> int:
        _typeid = self.packet[
            self.current_position : self.current_position + self.type_id_length
        ]
        return Converter.bin_to_base_10("".join(_typeid))

    def process_subpacket(self) -> int:
        version: int = self.get_version()
        self.version_sum += version
        self.advance_position(self.version_length)

        typeid: int = self.get_typeid()
        self.advance_position(self.type_id_length)

        if typeid != TypeID.IntLiteral:
            length_type_id = self.packet[self.current_position]
            self.advance_position()
            if length_type_id == LenTypeID.TotalLenInBits:
                return self.process_sub_packet_by_length(typeid)
            elif length_type_id == LenTypeID.NumOfSubPackets:
                return self.process_sub_packet_by_number_of_sub_packets(typeid)
        else:
            return self.process_int_literal()

    def process_int_literal(self) -> int:
        int_list = []
        chunk_len = 5
        first_val = None
        while first_val != "0":
            first_val, *int_chunk = self.packet[
                self.current_position : self.current_position + chunk_len
            ]
            int_list.extend(int_chunk)
            self.advance_position(chunk_len)
        binary_number = "".join(int_list)
        int_literal = Converter.bin_to_base_10(binary_number)
        return int_literal

    def process_sub_packet_by_length(self, procedure, field_len=15):
        n_bits_bin = "".join(
            self.packet[self.current_position : self.current_position + field_len]
        )
        n_bits = Converter.bin_to_base_10(n_bits_bin)

        self.advance_position(field_len)

        position = self.current_position
        end_position = position + n_bits

        vals = []
        while self.current_position < end_position:
            vals.append(self.process_subpacket())
        return self.operations[procedure](vals)

    def process_sub_packet_by_number_of_sub_packets(self, procedure, field_len=11):
        n_sub_packets_bin = "".join(
            self.packet[self.current_position : self.current_position + field_len]
        )
        n_sub_packets = Converter.bin_to_base_10(n_sub_packets_bin)

        self.advance_position(field_len)

        vals = []
        for _ in range(n_sub_packets):
            vals.append(self.process_subpacket())
        return self.operations[procedure](vals)


def part_a():
    fp = r"data/day16.txt"
    hex_packet = parse_input(fp)
    bin_packet = Converter.hex_to_bin(hex_packet)
    packet = Packet(bin_packet)
    packet.process()
    return packet.version_sum


def part_b():
    fp = r"data/day16.txt"
    hex_packet = parse_input(fp)
    bin_packet = Converter.hex_to_bin(hex_packet)
    packet = Packet(bin_packet)
    packet.process()
    return packet.value


if __name__ == "__main__":
    print(part_a())
    print(part_b())
