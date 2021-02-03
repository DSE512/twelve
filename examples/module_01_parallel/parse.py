import time

from pathlib import Path
from multiprocessing import Pool


def read_file(path):
    """Read in a text file

    Args:
        path: path to the text.
    """
    start = time.perf_counter()

    with open(path, 'r') as f:
        text = f.readline()

    end = time.perf_counter()
    print(f"Read file in: {end-start:.4} seconds.")

    return text


def main():
    start = time.perf_counter()

    paths = Path("data").glob("**/*.txt")
    files = [x for x in paths if x.is_file()]

    pool = Pool(4)
    results = pool.map(read_file, files)
    pool.close()

    end = time.perf_counter()
    print(f"Total time: {end-start} seconds.")


if __name__=="__main__":
    main()

