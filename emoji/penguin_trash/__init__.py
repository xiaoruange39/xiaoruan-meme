from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "家的归宿"


def penguin_trash(images: list[BuildImage], texts: list[str], args):
    text = texts[0] if texts else default_text
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (0, 369, 381, 423),
            text,
            max_fontsize=50,
            min_fontsize=1,
            stroke_fill="white",
            stroke_ratio=0.02,
            fill="#ffffff",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").circle().resize((120, 120), keep_ratio=True)
        return frame.copy().paste(img, (186, 142), below=True)

    return make_png_or_gif(images, make)


add_meme(
    "penguin_trash",
    penguin_trash,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["家的归宿","家的归属","企鹅垃圾桶"],
    date_created=datetime(2025, 10, 16),
    date_modified=datetime(2025, 10, 16),
)
