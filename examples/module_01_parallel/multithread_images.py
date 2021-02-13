import time
from twelve.data import Images
from concurrent import futures


class MultiThreadImages(Images):
    """Download image data using multiple threads

    Most of the work here is done by
    `twelve.data.image.Images`, where `Images` loops
    over a list of urls pointing to images on unsplash,
    downloading them one at a time. Here we overwrite
    `Images.download` in order to use multiple threads.
    This way we can speed up this I/O problem!
    """

    def __init__(self, root="img"):
        super().__init__(root=root)

    def download(self):
        self.root.mkdir()

        print("Downloading...")
        start = time.perf_counter()
        with futures.ThreadPoolExecutor() as exec:
            exec.map(self._download_image, self.urls)
        end = time.perf_counter()
        print(f"Finished in {end-start:.4} seconds")


def main():
    # Note: if data/img already exists, this will do nothing!
    images = MultiThreadImages("data/img")


if __name__=="__main__":
    main()
