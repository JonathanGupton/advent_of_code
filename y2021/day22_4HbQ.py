from re import findall


def count(cubes):
    if not cubes:
        return 0

    (state, *head), *tail = cubes
    if state == "off":
        return count(tail)

    return (
        volume(*head)
        + count(tail)
        - count({intersect(*head, *t) for t in tail} - {None})
    )


def intersect(x, X, y, Y, z, Z, _, u, U, v, V, w, W):
    x = x if x > u else u
    X = X if X < U else U
    y = y if y > v else v
    Y = Y if Y < V else V
    z = z if z > w else w
    Z = Z if Z < W else W
    if x <= X and y <= Y and z <= Z:
        return "", x, X, y, Y, z, Z


def volume(x, X, y, Y, z, Z):
    return (X - x + 1) * (Y - y + 1) * (Z - z + 1)


def parse(line):
    state, new = line.split()
    return state, *map(int, findall(r"-?\d+", new))


c = count(map(parse, open(r"data/day22.txt")))
print(c)
