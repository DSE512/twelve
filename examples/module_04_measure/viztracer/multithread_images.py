import time

from twelve.data import Images
from concurrent import futures
from viztracer import VizTracer


class MultiThreadImages(Images):
    """Download image data using multiple threads"""

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
    tracer = VizTracer()
    tracer.start()

    images = MultiThreadImages("img")

    tracer.stop()
    tracer.save("viztrace_results.html") 


if __name__=="__main__":
    main()
