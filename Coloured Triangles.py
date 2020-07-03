import numpy as np
import functools
import itertools
from ttictoc import TicToc
import timeit
import time


def triangle(row):
    vector = [*map("RGB".index, row)]

    while len(vector) - 1:
        while len(vector) % 3 - 1:
            vector = [(-a - b) % 3 for a, b in zip(vector, vector[1:])]
        vector = vector[::3]
    return "RGB"[vector[0]]


