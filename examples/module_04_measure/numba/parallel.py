import time
from numba import njit, prange
from contextlib import contextmanager


@njit(parallel=True)
def prange_test(A):
    s = 0
    # Without "parallel=True" in the jit-decorator
    # the prange statement is equivalent to range
    for i in prange(A.shape[0]):
        s += A[i]
    return s

@contextmanager
def timing(description: str) -> None:
    start = time.perf_counter()
    yield
    end = time.perf_counter()

    print(f"{description}: {end-start:.6f}")


if __name__=="__main__":
    import numpy as np

    with timing("parallel"):
        x = np.arange(1_000_000)
        prange_test(x)
