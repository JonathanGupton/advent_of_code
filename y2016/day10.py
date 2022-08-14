from collections import deque, defaultdict


with open(r"data/day10.txt", "r") as f:
    instructions = deque(line.strip() for line in f.readlines())

bots: dict[int, list[int]] = defaultdict(list)
outputs: dict[int, list[int]] = defaultdict(list)

value_func = {"high": max, "low": min}
recipient_map = {"bot": bots, "output": outputs}

while instructions:
    instruction = instructions.popleft()
    match instruction.split():
        case ["value", value, "goes", "to", "bot", bot]:
            value, bot = int(value), int(bot)
            bots[bot].append(value)
        case [
                "bot",
                donor,
                "gives",
                left_value,
                "to",
                left_recipient_type,
                left_recipient_id,
                "and",
                right_value,
                "to",
                right_recipient_type,
                right_recipient_id
        ]:
            donor = int(donor)
            if len(bots[donor]) == 2:
                if min(bots[donor]) == 17 and max(bots[donor]) == 61:
                    print(f"Bot with microchip-17 and microchip-61 is {donor}")

                left_recipient_id, right_recipient_id = (
                    int(left_recipient_id), int(right_recipient_id)
                )

                recipient_map[left_recipient_type][left_recipient_id].append(
                    value_func[left_value](bots[donor])
                )

                recipient_map[right_recipient_type][right_recipient_id].append(
                    value_func[right_value](bots[donor])
                )

                bots[donor] = []

            else:
                instructions.append(instruction)

print(outputs[0][0] * outputs[1][0] * outputs[2][0])
