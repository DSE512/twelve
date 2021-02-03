""""""""
import requests

from PIL import Image
from pathlib import Path


class Images:

    urls = [
        "https://images.unsplash.com/photo-1611843217333-e2e1eeb6299f",
        "https://images.unsplash.com/photo-1573261658953-8b29e144d1af",
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
        """"""
        self.savepath.mkdir(parents=True)
        for url in self.urls:
            self.download_image(url)

    def download_image(self, url):
        imgbytes = requests.get(url).content
        img_name = Path(url).name
        img_name = f'{img_name}.png'
        savepath = self.savepath.joinpath(img_name)

        with open(savepath, 'wb') as f:
            f.write(imgbytes)
            print(f'{img_name} was downloaded...')

    def load_data(self):
        """"""
        path = self.savepath.glob("**/*.png")
        imgs = [x for x in path if x.is_file()]
        self.data = [Image.open(img) for img in imgs]

