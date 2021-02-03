import random
import multiprocessing as mp


def random_integer(output):
    """Generate a random integer in [0, 9]

    Args:
        output: multiprocessing queue
    """
    integer = random.randint(0, 9)
    output.put(integer)


def main():
    output = mp.Queue()

    processes = []
    for _ in range(4):
        processes.append(
            # Create a process that wraps our function
            mp.Process(target=random_integer, args=(output,))
        )

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    results = [output.get() for proc in processes]
    print(results)


if __name__=="__main__":
    main()

