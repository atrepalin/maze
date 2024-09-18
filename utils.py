import matplotlib.pyplot as plt
import functools


def plotlive(func):
    plt.ion()

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        axes = plt.gcf().get_axes()

        for axis in axes:
            axis.cla()

        result = func(*args, **kwargs)

        plt.draw()
        plt.pause(0.01)

        return result

    return new_func
