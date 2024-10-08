import matplotlib.pyplot as plt
import functools
import keyboard


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


def select_option(options):
    current_selection = 0

    def print_menu():
        for i, option in enumerate(options):
            if i == current_selection:
                print(f"\033[0;32m\033[K> {option}")
            else:
                print(f"\033[0m\033[K  {option}")

    print_menu()

    while True:
        print(f"\033[0m\033[{len(options)}A", end="")

        event = keyboard.read_event()

        if event.event_type == "down":
            if event.name == "up":
                current_selection = (current_selection - 1) % len(options)
            elif event.name == "down":
                current_selection = (current_selection + 1) % len(options)
            elif event.name == "enter":
                print(f"\033[{len(options)}B", end="")
                break

        print_menu()

    return current_selection
