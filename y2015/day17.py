from collections import Counter


def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split("\n")


def store(volume, containers, trail=()):
    global trails
    combinations = 0
    if sum(containers) < volume:
        return combinations
    for i in range(len(containers)):
        if containers[i] == volume:
            trail_append = trail + (containers[i],)
            trails.append(trail_append)
            combinations += 1
            continue
        else:
            combinations += store(volume - containers[i], containers[i+1:], trail + (containers[i],))
    return combinations



f = r"data\day17.txt"
target_volume = 150
trails = []
bottles = tuple(sorted([int(i) for i in file_io(f)], reverse=True))
total_combinations = store(target_volume, bottles)
c = Counter([len(t) for t in trails])

print(total_combinations)
print(c[min(c.keys())])
