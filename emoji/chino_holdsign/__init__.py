from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def chino_holdsign(images, texts: list[str], args):
    text = texts[0]
    
    # 1. 定义文本绘制区域的左上角和右下角坐标（用于定位文字范围）
    # 格式：(左上角x, 左上角y, 右下角x, 右下角y)
    text_area = (5, 5, 470, 320)
    text_width = text_area[2] - text_area[0]  # 计算文本区域宽度
    text_height = text_area[3] - text_area[1]  # 计算文本区域高度
    
    # 2. 创建文本图像（尺寸与文本区域一致）
    text_img = BuildImage.new("RGBA", (text_width, text_height))
    
    # 3. 在文本区域内绘制文字（用左上角和右下角定位）
    try:
        text_img.draw_text(
            text_area,  # 直接使用左上角和右下角定义的区域
            text,
            max_fontsize=170,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            font_families=["FZShaoEr-M11S"],
            fill="#51201b",
        )
    except ValueError:
        raise TextOverLength(text)  # 文本过长时抛出异常
    
    # 4. 旋转文本图像
    # expand=True：确保旋转后图像完整显示，不被截断
    rotated_text = text_img.rotate(angle=20, expand=True)
    
    # 5. 加载模板图，将旋转后的文本粘贴到指定位置
    frame = BuildImage.open(img_dir / "0.png")
    # 粘贴位置：(x, y)
    frame.paste(rotated_text, (5, 100), alpha=True)
    
    return frame.save_jpg()


add_meme(
    "chino_holdsign",
    chino_holdsign,
    min_texts=1,
    max_texts=1,
    default_texts=["卖"],
    keywords=["智乃举牌", "香风智乃举牌"],
    date_created=datetime(2025, 9, 25),
    date_modified=datetime(2025, 9, 25),
)