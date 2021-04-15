import time
import math

from numba import jit, njit
from contextlib import contextmanager


@njit(cache=True)
def square(x):
    return x ** 2

@jit(nopython=True, cache=True)
def pythagorean_theorem(x, y):
    return math.sqrt(square(x) + square(y))


def pythagorus(x, y):
    return math.sqrt(x**2 + y**2)


@contextmanager
def timing(description: str) -> None:
    start = time.perf_counter()
    yield
    end = time.perf_counter()

    print(f"{description}: {end-start}")


def main():
    with timing("Python"):
        pythagorus(5, 5)

    with timing("Numba "):
        pythagorean_theorem(5, 5)

    with timing("Numba "):
        pythagorean_theorem(5, 5)


if __name__=="__main__":
    main()
