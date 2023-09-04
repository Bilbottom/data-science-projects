
import random
from matplotlib import pyplot as plt


def random_walk(start, volatility, length) -> list:
    volatility_neg = -1 * volatility
    walk = [start]
    walk.extend(
        max(walk[-1] + random.uniform(volatility_neg, volatility), 0)
        for _ in range(1, length)
    )
    return walk


def relative_walk(start, volatility, length) -> list:
    factor = 1 + volatility
    walk = [start]
    walk.extend(
        max(walk[-1] * random.uniform(1 / factor, factor), 0)
        for _ in range(1, length)
    )
    return walk


def normal_walk(start, volatility, length) -> list:
    walk = [start]
    walk.extend(
        max(walk[-1] + random.gauss(0, volatility), 0)
        for _ in range(1, length)
    )
    return walk


def plot_walk(start, volatility, length, use_walk):
    time = list(range(length))
    walk1 = use_walk(start, volatility, length)
    walk2 = use_walk(start, volatility, length)
    walk3 = use_walk(start, volatility, length)
    walk4 = use_walk(start, volatility, length)
    plt.plot(time, walk1)
    plt.plot(time, walk2)
    plt.plot(time, walk3)
    plt.plot(time, walk4)
    plt.show()


def plot_norm_rand(start, volatility, length):
    time = list(range(length))
    walk1 = random_walk(start, volatility, length)
    walk2 = random_walk(start, volatility, length)
    walk3 = normal_walk(start, volatility, length)
    walk4 = normal_walk(start, volatility, length)
    plt.plot(time, walk1, color='blue')
    plt.plot(time, walk2, color='blue')
    plt.plot(time, walk3, color='red')
    plt.plot(time, walk4, color='red')
    # more range with normal walk
    plt.show()


# plot_walk(100, 1, 1000, random_walk)
# plot_walk(100, 1, 1000, relative_walk)
# plot_walk(1000, 1, 10000, normal_walk)
plot_norm_rand(1000, 1, 1000)
