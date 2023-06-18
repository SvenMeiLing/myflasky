# coding: utf-8
import time

import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
from torch import nn

from app.scripts.load_config import PROJECT_APP_DIR


def get_analysis_index(
        image_path,
        pth_file=PROJECT_APP_DIR / "vision" / 'plant_classifier_new4.2.pth'
):
    """
    提供图像路径, 模型文件, 返回 -> 病害名称, 时间消耗, 正确几率,
    :param image_path: 需要识别的图像路径
    :param pth_file: 使用的模型文件
    :return: (name, time_consume, rate)
    """
    model = torchvision.models.resnet18(pretrained=False)
    num_classes = 3
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    state_dict = torch.load(pth_file, map_location=torch.device('cpu'))

    new_state_dict = {}
    for key in state_dict.keys():
        if key.startswith('fc.1'):
            new_key = key.replace('fc.1', 'fc')
        else:
            new_key = key.replace('fc.weight', 'fc.0.weight').replace('fc.bias', 'fc.0.bias')
        new_state_dict[new_key] = state_dict[key]

    model.load_state_dict(new_state_dict)

    model.eval()

    dataset = ['番茄叶斑病', '苹果黑星病', '葡萄黑腐病']
    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  # 随机水平翻转
        transforms.RandomRotation(10),  # 随机旋转
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    start = time.time()
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0)

    # 图像分类
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)
        predicted_class = predicted.item()

    class_labels = dataset
    predicted_label = class_labels[predicted_class]
    confidence = torch.softmax(outputs, dim=1)[0][predicted_class].item()
    print(confidence)
    return predicted_label, time.time() - start, confidence
