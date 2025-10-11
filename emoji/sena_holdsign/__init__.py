from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def sena_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (279, 817, 567, 1040),
            text,
            fill=(214, 109, 142),
            allow_wrap=True,
            max_fontsize=120,
            min_fontsize=30,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "sena_holdsign",
    sena_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["不卖,纯馋人"],
    keywords=["姬野星奏举牌", "星奏举牌"],
    date_created=datetime(2025, 9, 25),
    date_modified=datetime(2025, 9, 25),
)
