"""Question 2"""
import time
import numpy as np

from concurrent import futures


def timing(function):
    """Timing decorator

    Decorators allow us to wrap some
    `function` with added functionality;
    in this case, measuring how much time
    the function took to run.
    """
    def wrap(*args, **kwargs):
        start = time.perf_counter()
        ret = function(*args, **kwargs)
        end = time.perf_counter()
        print(f"Total time: {end-start} seconds.")
        return ret
    return wrap


def expand(step, num_steps):
    """A single step in the series expansion"""
    return 1 / (1 + ((step-0.5) / num_steps)**2)


def compute_series(num_steps=10):
    """Approximate pi by exapnding our series `num_steps`"""
    steps = []
    for step in range(num_steps):
        steps.append(
            expand(step, num_steps)
        )

    approx = 4 / num_steps * sum(steps)

    return num_steps, approx


@timing
def singlethread_series(expansions):
    for step in expansions:
        steps, approx = compute_series(step)
        print_difference(steps, approx)


@timing
def multithread_series(expansions):
    with futures.ThreadPoolExecutor() as executor:
        futs = executor.map(compute_series, expansions)

    for steps, approx in futs:
        print_difference(steps, approx)


def print_difference(steps, approx):
    print(
        f"Pi({steps}) = {approx:<20} | " \
        f"Pi - approximation = {np.pi-approx:.5}"
    )


def main():
    from viztracer import VizTracer

    expansions = [*range(10, 10_000, 50)]

    print(f"Single Thread Execution:")
    singlethread_series(expansions)

    tracer = VizTracer()
    tracer.start()

    print(f"Multi-thread Execution:")
    multithread_series(expansions)

    tracer.stop()
    tracer.save("multithread_results.html")


if __name__=="__main__":
    main()

