
# a, b = (1, 2)
# print(a)
# print(b)




# my_list = [1, 2, 3]
# my_list.pop()
# print(my_list)
#
# my_list.pop(0)
# print(my_list)



# from collections import deque
#
# memory = deque()
# [memory.append((1, 2, 3, 4, 5)) for _ in range(5)]
# memory.append(('a', 'b', 'c', 'd', 'e'))
#
# # print(zip(*memory))
# # print(zip(memory))
#
#
# ones, twos, threes, fours, fives = zip(*memory)
#
# print(ones, twos, threes, fours, fives)


my_list = [1, 2, 3]
print(my_list)
print(*my_list)


def foo(a, b, c):
    print(a + b + c)


foo(*my_list)  # works and prints 6
foo(my_list)   # TypeError because b and c are missing
