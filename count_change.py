def count_change(coins, amount):
    if amount == 0:
        return 1
    if amount < 0:
        return 0
    if len(coins) == 0:
        return 0

    return count_change(coins, amount - coins[-1]) + count_change(coins[:-1], amount)


print(count_change([1, 2, 3], 4))
print(count_change([2, 5, 10, 20, 50], 419))
