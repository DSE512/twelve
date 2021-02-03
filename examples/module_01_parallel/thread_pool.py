import time

from concurrent.futures import ThreadPoolExecutor


def snooze():
    print("Sleeping for two seconds.")
    time.sleep(2)
    print("Done sleeping.")
    return "I am awake!"


def main():
    start = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(snooze) for _ in range(4)]

    print(f"\nResults from executor:")
    for fut in futures:
        result = fut.result()
        print(result)

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

