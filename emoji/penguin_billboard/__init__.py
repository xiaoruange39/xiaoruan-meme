from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "努力搬砖中"


def penguin_billboard(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    
    try:
        frame.draw_text(
            (20, frame.height - 80, frame.width - 20, frame.height),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=50,
            min_fontsize=5,
            stroke_fill="black",
            stroke_ratio=0.01,
            lines_align="center",
            font_families=["NotoSansSC-Bold"],
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 30), (410, -30), (410, 346), (0, 330))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((410, 410), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen.rotate(0, expand=True), (160, 83), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "penguin_billboard",
    penguin_billboard,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["企鹅广告牌", "企鹅广告"],
    date_created=datetime(2025, 10, 19),
    date_modified=datetime(2025, 10, 19),
)