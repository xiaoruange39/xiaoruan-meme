from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def anon_pointing(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        # 缩放后添加旋转处理，rotate参数为旋转角度（正值为顺时针，负值为逆时针）
        # expand=True 确保旋转后图片完整显示
        img = imgs[0].convert("RGBA").resize((560, 560)).rotate(-7.25, expand=True)
        return frame.copy().paste(img, (874, 248), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "anon_pointing",
    anon_pointing,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    keywords=["爱音指"],
    date_created=datetime(2025, 9, 24),
    date_modified=datetime(2025, 9, 24),  # 更新修改日期
)
    