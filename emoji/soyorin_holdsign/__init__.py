from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def soyorin_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (283, 545, 759, 892),
            text,
            fill=(0, 0, 0),
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
    "soyorin_holdsign",
    soyorin_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["哦内该不要抛弃我"],
    keywords=["长崎爽世举牌", "爽世举牌", "素世举牌", "长崎素世举牌"],
    tags=mygo,
    date_created=datetime(2025, 9, 23),
    date_modified=datetime(2025, 9, 23),
)
