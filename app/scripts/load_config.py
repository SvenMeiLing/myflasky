# -*- coding: utf-8 -*-
# FileName: load_config.py
# Time : 2023/5/9 18:51
# Author: zzy
import os.path
from pathlib import Path

from yaml import load, SafeLoader

root_dir = os.path.dirname(os.path.dirname(__file__)).split(r"\myflasky")[0]
PROJECT_ROOT_DIR = Path(root_dir)  # 项目根目录
PROJECT_APP_DIR = Path(root_dir) / "app"  # app目录


def load_configure(exclude=None) -> dict:
    with open(rf"{PROJECT_APP_DIR}\instance\flask_app.yaml", encoding='utf-8') as y:
        config: dict = load(y, Loader=SafeLoader)
        if exclude:
            config.pop(exclude)
    return config


if __name__ == '__main__':
    print(os.path.dirname(__file__).split("myflasky")[0])
