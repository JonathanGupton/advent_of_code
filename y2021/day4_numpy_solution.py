import numpy as np
from collections import deque

n, *b = open(r"data/day04.txt")  # read input from stdin
b = np.loadtxt(b, int).reshape(-1, 5, 5)  # load boards into 3D array
out = deque()

for n in map(int, n.split(",")):  # loop over drawn numbers
    b[b == n] = -1  # mark current number as -1
    m = b == -1  # get all marked numbers
    win = (m.all(1) | m.all(2)).any(1)  # check for win condition
    if win.any():
        out.append((b * ~m)[win].sum() * n)  # print winning score
        b = b[~win]  # remove winning board
print(out)