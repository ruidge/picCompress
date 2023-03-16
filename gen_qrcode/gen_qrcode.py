# -*- coding: UTF-8 -*-
# @Author:rui.zhang1@dmall.com
# @Date:2023/3/16 16:03
import os
import sys

import qrcode
from PIL import Image, ImageFont, ImageDraw


def make_qrcode(text):
    qr = qrcode.QRCode(version=10,
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=8, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def add_image_to_center(back_image, logo_image):
    qrcode_size = back_image.size[0]
    # 创建一个qrcode大小的背景，用于解决黑色二维码粘贴彩色logo显示为黑白的问题。
    qr_back = Image.new('RGBA', back_image.size, 'white')
    qr_back.paste(back_image)
    logo_background_size = int(qrcode_size / 4)
    # 创建一个尺寸为二维码1/4的白底logo背景
    logo_background_image = Image.new('RGBA', (logo_background_size, logo_background_size), 'white')
    # logo与其白底背景设置背景尺寸1/20的留白
    logo_offset = int(logo_background_size / 20)
    logo_size = int(logo_background_size - logo_offset * 2)
    # 将 logo 缩放至适当尺寸
    resized_logo = logo_image.resize((logo_size, logo_size))
    # 将logo添加到白色背景
    logo_background_image.paste(resized_logo, box=(logo_offset, logo_offset))
    # 将白色背景添加到二维码图片
    logo_background_offset = int((qrcode_size - logo_background_size) / 2)
    qr_back.paste(logo_background_image, box=(logo_background_offset, logo_background_offset))
    return qr_back


def add_text_to_img(back_image, text):
    qrcode_size = back_image.size[0]
    logo_width = int(qrcode_size / 4)
    y = int(qrcode_size / 2 + logo_width / 2 - 20)
    x = int(qrcode_size / 2 - logo_width / 2 + 10)
    draw = ImageDraw.Draw(back_image)
    font_style = ImageFont.FreeTypeFont(size=15)
    draw.text((x, y), text, fill=(255, 104, 10), font=font_style)
    return back_image


def main():
    if len(sys.argv) < 2:
        print("Please input a url as parameter!!!")
        exit()

    content = sys.argv[1]

    path = os.path.split(os.path.realpath(__file__))[0]
    logo_image_file = os.path.join(path, 'android_logo.png')
    with Image.open(logo_image_file) as logo_image:
        qr_code = make_qrcode(content)
        qr_code_with_logo = add_image_to_center(qr_code, logo_image)
        qr_code_with_logo_type = add_text_to_img(qr_code_with_logo, "release")
        if os.path.isfile("dmall.png"):
            os.remove("dmall.png")
        qr_code_with_logo_type.save('dmall.png')


if __name__ == '__main__':
    main()
