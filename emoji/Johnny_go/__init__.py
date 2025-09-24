from datetime import datetime
from pathlib import Path
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

# 各帧头像的位置和尺寸参数
locs = [
    [321, 27, 56, 56],
    [321, 27, 56, 56],
    [305, 5, 77, 77],
    [305, 5, 77, 77],
    [275, -5, 86, 86],
    [275, -5, 86, 86],
    [244, 41, 100, 100],
    [244, 41, 100, 100],
    [209, 129, 87, 87],
    [209, 129, 87, 87],
    [121, 145, 122, 122],
    [121, 145, 122, 122],
    [209, 129, 87, 87],
    [209, 129, 87, 87],
    [245, 39, 100, 100],
    [245, 39, 100, 100],
    [275, -5, 86, 86],
    [275, -5, 86, 86],
    [305, 4, 78, 78],
    [305, 4, 78, 78]
]

def Johnny_go(images: list[BuildImage], texts, args):
    # 用户提供的图片作为底层
    base_img = images[0].convert("RGBA")
    
    # 处理头像（圆形裁剪）
    avatar = images[0].circle().convert("RGBA")
    
    frames: list[IMG] = []
    
    # 遍历每帧，应用对应的位置参数
    for i in range(len(locs)):
        # 获取当前帧的位置参数：x坐标、y坐标、宽度、高度
        x, y, w, h = locs[i]
        
        # 加载模板帧
        template = BuildImage.open(img_dir / f"{i}.png")
        template_size = template.size
        
        # 底层图调整为模板尺寸
        frame_base = base_img.resize(template_size).copy()
        
        # 按当前帧参数调整头像大小
        resized_avatar = avatar.resize((w, h))
        
        # 1. 先贴用户底层图
        # 2. 再贴调整后的头像（按locs参数定位）
        frame_base.paste(resized_avatar, (x, y), alpha=True)
        
        # 3. 最后贴模板（模板在上层，覆盖部分区域）
        frame_base.paste(template, (0, 0), alpha=True)
        
        frames.append(frame_base.image)
    
    return save_gif(frames, 0.05)

add_meme(
    "Johnny_go",
    Johnny_go,
    min_images=1,
    max_images=1,
    keywords=["GO乔尼GO","go乔尼go","go!乔尼!go!","go！乔尼！go！"],
    date_created=datetime(2025, 9, 24),
    date_modified=datetime(2025, 9, 24),
)
