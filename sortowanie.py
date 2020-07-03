import json
import itertools
import functools
import copy
import timeit
from ttictoc import TicToc
import random

source = []

for i in range(10000 ):
    source.append(random.randint(0, 100000))


def sort(arr, key=False,  result=[],):
    index = random.randint(0, len(arr) - 1)
    currentNumber = arr[index]

    if len(arr) == 1 or len(set(arr)) == 1:
        result += arr
        return True

    index = random.randint(0, len(arr) - 1)
    lower = []
    bigger = []

    for i, a in enumerate(arr):
        if a >= currentNumber:
            bigger.append(a)
        else:
            lower.append(a)

    if len(lower) != 0:
        sort(lower, 'l',  result)

    sort(bigger, 'b',  result)

    if key is True:
        return result


def bubble_Sort(arr):
    for i in range(len(arr)):
        for index, a in enumerate(arr):
            if index == len(arr) - 1:
                continue

            b = arr[index + 1]
            if a > b:
                arr[index] = b
                arr[index + 1] = a


bubble_Sort(source)



t = TicToc('name')
t.tic()
bubble_Sort(source)
t.toc()  # Prints and returns the elapsed time
print(t.elapsed)

t = TicToc('name')
t.tic()
sort(source)
t.toc()  # Prints and returns the elapsed time
print(t.elapsed)
