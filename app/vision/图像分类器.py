# import torch
# import torch.nn as nn
# import torch.optim as optim
# import torchvision.models as models
# import torchvision.transforms as transforms
# from torchvision.datasets import ImageFolder
#
# # 加载预训练模型
# model = models.resnet50(pretrained=True)
# num_classes = 5  # 假设有10个类别
# num_features = model.fc.in_features
# model.fc = nn.Linear(num_features, num_classes)
#
# # 数据预处理和加载
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])
# dataset = ImageFolder(r'G:/下载/original', transform)
# dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
#
# # 初始化模型和优化器
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
#
# # 训练模型
# num_epochs = 5
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
#
# for epoch in range(num_epochs):
#     running_loss = 0.0
#     for images, labels in dataloader:
#         images = images.to(device)
#         labels = labels.to(device)
#
#         # 前向传播
#         outputs = model(images)
#         loss = criterion(outputs, labels)
#
#         # 反向传播和优化
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#
#         running_loss += loss.item()
#
#     print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(dataloader):.4f}")
#
# #保存时
# torch.save(model,'save_path')
# #加载时
# torch.load('save_path/model')

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms

# 设置随机种子，以便结果可复现
torch.manual_seed(42)

# 定义数据预处理和数据加载器
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = torchvision.datasets.ImageFolder(root=r'G:/下载/original', transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# 定义模型
model = torchvision.models.resnet18(pretrained=True)
num_classes = len(train_dataset.classes)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# 训练模型
num_epochs = 5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

for epoch in range(num_epochs):
    running_loss = 0.0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss:.4f}')

# 保存模型
torch.save(model.state_dict(), 'plant_classifier.pth')

