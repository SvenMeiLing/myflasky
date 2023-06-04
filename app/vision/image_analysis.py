# -*- coding: utf-8 -*-
# FileName: image_analysis.py
# Time : 2023/5/26 13:38


from typing import Callable

import torch
import torchvision
from torch import nn
from PIL import Image
import torchvision.transforms as transforms

from app.scripts.load_config import PROJECT_APP_DIR


def get_analysis_index(img_url: str) -> int:
    """
    负责植物病害分析, 仅限于模型中有的分类器
    :param img_url: 图片路径
    :return: 一个索引, 0~2
    """
    model = torchvision.models.resnet18(pretrained=False)
    num_classes = 3  # 根据实际分类数进行修改
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(PROJECT_APP_DIR / "vision" / 'plant_classifier2.pth', map_location=torch.device('cpu')))
    model.eval()

    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image_path = img_url

    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0)  # 添加一个维度作为批次维度

    # 运行图像分类
    with torch.no_grad():
        outputs = model(image)

        # 获取预测结果
    _, predicted = torch.max(outputs, 1)
    predicted_class = predicted.item()
    # 输出预测结果
    return predicted_class


def retrieval_result(callback: Callable, img_url) -> str:
    """
    :param callback: 一个识别图像并分类的function
    :param img_url: 要识别的图像, 会自动传给图像分析的function
    :return:
    """
    index_tables = {
        0: "番茄叶斑病",
        1: "苹果黑星病",
        2: "葡萄黑腐病"
    }
    try:
        return index_tables.get(callback(img_url))
    except Exception as e:
        print(e)
        return "The program encountered an exception"
