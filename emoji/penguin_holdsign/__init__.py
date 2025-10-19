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


help_text = "图片编号，范围为 0~6，0为随机"


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
        "text_bbox": (223, 350, 781, 674),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (1.4, 1.4),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "1.png",
        "text_bbox": (298, 34, 567, 264),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (-4, -4),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "2.png",
        "text_bbox": (48, 196, 329, 379),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (0, 0),
        "text_color": (255, 255, 255)
    },
    {
        "frame_file": "3.png",
        "text_bbox": (320, 36, 555, 244),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (-4.2, -4.2),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "4.png",
        "text_bbox": (0, 391, 496, 658),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (0, 0),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "5.png",
        "text_bbox": (366, 46, 643, 279),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (-2.5, -2.5),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "6.png",
        "text_bbox": (109, 188, 268, 297),
        "font_families": ["FZSEJW", "FZXS14", "SimHei"],
        "rotation_range": (-1.1, -1.1),
        "text_color": (0, 0, 0)
    }
]


def penguin_holdsign(images: list[BuildImage], texts: list[str], args: Model):
    text = texts[0] if texts else "色情消息秒回"

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
        line_spacing = 5  # 行间距
        min_font_size = 5  # 最小字体大小

        # 获取旋转角度
        if config["rotation_range"][0] == config["rotation_range"][1]:
            rotation_angle = config["rotation_range"][0]  # 固定角度
        else:
            rotation_angle = random.uniform(*config["rotation_range"])
        
        text_color = config["text_color"]
        
        # 创建透明文本图像
        text_img = BuildImage.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img.image)
        
        # 1. 加载初始字体
        font_size = 70
        font = None
        for font_name in config["font_families"]:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
        if not font:
            raise ValueError("未找到可用字体（如NotoSansSC-Bold、SimHei）")
        
        # 2. 定义文本拆分函数：按文本框宽度拆分为多行（中文按字符拆分）
        def split_text(txt, fnt, max_w):
            lines = []
            current_line = ""
            for char in txt:
                # 测试当前字符加入后是否超出宽度
                test_line = current_line + char
                test_bbox = draw.textbbox((0, 0), test_line, font=fnt)
                test_w = test_bbox[2] - test_bbox[0]
                if test_w > max_w:
                    lines.append(current_line)  # 保存当前行
                    current_line = char  # 新行从当前字符开始
                else:
                    current_line = test_line
            if current_line:  # 保存最后一行
                lines.append(current_line)
            return lines
        
        # 3. 循环缩小字体：确保多行文本总高度 ≤ 文本框高度
        while font_size >= min_font_size:
            # 拆分文本为多行
            lines = split_text(text, font, text_width)
            if not lines:
                break  # 空文本无需处理
            
            # 计算多行文本总高度（含行间距）
            total_text_h = 0
            line_heights = []  # 记录每行高度
            for line in lines:
                line_bbox = draw.textbbox((0, 0), line, font=font)
                line_h = line_bbox[3] - line_bbox[1]
                line_heights.append(line_h)
                total_text_h += line_h
            # 加上所有行间距（行数-1个间隔）
            total_text_h += line_spacing * (len(lines) - 1)
            
            # 检查是否适配文本框（总高度≤文本框高度）
            if total_text_h <= text_height:
                break  # 适配成功，退出循环
            
            # 适配失败：缩小字体并重新加载
            font_size -= 1
            font = None
            for font_name in config["font_families"]:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except:
                    continue
            if not font:
                raise ValueError(f"字体无法缩小到 {font_size} 号（请检查字体文件）")
        
        # 4. 检查字体是否过小（超出最小限制则报错）
        if font_size < min_font_size:
            raise TextOverLength(f"文本过长，最小 {min_font_size} 号字体仍无法适配（可增大min_font_size或缩小文本）")
        
        # 5. 逐行绘制文本（水平居中+整体垂直居中）
        # 重新拆分最终字体的文本（确保准确性）
        lines = split_text(text, font, text_width)
        # 重新计算总高度和每行高度
        total_text_h = 0
        line_heights = []
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_h = line_bbox[3] - line_bbox[1]
            line_heights.append(line_h)
            total_text_h += line_h
        total_text_h += line_spacing * (len(lines) - 1)
        
        # 计算垂直居中的起始Y坐标
        start_y = (text_height - total_text_h) // 2
        current_y = start_y
        
        # 逐行绘制
        for i, line in enumerate(lines):
            line_h = line_heights[i]
            # 计算该行水平居中的X坐标
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_w = line_bbox[2] - line_bbox[0]
            line_x = (text_width - line_w) // 2
            # 绘制文本
            draw.text((line_x, current_y), line, font=font, fill=text_color)
            # 下移到下一行（行高+行间距）
            current_y += line_h + line_spacing
        
        # 6. 旋转文本并粘贴到原图
        rotated_text = text_img.rotate(rotation_angle, expand=True)
        # 计算粘贴位置（文本框内居中）
        paste_x = x1 + (text_width - rotated_text.width) // 2
        paste_y = y1 + (text_height - rotated_text.height) // 2
        frame.paste(rotated_text, (paste_x, paste_y), rotated_text)
        
        return frame.copy()

    return make_jpg_or_gif(images, make)


add_meme(
    "penguin_holdsign",
    penguin_holdsign,
    min_images=0,
    max_images=0,
    min_texts=0,
    max_texts=1,
    default_texts=["色情消息秒回"],
    args_type=args_type,
    keywords=["企鹅举牌"],
    date_created=datetime(2025, 10, 11),
    date_modified=datetime(2025, 10, 19),
)
