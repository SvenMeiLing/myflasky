# -*- coding: utf-8 -*-
# FileName: code.py
# Time : 2023/3/31 22:46
# Author: zzy
import random
from os import path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.scripts.load_config import PROJECT_ROOT_DIR

codeImgPath = path.join(PROJECT_ROOT_DIR, r"static\code_img\code.png")
ttf_path = path.join(PROJECT_ROOT_DIR, r"static\ttf\Monaco.ttf")


def check_code(width=128, height=38, char_length=5, font_file=ttf_path, font_size=28):
    code = []
    img = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 25))
    draw = ImageDraw.Draw(img, mode="RGBA")

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 8, 98, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, "".join(code)


if __name__ == '__main__':
    _, code = check_code()
    print(code)
