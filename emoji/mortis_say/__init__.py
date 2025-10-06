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

def mortis_say(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").resize((305, 305))
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    try:        
        frame.draw_text(
            (390, 8, 941, 118),
            text,
            fill=(0, 0, 0),
            allow_wrap=True,
            max_fontsize=72,
            min_fontsize=18,
            lines_align="center",
            font_families=["NotoSansSC-Regular"],
        )

        frame.paste(img, (535, 340), alpha=True, below=True)        
    except ValueError:
        raise TextOverLength(text)
    
    return frame.save_jpg()


add_meme(
    "mortis_say",
    mortis_say,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["你看你骚的"],
    keywords=["若叶睦说", "睦说"],
    args_type=args_type,
    tags=MemeTags.mygo,
    date_created=datetime(2025, 9, 25),
    date_modified=datetime(2025, 9, 25),
)
