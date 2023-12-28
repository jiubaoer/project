import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.datasets import ImageFolder
import os
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt


class DistanceDataset(Dataset):
    # 创建数据集类, 用于加载图片和距离
    def __init__(self, csv_file, root_dir):
        # 加载图片名称 和 距离数据
        self.data = pd.read_csv(csv_file)
        # 记录图片库的路径
        self.root_dir = root_dir
        # 定义图片预处理
        self.transform = transforms.Compose([
            transforms.Grayscale(),  # 灰度化
            transforms.ToTensor(),  # 转化为tensor
        ])
        # 定义高斯核函数
        self.gaussian_filter = torch.tensor([[1, 2, 1],
                                             [2, 4, 2],
                                             [1, 2, 1]], dtype=torch.float32).view(1, 1, 3, 3)
        self.gaussian_filter /= self.gaussian_filter.sum()
        # 定义sobel水平滤波器
        self.sobel_filter_horizontal = torch.tensor([[-1, 0, 1],
                                                     [-2, 0, 2],
                                                     [-1, 0, 1]], dtype=torch.float32).view(1, 1, 3, 3) * 2
        # 定义sobel垂直滤波器
        self.sobel_filter_vertical = torch.tensor([[-1, -2, -1],
                                                   [0, 0, 0],
                                                   [1, 2, 1]], dtype=torch.float32).view(1, 1, 3, 3) * 0.5

    def __len__(self):
        return len(self.data)

    def non_maximum_supression(self, magnitude, angle):
        # 获取图像尺寸
        h, w = magnitude.shape[1:]
        # 创建与梯度向量相同大小的零向量， 用于存储NMS结果
        nms_image = torch.zeros_like(magnitude)
        # 对每一个像素判断
        for i in range(1, h-1):
            for j in range(1, w-1):
                angle_deg = angle[0, i, j] * 180 / torch.pi
                angle_deg = (angle_deg + 180) % 180

                q, r = 255, 255

                # 水平边缘
                if (0 <= angle_deg < 22.5) or (157.5 <= angle_deg <= 180):
                    q = magnitude[0, i, j + 1]
                    r = magnitude[0, i, j - 1]
                # 垂直边缘
                elif 22.5 <= angle_deg < 67.5:
                    q = magnitude[0, i + 1, j - 1]
                    r = magnitude[0, i - 1, j + 1]
                # +/- 45度边缘
                elif 67.5 <= angle_deg < 112.5:
                    q = magnitude[0, i + 1, j]
                    r = magnitude[0, i - 1, j]
                # +/- 135度边缘
                elif 112.5 <= angle_deg < 157.5:
                    q = magnitude[0, i - 1, j - 1]
                    r = magnitude[0, i + 1, j + 1]

                # 判断当前像素是否为边缘的最强部分
                if (magnitude[0, i, j] >= q) and (magnitude[0, i, j] >= r):
                    nms_image[0, i, j] = magnitude[0, i, j]
        return nms_image

    def __getitem__(self, idx):
        image_path = os.path.join(self.root_dir, self.data.iloc[idx, 0])
        image = Image.open(image_path)
        # 图片预处理
        image_tensor = self.transform(image)
        image_tensor = image_tensor.unsqueeze(0)
        # 高斯滤波
        smoothed_image = F.conv2d(image_tensor, self.gaussian_filter, stride=1, padding=1)
        # sobel水平卷积
        sobel_x = F.conv2d(smoothed_image, self.sobel_filter_horizontal, stride=1, padding=1)
        # sobel垂直卷积
        sobel_y = F.conv2d(smoothed_image, self.sobel_filter_vertical, stride=1, padding=1)
        magnitude = torch.sqrt(sobel_x ** 2 + sobel_y ** 2)
        # 映射到255范围内整数
        # magnitude /= torch.max(magnitude)
        # magnitude *= 255
        distance = self.data.iloc[idx, 1].astype('float32')
        # 维度降低
        magnitude = magnitude.squeeze(0)
        angle = torch.atan2(sobel_y, sobel_x)
        angle = angle.squeeze(0)
        # 非极大值抑制
        nms_image = self.non_maximum_supression(magnitude, angle)
        # 展示图片
        image_tensor = image_tensor.squeeze(0)
        smoothed_image = smoothed_image.squeeze(0)
        plt.subplot(3, 2, 1)
        plt.imshow(image)
        plt.title("Original Image")

        plt.subplot(3, 2, 2)
        plt.imshow(transforms.ToPILImage()(image_tensor), cmap="gray")
        plt.title("Gray Image")

        plt.subplot(3, 2, 3)
        plt.imshow(transforms.ToPILImage()(smoothed_image), cmap="gray")
        plt.title("Smoothed Image")

        plt.subplot(3, 2, 4)
        plt.imshow(transforms.ToPILImage()(magnitude), cmap="gray")
        plt.title("Magnitude Image")

        plt.subplot(3, 2, 5)
        plt.imshow(transforms.ToPILImage()(nms_image), cmap="gray")
        plt.title("Nms Image")

        plt.show()
        return magnitude, distance


class YOLOModel(nn.Module):
    def __init__(self):
        super(YOLOModel, self).__init__()
        # 640 480
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1, stride=1)
        self.conv3 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1, stride=1)
        self.fc = nn.Linear(256 * 720 * 576, 1)

    def forward(self, x):
        # relu  f(x)=max(0, x)
        x = self.conv1(x)
        x = torch.relu(x)
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


if __name__ == "__main__":
    # 创建数据集
    dataset = DistanceDataset(csv_file='dataset.csv', root_dir='images')
    dataloader = DataLoader(dataset, batch_size=24, shuffle=True)
    # 创建模型
    model = YOLOModel()
    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.01)
    # 开始训练
    epochs = 10
    for epoch in range(epochs):
        for data_batch, labels_batch in dataloader:
            labels_batch = labels_batch.view(-1, 1)
            # 前向传播
            outputs = model(data_batch)
            # 计算损失
            loss = criterion(outputs, labels_batch).float()

            # 梯度清零
            optimizer.zero_grad()

            # 反向传播
            loss.backward()

            # 更新参数
            optimizer.step()

        print(epoch)

