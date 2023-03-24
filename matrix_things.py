import numpy as np


def int_to_bin(rgb):
    r, g, b = rgb
    return f'{r:08b}', f'{g:08b}', f'{b:08b}'


def bin_to_int(rgb):
    r, g, b = rgb
    return int(r, 2), int(g, 2), int(b, 2)


def set_bit(arr, i):
    if i <= 0 or i > len(arr):
        return arr
    if arr[i - 1][0] == 1:
        arr[i - 1][0] = 0
    else:
        arr[i - 1][0] = 1
    return arr


def arr_to_str(arr):
    res = ''.join(map(lambda x: str(x[0]), arr))
    return res


def str_to_arr(s):
    m = [[int(x)] for x in s]
    return np.array(m)


def get_ind(arr):
    s = ''.join(map(lambda x: str(x[0]), arr))
    return int(s, 2)


def matr_to_bin(m):
    m = [x % 2 for x in m]
    return np.array(m)
