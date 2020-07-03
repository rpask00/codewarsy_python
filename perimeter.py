from functools import reduce
counter = 0


def reduceSmall(x, y):
    global counter
    if x:
        if x != y:
            counter += 1
    return y


def land_perimeter(arr):
    global counter
    counter = 0

    landHorizont = arr[:]
    length = len(landHorizont[0])
    landVertical = [[] for h in range(length)]

    for i, hor in enumerate(landHorizont):
        for j, h in enumerate(hor):
            landVertical[j].append(h)
    landVertical = [''.join(v) for v in landVertical]

    for h in landHorizont:
        reduce(reduceSmall, h)

    for v in landVertical:
        reduce(reduceSmall, v)

    for arr in [landHorizont[0], landHorizont[-1], landVertical[0], landVertical[-1]]:
        for a in arr:
            if a is 'X':
                counter += 1
    return 'Total land perimeter: {}'.format(counter)


print(land_perimeter(["OXOOOX", "OXOXOO", "XXOOOX", "OXXXOO", "OOXO\OX", "OXOOOO", "OOXOOX", "OOXOOO", "OXOOOO", "OXOOXX"]))
print(land_perimeter(["OXOOO", "OOXXX", "OXXOO", "XOOOO", "XOOOO", "XXXOO", "XOXOO", "OOOXO", "OXOOX", "XOOOO", "OOOXO"]))
print(land_perimeter(["XXXXXOOO", "OOXOOOOO", "OOOOOOXO", "XXXOOOXO", "OXOXXOOX"]))
print(land_perimeter(["XOOOXOO", "OXOOOOO", "XOXOXOO", "OXOXXOO", "OOOOOXX", "OOOXOXX", "XXXXOXO"]))
print(land_perimeter(["OOOOXO", "XOXOOX", "XXOXOX", "XOXOOO", "OOOOOO", "OOOXOO", "OOXXOO"]))
