from functools import cache


@cache
def chunk(w, z, div_z, add_x, add_y):
    x = z % 26
    z //= div_z
    x += add_x
    x = ((w == x) == 0)
    y = 25 * x + 1
    z *= y
    y = (w + add_y) * x
    z += y
    return z


diff_ops = (
    (1, 11, 14),
    (1, 13, 8),
    (1, 11, 4),
    (1, 10, 10),
    (26, -3, 14),
    (26, -4, 10),
    (1, 12, 4),
    (26, -8, 14),
    (26, -3, 1),
    (26, -12, 6),
    (1, 14, 0),
    (26, -6, 9),
    (1, 11, 13),
    (26, -12, 12)
)


def find_highest_value():
    global diff_ops
    z = 0
    depth = 0
    n_diff_ops = 14

    def process_chunks(z, depth):
        if depth == n_diff_ops:
            return z == 0
        for w in range(9, 0, -1):
            z = chunk(w, z, *diff_ops[depth])
            if out := process_chunks(z, depth+1):
                return str(w) + str(out)

    return process_chunks(z, depth)


highest_value = find_highest_value()

# https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs
