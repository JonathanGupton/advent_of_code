from collections import deque


CHUNKS = {"{": "}", "[": "]", "(": ")", "<": ">"}


def parse_input(filepath) -> list[str]:
    with open(filepath, 'r') as f:
        input_data = f.read().strip().split('\n')
    return input_data


def process_line(line: str) -> int | deque:
    global CHUNKS
    illegal_character_value = {
        ")" : 3,
        "]" : 57,
        "}" : 1197,
        ">" : 25137
    }
    line = deque(line)
    left = deque()
    while line:
        current_char = line.popleft()
        if not left:
            left.append(current_char)
        else:
            if CHUNKS[left[-1]] == current_char:
                left.pop()
            else:
                if current_char in CHUNKS:
                    left.append(current_char)
                else:
                    return illegal_character_value[current_char]
    return left


def complete_line(remaining_line: deque) -> deque[str]:
    global CHUNKS
    closing_chunks = deque()
    while remaining_line:
        closing_chunks.append(CHUNKS[remaining_line.popleft()])
    return closing_chunks


def compute_score(chunk_to_score: deque[str]) -> int:
    char_score = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    while chunk_to_score:
        score = (score * 5) + char_score[chunk_to_score.pop()]
    return score


def part_a():
    fp = r"data/day10.txt"
    data = parse_input(fp)
    n = 0
    for line in data:
        if points := process_line(line):
            if isinstance(points, int):
                n += points
    return n


def part_b():
    fp = r"data/day10.txt"
    data = parse_input(fp)
    scores = []
    for line in data:
        if output := process_line(line):
            if isinstance(output, deque):
                closing_chunks = complete_line(output)
                scores.append(compute_score(closing_chunks))
    return sorted(scores)[len(scores) // 2]


if __name__ == '__main__':
    print(part_a())
    print(part_b())
