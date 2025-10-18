from datetime import datetime
from pathlib import Path
import random
from PIL import ImageDraw, ImageFont

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength, MemeFeedback
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


help_text = "图片编号，范围为 0~1，0为随机"


class Model(MemeArgsModel):
    number: int = Field(0, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--number"],
            args=[ParserArg(name="number", value="int")],
            help_text=help_text,
        ),
    ],
)


frame_configs = [
    {
        "frame_file": "0.png",
        "text_bbox": (294, 640, 652, 851),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (3.4, 3.4),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "1.png",
        "text_bbox": (317, 591, 598, 795),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (-9.9, -9.9),
        "text_color": (0, 0, 0)
    },
]


def sakiko_holdsign(images: list[BuildImage], texts: list[str], args: Model):
    text = texts[0] if texts else "站街，不卖纯馋人"

    total_num = len(frame_configs) - 1
    if args.number == 0:
        config_index = random.randint(0, total_num)
    elif 1 <= args.number <= total_num + 1:
        config_index = args.number - 1
    else:
        raise MemeFeedback(f"图片编号错误，请选择 0~{total_num + 1}")

    config = frame_configs[config_index]

    def make(imgs: list[BuildImage]) -> BuildImage:
        frame = BuildImage.open(img_dir / config["frame_file"])
        x1, y1, x2, y2 = config["text_bbox"]
        text_width = x2 - x1  # 文本框宽度
        text_height = y2 - y1  # 文本框高度
        line_spacing = 5  # 行间距（可根据需求调整）
        min_font_size = 15  # 最小字体大小（可修改）

        # 获取旋转角度
        if config["rotation_range"][0] == config["rotation_range"][1]:
            rotation_angle = config["rotation_range"][0]
        else:
            rotation_angle = random.uniform(*config["rotation_range"])
        
        text_color = config["text_color"]
        
        # 创建透明文本图像
        text_img = BuildImage.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img.image)
        
        # 加载字体并调整大小（适配多行文本）
        font_size = 150
        font = None
        # 尝试加载字体
        for font_name in config["font_families"]:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
        if not font:
            raise ValueError("未找到可用字体")
        
        # 定义文本拆分函数（按宽度拆分为多行）
        def split_text(txt, fnt, max_w):
            lines = []
            current_line = ""
            for char in txt:
                test_line = current_line + char
                test_bbox = draw.textbbox((0, 0), test_line, font=fnt)
                test_w = test_bbox[2] - test_bbox[0]
                if test_w > max_w:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
            return lines
        
        # 循环缩小字体，直到文本能放入文本框（同时满足宽度和高度）
        while font_size >= min_font_size:
            # 拆分文本为多行
            lines = split_text(text, font, text_width)
            if not lines:
                break  # 空文本处理
            
            # 计算多行文本总高度（含行间距）
            total_h = 0
            line_heights = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_h = bbox[3] - bbox[1]
                line_heights.append(line_h)
                total_h += line_h
            total_h += line_spacing * (len(lines) - 1)  # 加行间距
            
            # 检查是否同时满足宽度和高度
            if total_h <= text_height:
                break  # 符合条件，退出循环
            
            # 不满足则缩小字体
            font_size -= 1
            # 重新加载对应大小的字体
            font = None
            for font_name in config["font_families"]:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except:
                    continue
            if not font:
                raise ValueError(f"字体无法加载到大小 {font_size}")
        
        # 检查最终字体是否过小
        if font_size < min_font_size:
            raise TextOverLength(f"文本过长，无法在文本框内显示（最小字体 {min_font_size} 仍超出）")
        
        # 拆分最终文本为多行
        lines = split_text(text, font, text_width)
        # 计算总高度和每行高度（用于居中）
        total_h = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_h = bbox[3] - bbox[1]
            line_heights.append(line_h)
            total_h += line_h
        total_h += line_spacing * (len(lines) - 1)
        
        # 计算文本起始Y坐标（垂直居中）
        start_y = (text_height - total_h) // 2
        current_y = start_y
        
        # 逐行绘制文本（水平居中）
        for i, line in enumerate(lines):
            line_h = line_heights[i]
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_w = line_bbox[2] - line_bbox[0]
            line_x = (text_width - line_w) // 2  # 水平居中
            draw.text((line_x, current_y), line, font=font, fill=text_color)
            current_y += line_h + line_spacing  # 下移到下一行
        
        # 旋转文本并粘贴到原图
        rotated_text = text_img.rotate(rotation_angle, expand=True)
        paste_x = x1 + (text_width - rotated_text.width) // 2
        paste_y = y1 + (text_height - rotated_text.height) // 2
        frame.paste(rotated_text, (paste_x, paste_y), rotated_text)
        
        return frame.copy()

    return make_jpg_or_gif(images, make)


add_meme(
    "sakiko_holdsign",
    sakiko_holdsign,
    min_images=0,
    max_images=0,
    min_texts=0,
    max_texts=1,
    default_texts=["站街，不卖纯馋人"],
    args_type=args_type,
    keywords=["丰川祥子举牌","祥子举牌","小祥举牌"],
    date_created=datetime(2025, 10, 18),
    date_modified=datetime(2025, 10, 18),
)