# -*- coding: utf-8 -*-
# FileName: load_config.py
# Time : 2023/5/9 18:51
# Author: zzy
import os.path
from pathlib import Path

from yaml import load, SafeLoader

import os
from pathlib import Path

root_dir = os.path.abspath(os.path.dirname(__file__)).split("myflasky")[0]
PROJECT_ROOT_DIR = Path(root_dir) / "myflasky"
PROJECT_APP_DIR = PROJECT_ROOT_DIR / "app"


def load_configure(exclude=None) -> dict:
    with open(PROJECT_APP_DIR.joinpath("instance/flask_app.yaml"), encoding='utf-8') as y:
        config: dict = load(y, Loader=SafeLoader)
        if exclude:
            config.pop(exclude)
    return config


if __name__ == '__main__':
    print(PROJECT_APP_DIR)
    print(str(PROJECT_APP_DIR / "instance/flask_app.yaml"))
