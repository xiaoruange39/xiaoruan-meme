from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def dusk_marriage(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        # 缩放后添加旋转处理，rotate参数为旋转角度（正值为顺时针，负值为逆时针）
        # expand=True 确保旋转后图片完整显示
        img = imgs[0].convert("RGBA").resize((126, 215))
        return frame.copy().paste(img, (67, 290), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "dusk_marriage",
    dusk_marriage,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    keywords=["结婚","跟这个结婚"],
    date_created=datetime(2025, 10, 5),
    date_modified=datetime(2025, 10, 5),  # 更新修改日期
)
    