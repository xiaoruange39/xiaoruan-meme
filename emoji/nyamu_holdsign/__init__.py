from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def nyamu_sign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    text_img = BuildImage.new("RGBA", (360, 290))
    try:
        text_img.draw_text(
            (10, 10, 350, 290),
            text,
            max_fontsize=80,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
            fill="#51201b",
        )
    except ValueError:
        raise TextOverLength(text)
    text_img = text_img.perspective(((10, -35), (390, 30), (350, 325), (-40, 250)))
    frame.paste(text_img, (280, 555), alpha=True)
    return frame.save_jpg()


add_meme(
    "nyamu_sign",
    nyamu_sign,
    min_texts=1,
    max_texts=1,
    default_texts=["站街,不卖纯馋人"],
    keywords=["喵梦举牌","祐天寺若麦举牌"],
    date_created=datetime(2025, 9, 23),
    date_modified=datetime(2025, 9, 23),
)
