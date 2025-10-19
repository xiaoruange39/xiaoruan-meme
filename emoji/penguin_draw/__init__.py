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

def penguin_draw(images: list[BuildImage], texts: list[str], args):

    img = images[0].convert("RGBA").resize((167, 167)).rotate(0.8, expand=True)
    
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:        
        frame.draw_text(
            (11, 306, 347, 353),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=72,
            min_fontsize=18,
            lines_align="center",
            font_families=["NotoSansSC-Regular"],
        )

        frame.paste(img, (35, 28), alpha=True, below=True)        
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "penguin_draw",
    penguin_draw,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["我要画画"],
    keywords=["企鹅画画"],
    args_type=args_type,
    date_created=datetime(2025, 10, 19),
    date_modified=datetime(2025, 10, 19),
)