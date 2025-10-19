from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def penguin_thinking(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (75, 81, 357, 206),
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
    "penguin_thinking",
    penguin_thinking,
    min_texts=1,
    max_texts=1,
    default_texts=["叽里咕噜说啥呢"],
    keywords=["企鹅思考"],
    date_created=datetime(2025, 10, 19),
    date_modified=datetime(2025, 10, 19),
)
