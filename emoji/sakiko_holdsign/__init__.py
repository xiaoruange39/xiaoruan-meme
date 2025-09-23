from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def raise_sign(images, texts: list[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    text_img = BuildImage.new("RGBA", (390, 265))
    try:
        text_img.draw_text(
            (10, 10, 380, 255),
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
    text_img = text_img.perspective(((5, 25), (375, -15), (375, 235), (25, 255)))
    frame.paste(text_img, (270, 615), alpha=True)
    return frame.save_jpg()


add_meme(
    "sakiko_sign",
    raise_sign,
    min_texts=1,
    max_texts=1,
    default_texts=["卖,给钱就做"],
    keywords=["丰川祥子举牌","祥子举牌","小祥举牌","举牌"],
    date_created=datetime(2022, 6, 12),
    date_modified=datetime(2023, 2, 14),
)
