from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def penguin_book(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")

    text = texts[0] if texts else "审美积累中"

    try:
        frame.draw_text(
            (16, 16, 510, 462),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=80,
            min_fontsize=15,
            lines_align="left",
            font_families=["FZXS14"],
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA")
        
        # 创建frame副本
        result_frame = frame.copy()
        
        # 第一次粘贴
        img1 = img.resize((413, 384)).rotate(15, expand=True)
        result_frame.paste(img1, (430, 590), alpha=True, below=True)
        
        # 第二次粘贴
        img2 = img.resize((150, 460)).rotate(20, expand=True)
        result_frame.paste(img2, (210, 580), alpha=True, below=True)
        
        return result_frame

    return make_jpg_or_gif(images, make)


add_meme(
    "penguin_book",
    penguin_book,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["企鹅看书"],
    date_created=datetime(2025, 10, 27),
    date_modified=datetime(2025, 10, 27),
)