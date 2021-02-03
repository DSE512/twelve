""""""""
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
    ]

    def __init__(self, savepath="img"):
        self.savepath = Path(savepath)
        self.check_download()
        self.load_data()

    def __repr__(self):
        return f"Images(savepath={self.savepath})"

    def check_download(self):
        """Check if the data has been downloaded"""
        if not self.savepath.exists():
            self.download()

    def download(self):
        """Download all images from unsplash"""
        self.savepath.mkdir()
        for url in self.urls:
            self.download_image(url)

    def download_image(self, url):
        """Download an individual image"""
        start = time.perf_counter()
        imgbytes = requests.get(url).content
        img_name = Path(url).name
        img_name = f'{img_name}.jpg'
        savepath = self.savepath.joinpath(img_name)

        with open(savepath, 'wb') as f:
            f.write(imgbytes)

        end = time.perf_counter()
        print(f"Downloaded {img_name} in {end-start:.5} second(s).")

    def load_data(self):
        """"""
        path = self.savepath.glob("**/*.jpg")
        imgs = [x for x in path if x.is_file()]
        self.data = [Image.open(img) for img in imgs]

