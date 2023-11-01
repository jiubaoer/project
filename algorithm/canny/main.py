import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# 自定义Canny边缘检测模型
class CannyEdgeDetection(nn.Module):
    def __init__(self):
        super(CannyEdgeDetection, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=5, padding=2)
        self.conv3 = nn.Conv2d(64, 1, kernel_size=5, padding=2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.conv3(x)
        return x


if __name__ == "__main__":
    # 加载图像
    image_path = '2.jpg'
    image = Image.open(image_path).convert('L')  # 转为灰度图
    image = transforms.ToTensor()(image).unsqueeze(0)

    # 初始化模型
    model = CannyEdgeDetection()

    # 加载预训练模型权重（可选）
    # model.load_state_dict(torch.load('canny_edge_detection.pth'))

    # 边缘检测
    with torch.no_grad():
        edge_map = model(image)

    # 将输出转换为图像格式
    edge_map = edge_map.squeeze().cpu().numpy()
    edge_map = (edge_map - np.min(edge_map)) / (np.max(edge_map) - np.min(edge_map))

    # 显示原始图像和边缘检测结果
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image.squeeze().cpu().numpy(), cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(edge_map, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis('off')

    plt.show()

