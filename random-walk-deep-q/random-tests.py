
from timeit import timeit, repeat
import random


# buckets = [
#     0,  # 0
#     0,  # 1
#     0,  # 2
#     0,  # 3
#     0,  # 4
#     0,  # 5
#     0,  # 6
#     0,  # 7
#     0,  # 8
#     0   # 9
# ]
#
#
# def rand_dist(n):
#     mod = n / 10
#     for i in range(n):
#         if i % mod == 0:
#             print(i)
#         buckets[int(str(10 * random.random())[0])] += 1
#
#     return [k/n for k in buckets]
#
#
# print(rand_dist(10000000))


# prices = [8, 3, 6, 9]
#
# tuples = [(i, p) for i, p in enumerate(prices)]
# print(tuples)


# def adjust_list(list_to_adjust, length):
#     diff = max(length - len(list_to_adjust), 0)
#     if diff == 0:
#         ret = list_to_adjust[-100:]
#     else:
#         ret = [0] * diff + list_to_adjust
#     return ret
#
#
# pack = [1, 2, 3, 4]
#
# print(adjust_list(pack, 10))


def get_ma(a_list, n):
    calc_list = a_list[-n:]
    return sum(calc_list)/len(calc_list)


new_list = [1, 2, 3, 4, 5]
print(get_ma(new_list, 3))
