"""Day 7 2015 solution"""
from functools import cache
from ctypes import c_ushort


def convert_to_int(val):
    try:
        val = int(val)
    except ValueError:
        pass
    return val


class Circuit:
    BITWISE = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "LSHIFT": lambda x, y: x << y,
        "RSHIFT": lambda x, y: x >> y,
        "NOT": lambda x: c_ushort(~x).value,
    }

    def __init__(self, connections):
        self.wires = {}
        self.process_connections(connections)

    def process_connections(self, connections):
        for line in connections:
            signal, wire = line.split(" -> ")
            wire = wire.strip()
            signal = signal.split(" ")
            if len(signal) == 1:
                self.wires[wire] = convert_to_int(signal[0])
            elif len(signal) == 2:
                if signal[0] == "NOT":
                    self.wires[wire] = ("NOT", signal[1])
            elif len(signal) == 3:
                operator = signal[1]
                left = convert_to_int(signal[0])
                right = convert_to_int(signal[2])
                self.wires[wire] = (operator, left, right)

    @cache
    def signal(self, wire):
        if isinstance(wire, int):
            return wire
        if isinstance(self.wires[wire], int):
            return self.wires[wire]
        if len(self.wires[wire]) == 1:
            return self.signal(self.wires[wire])
        return self.BITWISE[self.wires[wire][0]](
            *[self.signal(connection) for connection in self.wires[wire][1:]]
        )


def file_io(file_location):
    with open(file_location, "r") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    # f = r"data\day07_example_a.txt"
    f = r"data\day07.txt"
    data = file_io(f)
    c = Circuit(data)
    c.wires["b"] = 16076
    print(c.signal("lx"))
    # for k in c.wires:
    #     print(f"{k}:  {c.signal(k)}")
    # print(c.signal('a'))
    # print(c.signal('m'))
