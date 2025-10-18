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


help_text = "图片编号，范围为 0~4，0为随机"


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
        "text_bbox": (223, 335, 786, 664),
        "font_families": ["NotoSansSC-Bold", "FZXS14", "SimHei"],
        "rotation_range": (1.4, 1.4),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "1.png",
        "text_bbox": (303, 9, 562, 279),
        "font_families": ["NotoSansSC-Bold", "FZXS14", "SimHei"],
        "rotation_range": (-4, -4),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "2.png",
        "text_bbox": (48, 206, 329, 339),
        "font_families": ["NotoSansSC-Bold", "FZXS14", "SimHei"],
        "rotation_range": (0, 0),
        "text_color": (255, 255, 255)
    },
    {
        "frame_file": "3.png",
        "text_bbox": (320, 21, 560, 259),
        "font_families": ["NotoSansSC-Bold", "FZXS14", "SimHei"],
        "rotation_range": (-4.2, -4.2),
        "text_color": (0, 0, 0)
    },
    {
        "frame_file": "4.png",
        "text_bbox": (0, 391, 496, 658),
        "font_families": ["NotoSansSC-Bold", "FZXS14", "SimHei"],
        "rotation_range": (0, 0),
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
        text_width = x2 - x1
        text_height = y2 - y1
        
        # 获取旋转角度
        if config["rotation_range"][0] == config["rotation_range"][1]:
            rotation_angle = config["rotation_range"][0]  # 固定角度
        else:
            rotation_angle = random.uniform(*config["rotation_range"])
        
        text_color = config["text_color"]
        
        # 创建透明文本图像
        text_img = BuildImage.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img.image)
        
        # 加载字体并调整大小
        font_size = 100
        font = None
        for font_name in config["font_families"]:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
        if not font:
            raise ValueError("未找到可用字体")
        
        while font_size >= 15:
            try:
                text_bbox = draw.textbbox((0, 0), text, font=font)
                txt_w = text_bbox[2] - text_bbox[0]
                txt_h = text_bbox[3] - text_bbox[1]
                if txt_w <= text_width and txt_h <= text_height:
                    break
            except:
                pass
            font_size -= 1
            for font_name in config["font_families"]:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except:
                    continue
        
        if font_size < 15:
            raise TextOverLength(text)
        
        # 绘制文本并旋转
        text_x = (text_width - txt_w) // 2
        text_y = (text_height - txt_h) // 2
        draw.text((text_x, text_y), text, font=font, fill=text_color)
        
        rotated_text = text_img.rotate(rotation_angle, expand=True)  # 传入小数角度
        
        # 粘贴到原图
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
    date_created=datetime(2025, 10, 18),
    date_modified=datetime(2025, 10, 18),
)
