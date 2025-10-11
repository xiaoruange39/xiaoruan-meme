from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def penguin_holdsign(images, texts: list[str], args):
    text = texts[0]
    
    # 1. 定义模板图上文本区域的坐标（用于最终定位）
    text_area = (223, 355, 786, 684)
    text_width = text_area[2] - text_area[0]
    text_height = text_area[3] - text_area[1]
    
    # 2. 创建与牌子等大的文本图像（透明背景）
    text_img = BuildImage.new("RGBA", (text_width, text_height))
    
    # 3. 在文本图像上绘制文字（用相对自身的坐标，而非模板图坐标）
    try:
        text_img.draw_text(
            (0, 0, text_width, text_height),
            text,
            max_fontsize=120,
            min_fontsize=10,
            allow_wrap=True,
            lines_align="center",
            font_families=["NotoSansSC-Bold", "SimHei"],
            fill="#000000",
        )
    except ValueError as e:
        if "too long" in str(e).lower():
            raise TextOverLength(text) from e
        raise
    
    # 4. 旋转文本图像（模拟手持角度）
    rotated_text = text_img.rotate(angle=1.5, expand=True)
    
    # 5. 计算旋转后文本的粘贴位置（确保中心与原牌子区域对齐）
    # 原牌子区域的中心坐标
    orig_center_x = text_area[0] + text_width // 2
    orig_center_y = text_area[1] + text_height // 2
    # 旋转后文本图像的中心坐标
    rotated_center_x = rotated_text.width // 2
    rotated_center_y = rotated_text.height // 2
    # 粘贴位置 = 原中心 - 旋转后中心（确保中心对齐）
    paste_x = orig_center_x - rotated_center_x
    paste_y = orig_center_y - rotated_center_y
    
    # 6. 加载模板图并粘贴文本
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(rotated_text, (paste_x, paste_y), alpha=True)
    
    return frame.save_jpg()


add_meme(
    "penguin_holdsign",
    penguin_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["我的很大"],
    keywords=["企鹅举牌"],
    date_created=datetime(2025, 10, 11),
    date_modified=datetime(2025, 10, 11),
)