from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def amamiya_holdsign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    text_img = BuildImage.new("RGBA", (785, 455))
    try:
        text_img.draw_text(
            (10, 10, 775, 445),
            text,
            max_fontsize=150,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            font_families=["NotoSansSC-Bold"],
            fill="#000000",
        )
    except ValueError:
        raise TextOverLength(text)
    text_img = text_img.perspective(((35, -5), (775, 45), (730, 480), (5, 405)))
    frame.paste(text_img, (157, 5), alpha=True)
    return frame.save_jpg()


add_meme(
    "amamiya_holdsign",
    amamiya_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["街头演讲中"],
    keywords=["莲举牌","雨宫莲举牌"],
    date_created=datetime(2025, 10, 12),
    date_modified=datetime(2025, 10, 12),
)