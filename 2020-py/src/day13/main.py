from src.helper import IO
from functools import reduce


#   --- NOT MY CODE : https://rosettacode.org/wiki/Chinese_remainder_theorem
def chinese_remainder(n, a):
    sum_val = 0
    prod = reduce(lambda x, y: x * y, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_val += a_i * mul_inv(p, n_i) * p
    return sum_val % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1
#   --- NOT MY CODE ENDS HERE


file_input = IO.read_all()
orig_timestamp, IDs = int(file_input[0]), [int(x) if x[0] != 'x' else 0 for x in file_input[1].split(",")]

IO.write(orig_timestamp, IDs)
bus = min([(((orig_timestamp-1)//ID * ID + ID), ID) for ID in IDs if ID > 0])
IO.write(bus, (bus[0] - orig_timestamp) * bus[1])
IO.write(chinese_remainder(*zip(*[(ID[1], ID[1] - ID[0]) for ID in enumerate(IDs) if ID[1] > 0])))
