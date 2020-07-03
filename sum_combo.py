results = []


def find_combos(n, arr):
    if sum(arr) == n:
        results.append(arr)
        return True
    elif sum(arr) > n:
        return False

    last_index = arr[-1] if len(arr) else 1
    for i in range(last_index, n+1):
        arr.append(i)
        if find_combos(n, arr.copy()):
            continue
        else:
            arr.pop()

    return False


def combos(n):
    global results
    results = []
    find_combos(n, [])
    return results


for r in combos(30):
    print(r)


