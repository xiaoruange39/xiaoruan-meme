from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def penguin_controller(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (0, 460, 719, 591),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=150,
            min_fontsize=30,
            lines_align="center",
            font_families=["NotoSansSC-Bold"],
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "penguin_controller",
    penguin_controller,
    min_texts=1,
    max_texts=1,
    default_texts=["真得控制你了"],
    keywords=["企鹅手柄","企鹅控制"],
    date_created=datetime(2025, 10, 17),
    date_modified=datetime(2025, 10, 17),
)
