# -*- coding: UTF-8 -*-
# @Author:rui.zhang1@dmall.com
# @Date:2022/11/21 09:55
import json
import os

SIZE_THRESHOLD = 512
tmp_png = 'temp.png'
png_files = []

compressedSuccessNum = 0
compressedFailNum = 0
ignoreSizeNum = 0


class Config:
    def __init__(self, dic):
        self.rootPath: str = dic['rootPath']
        self.includePath: list[str] = dic['includePath']
        self.excludePath: list[str] = dic['excludePath']

    def __str__(self):
        return f'rootPath:{self.rootPath},includePath:{self.includePath},excludePath:{self.excludePath},'


def get_conf():
    with open('config.json') as f:
        return json.load(f, object_hook=Config)


config = get_conf()


def list_pic():
    root_path = config.rootPath
    include_path = config.includePath
    exclude_path = config.excludePath

    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            print(path)
            include = False
            for in_p in include_path:
                if in_p in path:
                    include = True
                    break
            if include:
                append = True
                for ex_p in exclude_path:
                    if ex_p in path:
                        append = False
                if append and path.endswith('.png') and (not path.endswith('.9.png')):
                    png_files.append(path)


# 压缩图片
def compress_png(png_file):
    args = [
        '--quality 70-100',
        '--skip-if-larger',
        '--speed 1',
        '--nofs',
        '--strip',
        '--force',
        f'--output "{tmp_png}"',
        f'-- "{png_file}"',
    ]
    cmd = f"./pngquant {' '.join(args)}"
    print(cmd)

    exitCode = os.system(cmd)
    # 转为int值
    exitCode >>= 8
    if exitCode != 0:
        global compressedFailNum
        compressedFailNum += 1
        if exitCode == 99:
            print(f'compress fail exitCode: {exitCode}, result is larger than original, ignore result')
        elif exitCode == 98:
            print(
                f'compress fail exitCode: {exitCode}, file size gain must be greater '
                f'than the amount of quality lost, ignore result')
        else:
            print(f'exitCode: {exitCode}')
    else:
        print('compress success')
        write_origin_png_if_need(png_file)


# 压缩图片
def write_origin_png_if_need(png_file):
    global ignoreSizeNum, compressedSuccessNum
    if os.path.exists(png_file) and os.path.exists(tmp_png):
        origin_size = os.path.getsize(png_file)
        tmp_size = os.path.getsize(tmp_png)
        if origin_size - tmp_size > SIZE_THRESHOLD:
            compressedSuccessNum += 1
            with open(png_file, 'wb') as pf:
                with open(tmp_png, 'rb') as tf:
                    pf.write(tf.read())
        else:
            ignoreSizeNum += 1
    else:
        print(f'file not found')


def main():
    get_conf()
    list_pic()
    for png_file in png_files:
        compress_png(png_file)
    print(f'图片总数:{len(png_files)},压缩成功:{compressedSuccessNum},压缩失败:{compressedFailNum},忽略:{ignoreSizeNum}')
    os.remove(tmp_png)


if __name__ == '__main__':
    main()
