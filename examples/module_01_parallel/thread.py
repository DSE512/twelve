import time
import threading


def snooze():
    print("Sleeping for two seconds.")
    time.sleep(2)
    print("Done sleeping.")


def main():
    start = time.perf_counter()

    threads = []
    for _ in range(4):
        threads.append(
            threading.Thread(target=snooze)
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

