import time

from concurrent import futures


def snooze(seconds):
    """Snooze for seconds

    Args:
        seconds: amount of time to snooze for

    Returns:
        seconds: So that we can see the order
                 in which threads finish
    """
    print(f"Sleeping for {seconds} seconds.")
    time.sleep(seconds)
    return f"Slept for {seconds} seconds"


def main():
    start = time.perf_counter()

    with futures.ThreadPoolExecutor() as executor:
        seconds = [3, 4, 1, 2]
        futs = [executor.submit(snooze, sec) for sec in seconds]

    print(f"\nResults from executor:\n")
    for fut in futures.as_completed(futs):
        print(fut.result())

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

