from itertools import groupby


def look_and_say_groupby(initial):
    output = ""
    for k, g in groupby(initial):
        output += str(sum(1 for _ in g)) + str(k)
    return output


initial = "1113122113"
for _ in range(49):
    initial = look_and_say_groupby(initial)
print(len(look_and_say_groupby(initial)))
