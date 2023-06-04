# coding=utf-8
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

# 创建模型对象并加载保存的参数
from torch import nn

model = torchvision.models.resnet18(pretrained=False)
num_classes = 5  # 根据实际分类数进行修改
model.fc = nn.Linear(model.fc.in_features, num_classes)

model.load_state_dict(torch.load('plant_classifier.pth', map_location=torch.device('cpu')))
# map_location=torch.device('cpu')我的电脑不加这个运行不了报错:
#   Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False.
#   If you are running on a CPU-only machine, please use torch.
#   load with map_location=torch.device('cpu') to map your storages to the CPU.

model.eval()

# 数据预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

import os

# 指定文件夹路径
folder_path = r'../upload/'

image_path = r'../upload/plant1.jpeg'  # 替换为实际的图像路径
print(image_path)
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
print(f'The predicted class index: {predicted_class}')

# 获取文件夹中的所有文件名称
file_names = os.listdir(folder_path)
# for file in file_names:
# # 加载和预处理图像
#     image_path = 'G:\BaiduNetdiskDownload\pytorch\锈病\\'+file  # 替换为实际的图像路径
#     print(image_path)
#     image = Image.open(image_path)
#     image = transform(image)
#     image = image.unsqueeze(0)  # 添加一个维度作为批次维度
#
#     # 运行图像分类
#     with torch.no_grad():
#         outputs = model(image)
#
#     # 获取预测结果
#     _, predicted = torch.max(outputs, 1)
#     predicted_class = predicted.item()
#
# # 输出预测结果
#     print(f'The predicted class index: {predicted_class}')
