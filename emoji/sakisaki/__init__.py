from datetime import datetime
from pathlib import Path
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

def sakisaki(images: list[BuildImage], texts, args):
    # 处理用户头像：转换为圆形透明PNG
    avatar = images[0].convert("RGBA")
    avatar = avatar.resize((110, 110)).circle()  # 确保生成透明背景的圆形
    
    frames: list[IMG] = []
    # 各帧中头像的位置参数 (x, y, width, height)
    locs = [
        [245, 132, 41, 41],
        [245, 132, 41, 41],
        [246, 132, 41, 41],
        [237, 137, 41, 41],
        [219, 143, 41, 41],
        [204, 148, 41, 41],
        [198, 148, 41, 41],
        [190, 153, 41, 41],
        [180, 157, 41, 41],
        [162, 160, 41, 41],
        [147, 155, 41, 41],
        [128, 163, 44, 44],
        [113, 165, 44, 44],
        [87, 174, 45, 45],
        [61, 178, 45, 45],
        [50, 178, 46, 46],
        [34, 185, 48, 48],
        [22, 181, 48, 48],
        [34, 185, 48, 48],
        [50, 178, 46, 46],
        [61, 178, 45, 45],
        [87, 174, 45, 45],
        [113, 165, 44, 44],
        [140, 156, 44, 44],
        [147, 155, 41, 41],
        [147, 155, 41, 41],
        [161, 159, 41, 41],
        [180, 158, 41, 41],
        [195, 150, 41, 41],
        [199, 148, 41, 41],
        [210, 147, 41, 41],
        [229, 137, 41, 41],
        [240, 135, 41, 41]
    ]
    
    for i in range(len(locs)):
        # 1. 加载模板作为底层
        frame = BuildImage.open(img_dir / f"{i}.png")
        
        # 2. 在模板的指定位置贴上圆形头像
        pos = locs[i]
        avatar_size = (pos[2], pos[3])
        avatar_pos = (pos[0], pos[1])
        avatar_img = avatar.resize(avatar_size)
        frame.paste(avatar_img, avatar_pos, alpha=True)
        
        frames.append(frame.image)
    
    return save_gif(frames, 0.05)

add_meme(
    "sakisaki",
    sakisaki,
    min_images=1,
    max_images=1,
    keywords=["saki酱","saki","阴暗的爬行","阴暗爬行"],
    date_created=datetime(2025, 9, 24),
    date_modified=datetime(2025, 9, 24),
)
