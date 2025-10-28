from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image
from PIL.Image import Image as IMG

from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"

class Model(MemeArgsModel):
    pass

args_type = MemeArgsType(
    args_model=Model,
    parser_options=[],
)

def penguin_service(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").resize((366, 366))
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:        
        frame.draw_text(
            (5, 1096, 1248, 1240),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=150,
            min_fontsize=18,
            lines_align="center",
            font_families=["NotoSansSC-Regular"],
        )

        frame.paste(img, (253, 365), alpha=True, below=True)        
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "penguin_service",
    penguin_service,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["正在提供银铛服务"],
    keywords=["企鹅服务员", "企鹅服务", "企鹅上菜", "企鹅餐盘"],
    args_type=args_type,
    date_created=datetime(2025, 10, 28),
    date_modified=datetime(2025, 10, 28),
)
