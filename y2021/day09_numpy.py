import numpy as np


def local_minima(m):
    m = np.pad(m, pad_width=1, mode='constant', constant_values=9)
    return ((m < np.roll(m, 1, 0)) &
            (m < np.roll(m, -1, 0)) &
            (m < np.roll(m, 1, 1)) &
            (m < np.roll(m, -1, 1)))[1:-1,1:-1]


matrix = np.genfromtxt(r"data/day09.txt", delimiter=1)
minima = local_minima(matrix)
values = np.extract(minima, matrix)
print(int(sum(values)) + len(values))
