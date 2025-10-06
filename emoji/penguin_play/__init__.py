from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def penguin_play(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    frame = BuildImage.open(img_dir / "0.png")

    ta = "他"
    name = ta
    if texts:
        name = texts[0]
    elif args.user_infos:
        info = args.user_infos[0]
        ta = "他" if info.gender == "male" else "她"
        name = info.name or ta

    text = f"都出来一起玩{name}"
    try:
        frame.draw_text(
            (50, 706, 1029, 864),
            text,
            fill=(205, 150, 122),
            #allow_wrap=True,
            max_fontsize=100,
            min_fontsize=5,
            lines_align="left",
            font_families=["NotoSansSC-Bold"],
        )
    except ValueError:
        raise TextOverLength(name)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((348, 348)).rotate(angle=-6.5, expand=True)
        return frame.copy().paste(img, (645, 305), alpha=True, below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "penguin_play",
    penguin_play,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["企鹅指"],
    date_created=datetime(2025, 10, 6),
    date_modified=datetime(2025, 10, 6),
)
