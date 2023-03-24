import numpy as np


def int_to_bin(rgb):
    r, g, b = rgb
    return f'{r:08b}', f'{g:08b}', f'{b:08b}'


def int_to_bin_arr(rgb):
    r, g, b = rgb
    rb = bin(r)[2:]
    gb = bin(g)[2:]
    bb = bin(b)[2:]
    return [0] * (8 - len(rb)) + [int(x) for x in rb], [0] * (8 - len(gb)) + [int(x) for x in gb], [0] * (
                8 - len(bb)) + [int(x) for x in bb]


def bin_to_int(rgb):
    r, g, b = rgb
    return get_ind(r), get_ind(g), get_ind(b)


def set_bit(arr, i):
    if i <= 0 or i > len(arr):
        return arr
    if arr[i - 1] == 1:
        arr[i - 1] = 0
    else:
        arr[i - 1] = 1
    return arr


def get_ind(arr):
    return int("".join(str(x) for x in arr), 2)


def matr_to_bin(m):
    m = [x % 2 for x in m]
    return np.array(m)
