import functools
import itertools
import collections
import json


sea = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
       [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
       [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

correct_ships = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]


def red_horizontal(prev, curr):
    for i, pr in enumerate(prev):
        p = pr[len(pr)-1]
        if p['y'] == curr['y'] and p['x'] + 1 == curr['x']:
            prev[i].append(curr)
            return prev

    prev.append([curr])
    return prev


def red_vertical(prev, curr):
    for i, pr in enumerate(prev):
        p = pr[len(pr)-1]
        if p['x'] == curr['x'] and p['y'] + 1 == curr['y']:
            prev[i].append(curr)
            return prev

    prev.append([curr])
    return prev


def get_duplcates(a):
    return [[json.loads(item)] for item, count in collections.Counter(a).items() if count > 1]


def getCordsToDelete(ship):
    cordsToDelete = []
    for cord in ship:
        for x in range(-1, 2):
            for y in range(-1, 2):
                next_cord = {'x': cord['x'] + x, 'y': cord['y'] + y}
                if ship.count(next_cord):
                    continue
                if cord['x'] + x <= 9 and cord['y'] + y <= 9 and cord['x'] + x >= 0 and cord['y'] + y >= 0:
                    cordsToDelete.append(json.dumps(next_cord))

    cordsToDelete = set(cordsToDelete)
    return [json.loads(c) for c in cordsToDelete]


def validate_battlefield(sea):
    sea = list(itertools.chain(*sea))
    cords = []
    for i, cord in enumerate(sea):
        if cord:
            cords.append({
                "x": i % 10,
                "y": i // 10,
            })

    hor = functools.reduce(red_horizontal, cords, [])
    ver = functools.reduce(red_vertical, cords, [])

    storage = [h for h in hor if len(h) > 1]
    storage += [v for v in ver if len(v) > 1]
    storage += get_duplcates([json.dumps(ship) for ship in itertools.chain(*[h for h in hor if len(h) == 1] + [v for v in ver if len(v) == 1])])
    storage_len = [len(s) for s in storage]
    storage_len.sort()
    if storage_len != correct_ships:
        return False
    delete = []

    for s in storage:
        delete.append(getCordsToDelete(s))

    delete = itertools.chain(*delete)
    for d in delete:
        if cords.count(d):
            return False

    return True


print(validate_battlefield(sea))
