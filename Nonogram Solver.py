import json
import copy


class Nonogram:
    def __init__(self, clues):
        self.clues = clues
        self.SIZE = len(clues[0])
        self.result = [[0 for i in range(self.SIZE)] for i in range(self.SIZE)]
        self.arrangements = {}
        self.order = []

        for clue in clues:
            for c in clue:
                if c not in self.arrangements:
                    self.arrangements[c] = self.__getArrangements(c)

        self.__get_order()

    def insert(self, previous_Result, row, arrangement, isHorizontal):
        current_row = previous_Result[row] if isHorizontal else [
            previous_Result[i][row] for i in range(self.SIZE)]

        for i, current in enumerate(current_row):
            if current is 1 and arrangement[i] is 0:
                return False

        if isHorizontal:
            previous_Result[row] = arrangement
        else:
            for i in range(self.SIZE):
                previous_Result[i][row] = arrangement.pop(0)

        return previous_Result

    def solve(self):
        # self.filter_solve()
        self.__solve(copy.deepcopy(self.arrangements),
                     copy.deepcopy(self.result), 0, {})
        return tuple([tuple(r) for r in self.result])

    def filter_solve(self, prev_inserts, arragments):

        for clue in prev_inserts:
            arragment = prev_inserts[clue]
            arragments[clue] = [arragment]

        status = [False]

        while not all(status):
            status = []
            for y in range(self.SIZE):
                for x in range(self.SIZE):
                    positions = set()

                    for row in arragments[self.clues[1][y]]:
                        for i, cell in enumerate(row):
                            if cell:
                                positions.add(i)

                    columns = arragments[self.clues[0][x]]

                    prev_len = len(columns)
                    columns = [col for col in columns if not (
                        col[y] and x not in positions)]
                    new_len = len(columns)

                    if new_len is 0:
                        return False

                    status.append(prev_len == new_len)

            for x in range(self.SIZE):
                for y in range(self.SIZE):
                    positions = set()

                    for column in arragments[self.clues[0][x]]:
                        for i, cell in enumerate(column):
                            if cell:
                                positions.add(i)

                    rows = arragments[self.clues[0][x]]

                    prev_len = len(rows)
                    rows = [row for row in rows if not(
                        row[y] and y not in positions)]

                    new_len = len(rows)

                    if new_len is 0:
                        return False

                    status.append(prev_len == new_len)

        return True

    def __get_order(self):
        row = 0
        for clue in self.clues:
            for c in clue:
                self.order.append((len(self.arrangements[c]), row))
                self.order = sorted(self.order, key=lambda a: a[0])
                row += 1

    def __solve(self, arrangements, prev_result, order, prev_inserts):
        if order is 3:
            if not self.filter_solve(prev_inserts, arrangements):
                return False

        if order == self.SIZE*2:
            self.result = prev_result
            return True

        row = self.order[order][1]

        isHorizontal = row//self.SIZE
        index = row % self.SIZE

        clue = self.clues[isHorizontal][index]

        for arrangement in arrangements[clue]:
            new_result = self.insert(
                copy.deepcopy(prev_result), index, arrangement.copy(), isHorizontal)

            if new_result is False:
                continue

            prev_inserts[clue] = arrangement

            if self.__solve(copy.deepcopy(arrangements), new_result, order+1, prev_inserts):
                return True

        return False

    def __convertArrangements(self, arrangement, clue):
        newrow = [0 for i in range(self.SIZE)]

        for c in reversed(clue):
            index = arrangement.pop()
            for i in range(c):
                newrow[index] = 1
                index -= 1

        return newrow

    def __getArrangements(self, clue):
        arrangements = []
        index = clue[0]-1

        while index < self.SIZE:
            arrangements.append([index])
            index += 1

        for c in clue[1:]:
            for i, a in enumerate(arrangements):
                index = 1
                while True:
                    nxt_index = sum([a[-1], c, index])
                    if nxt_index >= self.SIZE:
                        break
                        # if len(a) is not len(clue):
                        #     arrangements.remove(a)

                    arrangements.append(a + [nxt_index])
                    index += 1

        arrangements = set([json.dumps(a)
                            for a in arrangements if len(a) == len(clue)])

        return [self.__convertArrangements(json.loads(a), clue) for a in arrangements]


clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))


clues_ = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1,
                                  1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)

# clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,)))

n = Nonogram(clues)
print(n.solve())
