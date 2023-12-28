import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.datasets import ImageFolder
import os
import torch.nn.functional as F
from torch.utils.data import DataLoader

# 高斯滤波
gaussian_filter = torch.tensor([[1, 2, 1],
                                [2, 4, 2],
                                [1, 2, 1]], dtype=torch.float32).view(1, 3, 3)
gaussian_filter /= gaussian_filter.sum()
conv_gaussian = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False, padding=1, stride=1)
conv_gaussian.weight.data = gaussian_filter

# 定义sobel水平滤波器
sobel_filter_horizontal = torch.tensor([[-1, 0, 1],
                                        [-2, 0, 2],
                                        [-1, -1, -1]], dtype=torch.float32)

# 定义sobel垂直滤波器
sobel_filter_vertical = torch.tensor([[-1, -2, -1],
                                      [0, 0, 0],
                                      [1, 2, 1]], dtype=torch.float32).view(1, 1, 3, 3)


# class Model(nn.Module):
#     def __init__(self, in_channels, out_channels, kernel_size):
#         super(Model, self).__init__()
#         # 定义高斯卷积层
#         self.conv_gaussian = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False, padding=1)
#         self.conv_gaussian.weight.data = gaussian_filter
#
#         # 水平边缘卷积
#         self.conv_sobel_horizontal = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False, padding=1)
#         self.conv_sobel_horizontal.weight.data = sobel_filter_horizontal
#
#         # 垂直边缘卷积
#         self.conv_sobel_vertical = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False, padding=1)
#         self.conv_sobel_vertical.weight.data = sobel_filter_vertical
#
#     def forward(self, x):
#         # 执行高斯滤波
#         smoothed_image = self.conv_gaussian(x)
#         # 计算边缘梯度强度
#         sobel_x = self.conv_sobel_horizontal(smoothed_image)
#         sobel_y = self.conv_sobel_vertical(smoothed_image)
#         magnitude = torch.sqrt(torch.square(sobel_x) + torch.square(sobel_y))
#         magnitude /= torch.max(magnitude)
#         magnitude *= 255
#         magnitude = magnitude.to(torch.uint8)
#         print(magnitude.shape)
#         # 计算边缘梯度方向
#         return magnitude


if __name__ == "__main__":
    x = torch.tensor([1.0, 2.0, 3.0])
    x_squared = torch.square(x) + torch.square(x)
    x_squared.sqrt_()
    print(x)
    print(x_squared)
