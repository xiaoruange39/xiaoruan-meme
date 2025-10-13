from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def saki_service(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (27, 85, 818, 388),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=150,
            min_fontsize=30,
            stroke_fill="black",
            stroke_ratio=0.03,
            lines_align="center",
            font_families=["NotoSansSC-Bold"],
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "saki_service",
    saki_service,
    min_texts=1,
    max_texts=1,
    default_texts=["不行哦亲"],
    keywords=["小祥客服","祥子客服","丰川祥子客服"],
    date_created=datetime(2025, 10, 13),
    date_modified=datetime(2025, 10, 13),
)
