import cv2
import matplotlib.pyplot as plt
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


if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)
    # 高斯滤波, 取出噪声
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    # 可视化结果
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Original Image")

    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap="gray")
    plt.title("Canny Edges")

    plt.show()

