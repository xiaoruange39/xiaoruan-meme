from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def saki_laborer(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA")
        
        # 创建frame副本
        result_frame = frame.copy()
        
        # 图片粘贴
        img = img.resize((317, 317)).rotate(28.34, expand=True)
        result_frame.paste(img, (49, 49), alpha=True, below=True)
        
        return result_frame

    return make_jpg_or_gif(images, make)


add_meme(
    "saki_laborer",
    saki_laborer,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["祥子打工","丰川祥子打工"],
    date_created=datetime(2025, 9, 2),
    date_modified=datetime(2025, 9, 25),
)