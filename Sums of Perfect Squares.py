import math


def sum_of_squares(n, arr=[], root=True, minimum=100):
    if minimum <= len(arr):
        return False

    if root:
        arr = []

    amount = sum([a ** 2 for a in arr])
    if amount == n:
        return True

    lower_sqrt = int(math.sqrt(n - sum([a ** 2 for a in arr])))
    arr.append(lower_sqrt)

    while lower_sqrt:
        if sum_of_squares(n, arr, False, minimum):
            if root:
                minimum = len(arr) if minimum >= len(arr) else minimum
                lower_sqrt -= 1
                arr = [lower_sqrt]
            else:
                return arr
        elif root:
            lower_sqrt -= 1
            arr = [lower_sqrt]
        else:
            return False
    return minimum
