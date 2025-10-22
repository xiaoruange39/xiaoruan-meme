from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "祥子喜欢这个"


def saki_dislike(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (20, frame.height - 130, frame.width - 20, frame.height),
            text,
            max_fontsize=70,
            min_fontsize=25,
            stroke_fill="white",
            stroke_ratio=0.06,
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        points = ((0, 0), (275, 140), (275, 637), (0, 765))
        screen = (
            imgs[0]
            .convert("RGBA")
            .resize((405, 405), keep_ratio=True)
            .perspective(points)
        )
        return frame.copy().paste(screen.rotate(0, expand=True), (80, -93), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "saki_like",
    saki_like,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["小祥喜欢", "丰川祥子喜欢", "祥子喜欢"],
    date_created=datetime(2025, 10, 6),
    date_modified=datetime(2025, 10, 6),
)