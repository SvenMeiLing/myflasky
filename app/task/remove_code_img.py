# -*- coding: utf-8 -*-
# FileName: remove_code_img.py
# Time : 2023/6/18 22:56
# Author: zzy
import os

from app.scripts.load_config import PROJECT_ROOT_DIR


def del_img(
        code_dir=PROJECT_ROOT_DIR / "static" / "code_img",
        keep_count=10
):
    # 获取该文件夹下所有文件的修改时间
    files = [
        (  # 拼接每个文件的绝对路径, 获取文件修改时间
            os.path.join(code_dir, f), os.path.getmtime(os.path.join(code_dir, f))
        ) for f in
        os.listdir(code_dir)  # 遍历出文件列表
    ]

    # 按照修改时间对文件进行排序，获取要删除的文件路径
    files_to_remove = sorted(files, key=lambda x: x[1])[:-keep_count]  # 默认删除后10个
    print(files)

    # 删除文件
    for file_path, mtime in files_to_remove:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")


if __name__ == '__main__':
    print(PROJECT_ROOT_DIR)
    del_img()
