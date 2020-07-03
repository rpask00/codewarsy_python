def words_index(x):
    index = 0
    l = len(x)-1

    while True:
        yield index % l
        index += 1


def justify(text, width):
    words = text.split(' ')
    lines = [[]]
    bufor = 0

    for w in words:
        lines[-1].append(w)

        if len(' '.join(lines[-1])) > width:
            lines[-1].pop()
            lines.append([w])

    for i, l in enumerate(lines[:-1]):
        lack = width-len(' '.join(l))
        gen = words_index(l)
        while lack:
            if len(l) == 1:
                break

            lines[i][next(gen)] += ' '
            lack -= 1

    result = ''.join([' '.join(l)+'\n' for l in lines])
    return result[:-1]


print(justify('There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free', 30))


