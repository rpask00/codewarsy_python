def sum_of_intervals(source):
    result = 0
    source.sort(key=lambda x: x[0])
    fake_ss = source.copy()
    intervals = []

    for i, ss in enumerate(source):
        for s in source:
            if ss[0] > s[0] and ss[1] < s[1]:
                try:
                    fake_ss.remove(ss)
                except:
                    continue

    for i in fake_ss:
        if not len(intervals):
            intervals.append(i)

        if i[0] > intervals[-1][1]:
            intervals.append(i)
        else:
            intervals[-1] = (intervals[-1][0], i[1])

    for i in intervals:
        result += i[1]-i[0]

    return result


# intervals = [(428, 442), (13, 55), (-327, 484), (-24, 64), (-207, -205), (324, 352), (487, 496), (451, 454), (364, 484), (-435, -173), (342, 460), (-40, 468), (196, 356), (482, 492), (-337, 99), (-362, -71)]

# print(sum_of_intervals(intervals))


# def sum_of_intervals(intervals):
#     return len(set([n for (a, b) in intervals for n in [i for i in range(a, b)]]))
