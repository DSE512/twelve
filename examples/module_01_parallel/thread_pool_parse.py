import time

from pathlib import Path
from concurrent import futures


def read_file(path):
    """Read in a text file

    Args:
        path: path to the text.
    """
    start = time.perf_counter()

    with open(path, 'r') as f:
        text = f.readlines()

    end = time.perf_counter()
    print(f"Read file in: {end-start:.4} seconds.")

    return text


def main():
    start = time.perf_counter()

    paths = Path("data").glob("**/*.txt")
    files = [x for x in paths if x.is_file()]

    with futures.ThreadPoolExecutor() as executor:
        futs = executor.map(read_file, files)

    print(f"\nResults from executor:\n")
    for fut in futs:
        num_lines = len(fut)
        print(f"File has {num_lines} number of lines")

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

