import time


def snooze():
    print("Sleeping for two seconds.")
    time.sleep(2)
    print("Done sleeping.")


def main():
    start = time.perf_counter()

    for _ in range(4):
        snooze()

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

