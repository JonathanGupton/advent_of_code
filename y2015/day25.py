

target_row = 3010
target_column = 3019

value = 20151125
multiplier = 252533
divisor = 33554393

max_row = 0
current_row, current_column = 0, 0

while True:
    if current_row == target_row - 1 and current_column == target_column - 1:
        print(value)
        break
    if current_row == 0:
        max_row += 1
        next_row, next_column = max_row, 0
    else:
        next_row = current_row - 1
        next_column = current_column + 1
    value = (value * multiplier) % divisor
    current_row, current_column = next_row, next_column
