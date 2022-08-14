class Reindeer:
    def __init__(self, name, fly_speed, fly_time, rest_time):
        self.name = name
        self.fly_speed = fly_speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self._cycle_time = fly_time + rest_time
        self._cycle_distance = self.fly_speed * self.fly_time
        self.position = 0
        self.time = 0

    def __str__(self):
        return f"{self.name} can fly {self.speed} km/s for {self.fly_time}, but then must rest for {self.rest_time} seconds."

    def __repr__(self):
        return f"Reindeer(name={self.name}, fly_speed={self.fly_speed}, fly_time={self.fly_time}, rest_time={self.rest_time}"

    def increment_position(self):
        self.time += 1
        self.position = self.calculate_distance(self.time)

    def calculate_distance(self, time):
        q, r = divmod(time, self._cycle_time)
        remainder = self._cycle_distance if r > self.fly_time else self.fly_speed * r
        return q * self._cycle_distance + remainder


def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split("\n")

def part_a():
    f = r"data\day14.txt"
    data = file_io(f)
    reindeer = {}
    for line in data:
        line = line.split(" ")
        name = line[0]
        fly_speed = int(line[3])
        fly_time = int(line[6])
        rest_time = int(line[13])
        reindeer[name] = Reindeer(name, fly_speed, fly_time, rest_time)
    print(max([reindeer[k].calculate_distance(2503) for k in reindeer]))



def part_b():
    # f = r"data\day14.txt"
    f = r"data\day14_example_a.txt"
    data = file_io(f)
    reindeer = {}
    for line in data:
        line = line.split(" ")
        name = line[0]
        fly_speed = int(line[3])
        fly_time = int(line[6])
        rest_time = int(line[13])
        reindeer[name] = Reindeer(name, fly_speed, fly_time, rest_time)
    points = {name: 0 for name in reindeer}
    for _ in range(1000):
        for r in reindeer:
            reindeer[r].increment_position()
        max_pos = max([reindeer[r].position for r in reindeer])
        for r in reindeer:
            if reindeer[r].position == max_pos:
                points[r] += 1
    print(max(*points.values()))


part_a()
part_b()
#
# # f = r"data\day14_example_a.txt"
# f = r"data\day14.txt"
# data = file_io(f)
# reindeer = {}
# for line in data:
#     line = line.split(" ")
#     name = line[0]
#     fly_speed = int(line[3])
#     fly_time = int(line[6])
#     rest_time = int(line[13])
#     reindeer[name] = Reindeer(name, fly_speed, fly_time, rest_time)
# print(max([reindeer[k].calculate_distance(2503) for k in reindeer]))