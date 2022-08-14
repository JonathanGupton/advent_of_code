from timeit import default_timer as timer
from collections import defaultdict

lines = str()
with open(r'data/day14.txt') as f:
    lines = [n.strip() for n in f.readlines()]




def day14Main(lines, numSteps):
    poly = lines[0]
    reactions = {}
    for line in lines:
        if len(line) > 0 and line[3] == '-': reactions[line[:2]] = line[-1]

    pairCount = defaultdict(int)

    for i in range(len(poly) - 1):
        currentPair = poly[i:i + 2]
        if not currentPair in pairCount:
            pairCount[currentPair] = 1
        else:
            pairCount[currentPair] += 1

    # last letter never changes
    last = poly[-1]

    for i in range(numSteps):
        newPairCount = defaultdict(int)

        for pair in pairCount:
            if pair in reactions:
                newPairs = (pair[0] + reactions[pair], reactions[pair] + pair[1])
                for newPair in newPairs:
                    newPairCount[newPair] += pairCount[pair]
            else:
                newPairCount[pair] += pairCount[pair]
        pairCount = newPairCount

    charCount = defaultdict(int)
    for pair in pairCount:
        charCount[pair[0]] += pairCount[pair]

    charCount[last] += 1

    mx = 0
    mn = 1000000000000000000000
    for c in charCount:
        mx = max(charCount[c], mx)
        mn = min(charCount[c], mn)

    return int(mx - mn)


def part1(lines):
    return day14Main(lines, 10)


def part2(lines):
    return day14Main(lines, 40)


start = timer()
p1 = part1(lines)
end = timer()
print("Part 1:", p1)
print("Time (msec):", (end - start) * 1000)
print()

start = timer()
p2 = part2(lines)
end = timer()
print("Part 2:", p2)
print("Time (msec):", (end - start) * 1000)
print()