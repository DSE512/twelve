import time
from twelve.data import Images
from concurrent import futures


class MultiImages(Images):

    def __init__(self, root="img"):
        super().__init__(root=root)

    def download(self):
        # map over urls and download in parallel
        self.root.mkdir()

        print("Downloading...")
        start = time.perf_counter()
        with futures.ThreadPoolExecutor() as exec:
            exec.map(self._download_image, self.urls)
        end = time.perf_counter()
        print(f"Finished in {end-start:.4} seconds")


def main():
    print("I am good")
    images = MultiImages("data/img")
    print("done")


if __name__=="__main__":
    main()
