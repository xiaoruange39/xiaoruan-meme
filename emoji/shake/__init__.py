from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def shake(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((946, 946))
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (47, 47), below=True)
    return frame.save_jpg()


add_meme(
    "shake",
    shake,
    min_images=1,
    max_images=1,
    keywords=["晃一晃","摇晃","晃动"],
    date_created=datetime(2025, 10, 17),
    date_modified=datetime(2025, 10, 17),
)
