import time
import random

from numba import jit
from contextlib import contextmanager


@jit(nopython=True)
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


@contextmanager
def timing(description: str) -> None:
    start = time.perf_counter()
    yield
    end = time.perf_counter()

    print(f"{description}: {end-start:.6f}")


if __name__=="__main__":

    with timing("First iteration "):
        pi = monte_carlo_pi(1_000_000)

    with timing("Second iteration"):
        pi = monte_carlo_pi(1_000_000)
