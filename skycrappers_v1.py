from ttictoc import TicToc
import timeit
import copy
import functools
import itertools
import json
import time


class Puzzle():
    def __init__(self, clues):
        self.clues = clues
        self.perms = set(itertools.permutations([1, 2, 3, 4, 5, 6, 7]))
        self.pairs = self.get_pairs()
        self.merged = []
        self.count = 0
        self.SIZE = 7
        self.city = [[0 for i in range(self.SIZE)] for j in range(self.SIZE)]

        for y in range(self.SIZE):
            for pair in self.pairs:
                if not pair:
                    continue

                if pair['id'] is y + 7:
                    horizontal = pair
                    break
            else:
                continue

            for x in range(self.SIZE):
                for pair in self.pairs:
                    if not pair:
                        continue

                    if pair['id'] is x:
                        vertical = pair
                        break
                else:
                    continue

                matches_x = set()
                matches_y = set()

                for h in horizontal['combinations']:
                    matches_x.add(h[x])

                for v in vertical['combinations']:
                    matches_y.add(v[y])

                shared = matches_y.intersection(matches_x)

                vertical['combinations'] = [
                    vert for vert in vertical['combinations'] if vert[y] in shared]
                horizontal['combinations'] = [
                    hor for hor in horizontal['combinations'] if hor[x] in shared]

    def vertigo(self, prev, act):
        if act > prev[-1]:
            prev.append(act)
        return prev

    def print_city(self, city):
        print('-------------------------')
        for cc in city:
            print(cc)
        print('-------------------------')

    def get_Mutual(self, aa, bb):
        return list(set(aa).intersection(bb))

    def insert_row(self, id, row, city):
        if id < 7:
            for i, r in enumerate(row):
                city[i][id] = r
            return city

        city[id - 7] = row
        cc = copy.deepcopy(city)
        return cc

    def chech_if_al_views_are_correct(self, city):
        inverse_city = []
        for i, c in enumerate(city):
            inverse_city.append([cc[i] for cc in city])
            if c.count(0):
                return False

            com = list(filter(lambda x: x['id'] == i + 7, self.merged))
            if com:
                com = com[0]['combinations']
                if not com.count(c):
                    return False

        for i, c in enumerate(inverse_city):
            if c.count(0):
                return False
            com = list(filter(lambda x: x['id'] == i, self.merged))
            if com:
                com = com[0]['combinations']
                if not com.count(c):
                    return False

        return True

    def get_pairs(self):
        views = [[] for x in range(7)]
        views_reverse = [[] for x in range(7)]
        for p in self.perms:
            point = list(p)
            inView = functools.reduce(self.vertigo, point, [point[0]])
            views[len(inView) - 1].append(json.dumps(point))
            point.reverse()
            views_reverse[len(inView) - 1].append(json.dumps(point))

        clues_1 = list(self.clues[:7])
        clues_2 = list(self.clues[7:14])
        clues_3 = list(self.clues[14:21])
        clues_3.reverse()
        clues_4 = list(self.clues[21:])
        clues_4.reverse()
        pairs = []

        for i, c in enumerate(clues_1):
            clues_1[i] = (clues_1[i], clues_3[i], i)

        for i, c in enumerate(clues_2):
            clues_2[i] = (clues_4[i], clues_2[i], i+7)

        for i, c in enumerate(clues_1 + clues_2):
            if not c[0] and not c[1]:
                pairs.append(None)
                continue
            elif c[0] and c[1]:
                mutual = self.get_Mutual(views[c[0]-1], views_reverse[c[1]-1])
            elif c[0] and not c[1]:
                mutual = views[c[0]-1]
            elif not c[0] and c[1]:
                mutual = views_reverse[c[1]-1]

            pairs.append({
                "is_horizontal": i > 6,
                "v1": c[0],
                "v2": c[1],
                "id": c[2],
                "combinations": [json.loads(m) for m in mutual],
                'size': len(mutual)
            })

        # return pairs[:6], pairs[6:]
        return pairs

    def validate_city(self, city, potential_row, index, is_horizontal):
        if is_horizontal:
            row = city[index]
        else:
            row = [c[index] for c in city]

        for i, r in enumerate(row):
            if r is 0:
                continue
            if r != potential_row[i]:
                return False

        return True

    def validate_city_all(self, city):
        reverse_city = [[] for x in range(7)]
        for row in city:
            for i, r in enumerate(row):
                if r is 0:
                    continue

                if r in reverse_city[i]:
                    return False

                reverse_city[i].append(r)

            row = [r for r in row if r is not 0]
            if len(set(row)) is not len(row):
                return False

        return True

    def solve_puzzle(self):
        combinations = list(filter(lambda i: i, self.pairs))
        self.merged = sorted(combinations, key=lambda x: x['size'])
        self.solve(self.city, 0)
        return self.city

    def solve(self, city, id):
        self.count += 1
        if id == len(self.merged):
            if self.chech_if_al_views_are_correct(city):
                self.city = city
                return True
            else:
                self.solve_after(city)
                return True

        m = self.merged[id]

        for c in m['combinations']:
            if self.validate_city(city, c, m['id'] % 7, m['is_horizontal']):
                fake_City = self.insert_row(m['id'], c, copy.deepcopy(city))
                if not self.validate_city_all(fake_City):
                    continue

                if self.solve(fake_City, id + 1):
                    return True

        return False

    def solve_after(self, city):
        print('solve')

        def get_matching_solves(current_row, potential_row):
            for i, current in enumerate(current_row):
                if current is 0:
                    continue

                if potential_row[i] is not current:
                    return False

            return True

        for i, row in enumerate(city):
            if row.count(0):
                matching = filter(lambda potential: get_matching_solves(
                    row, potential), self.perms)

                for match in matching:
                    fake_City = self.insert_row(
                        i+7, list(match), copy.deepcopy(city))

                    if not self.validate_city_all(fake_City):
                        continue

                    if self.solve_after(fake_City):
                        return True

                return False

        self.city = city


