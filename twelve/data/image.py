import time
import requests

from PIL import Image
from pathlib import Path


class Images:

    urls = [
        "https://images.unsplash.com/photo-1611843217333-e2e1eeb6299f",
        "https://images.unsplash.com/photo-1573261658953-8b29e144d1af",
        "https://images.unsplash.com/photo-1612051259312-eeff731fee07",
        "https://images.unsplash.com/photo-1568003134168-851bead4731a",
        "https://images.unsplash.com/photo-1609528911883-fc7e0ee63c51",
        "https://images.unsplash.com/photo-1611401138560-d4f24d0231db",
        "https://images.unsplash.com/photo-1577165216284-9d38f657975d",
        "https://images.unsplash.com/photo-1528360983277-13d401cdc186",
        "https://images.unsplash.com/photo-1599740746781-315ed467db0a",
        "https://images.unsplash.com/photo-1575315755495-963011c26509",
        "https://images.unsplash.com/photo-1595161696010-b3a866b31ee4",
        "https://images.unsplash.com/photo-1595161696730-2b02f78e68ed",
        "https://images.unsplash.com/photo-1595161610061-af4551e0d9f4",
        "https://images.unsplash.com/photo-1579964459204-3bdff32da13c",
    ]

    def __init__(self, root="img"):
        self.root = Path(root)
        self._check_download()

    def __repr__(self):
        return f"Images(root={self.root})"

    def load_data(self):
        """Load the saved images"""
        path = self.root.glob("**/*.jpg")
        imgs = [x for x in path if x.is_file()]
        return [Image.open(img) for img in imgs]

    def _check_download(self):
        """Check if the data has been downloaded"""
        if not self.root.exists():
            self.download()

    def _download_image(self, url):
        """Download an individual image"""
        start = time.perf_counter()
        imgbytes = requests.get(url).content
        img_name = Path(url).name
        img_name = f'{img_name}.jpg'
        savepath = self.root.joinpath(img_name)

        with open(savepath, 'wb') as f:
            f.write(imgbytes)

        end = time.perf_counter()
        print(f"Downloaded {img_name} in {end-start:.5} second(s).")

    def download(self):
        """Download all images from unsplash"""
        self.root.mkdir()

        print(f"Downloading images from unsplash...")
        start = time.perf_counter()

        for url in self.urls:
            self._download_image(url)

        end = time.perf_counter()
        print(f"Finished downloading in {end-start:.5} second(s).")

