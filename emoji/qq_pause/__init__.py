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

def qq_pause(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").resize((1024, 1024))
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:        
        frame.draw_text(
            (381, 777, 905, 839),
            text,
            fill=(255, 255, 255),
            allow_wrap=True,
            max_fontsize=72,
            min_fontsize=18,
            lines_align="center",
            font_families=["033-上首方糖体"],
        )

        frame.paste(img, (0, 0), alpha=True, below=True)        
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "qq_pause",
    qq_pause,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["你好，该用户已放假，请节后再说"],
    keywords=["暂停营业"],
    args_type=args_type,
    tags=MemeTags.mihoyo,
    date_created=datetime(2025, 10, 15),
    date_modified=datetime(2025, 10, 15),
)