clues = [
    # (3, 2, 2, 3, 2, 1,   1, 2, 3, 3, 2, 2,   5, 1, 2, 2, 4, 3,   3, 2, 1, 2, 2, 4),
    (0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0),
    (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0),
    (4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4),
    (0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0),
    (5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3),
    (4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0),
    (2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5),
    (1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4, 4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1),
    (0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0),
    (3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3),
    (0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1),
    (0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0),
    (0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0, 0, 3, 0, 5, 3, 4),
    (5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2),
    (1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1),
    (3, 2, 1, 2, 2, 4, 3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3),
    (4, 3, 2, 5, 1, 5, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 3, 5, 4, 1, 2, 3, 4),
    (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0),
    (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0)



]

# 0-6   -   20-14 
# 7-13    -   27-21

clues7x7 = [
    [0, 0, 5, 3, 0, 2, 0,   0, 0, 0, 4, 5, 0, 0,
0, 0, 0, 3, 2, 5, 4,   2, 2, 0, 0, 0, 0, 5],
    [7, 0, 0, 0, 2, 2, 3,   0, 0, 3, 0, 0, 0, 0,
        3, 0, 3, 0, 0, 5, 0,   0, 0, 0, 0, 5, 0, 4],
    [6, 4, 0, 2, 0, 0, 3,   0, 3, 3, 3, 0, 0, 4,
        0, 5, 0, 5, 0, 2, 0,   0, 0, 0, 4, 0, 0, 3],
    [0, 0, 0, 5, 0, 0, 3,   0, 6, 3, 4, 0, 0, 0,
        3, 0, 0, 0, 2, 4, 0,   2, 6, 2, 2, 2, 0, 0],
    [0, 0, 5, 0, 0, 0, 6,   4, 0, 0, 2, 0, 2, 0,
        0, 5, 2, 0, 0, 0, 5,   0, 3, 0, 5, 0, 0, 3],
    [0, 0, 5, 3, 0, 2, 0,   0, 0, 0, 4, 5, 0, 0,
        0, 0, 0, 3, 2, 5, 4,   2, 2, 0, 0, 0, 0, 5],
    [0, 2, 3, 0, 2, 0, 0,   5, 0, 4, 5, 0, 4, 0,
        0, 4, 2, 0, 0, 0, 6,   5, 2, 2, 2, 2, 4, 1],
    [0, 2, 3, 0, 2, 0, 0,   5, 0, 4, 5, 0, 4, 0,
        0, 4, 2, 0, 0, 0, 6,   0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 0, 5, 0,   0, 0, 0, 0, 5, 0, 4,
        7, 0, 0, 0, 2, 2, 3,   0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 4,   7, 0, 0, 0, 2, 2, 3,
        0, 0, 3, 0, 0, 0, 0,   3, 0, 3, 0, 0, 5, 0],
    [0, 0, 3, 0, 0, 0, 0,   3, 0, 3, 0, 0, 5, 0,
        0, 0, 0, 0, 5, 0, 4,   7, 0, 0, 0, 2, 2, 3],
    [3, 3, 2, 1, 2, 2, 3,   4, 3, 2, 4, 1, 4, 2,   2, 4, 1, 4, 5, 3, 2,   3, 1, 4, 2, 5, 2, 3]
]

t = TicToc('name')
# t.tic()
for tt in clues7x7:
    t.tic()
    puz = Puzzle(tt)
    print(tt.count(0))
    puz.print_city(puz.solve_puzzle())

    t.toc()  # Prints and returns the elapsed time
    print(t.elapsed)
