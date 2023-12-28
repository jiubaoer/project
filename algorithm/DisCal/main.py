import matplotlib.pyplot as plt
import numpy
import numpy as np
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
from PIL import Image

transform = transforms.Compose([
            transforms.Grayscale(),  # 灰度化
            transforms.ToTensor(),  # 转化为tensor
        ])

if __name__ == "__main__":
    image = Image.open('2.jpg')
    # 原始图像
    plt.subplot(1, 1, 1)
    plt.imshow(image)
    plt.title("Original Image")
    plt.show()
    # 灰度化
    image_tensor = transform(image)
    plt.subplot(1, 1, 1)
    image_pil_from_tensor = transforms.ToPILImage()(image_tensor)
    plt.imshow(image_pil_from_tensor, cmap="gray")
    plt.title("Gray Image")
    plt.show()
    # 高斯滤波
    gaussian_filter = torch.tensor([[1, 2, 1],
                                    [2, 4, 2],
                                    [1, 2, 1]], dtype=torch.float32).view(1, 1, 3, 3)
    gaussian_filter /= gaussian_filter.sum()
    image_tensor = image_tensor.unsqueeze(0)
    smoothed_image = F.conv2d(image_tensor, gaussian_filter, stride=1, padding=1)
    smoothed_image = smoothed_image.squeeze(0)
    image_pil_from_tensor = transforms.ToPILImage()(smoothed_image)
    plt.imshow(image_pil_from_tensor, cmap="gray")
    plt.title("Smoothed Image")
    plt.show()
    # 垂直增强，水平抑制



    # 非极大值抑制


    # PIL库打开图像
    image_pil = Image.open('2.jpg')
    # 打印原始图像大小
    print("原始图像大小: ", image_pil.size)
    # 预处理操作
    transform = transforms.Compose([
        transforms.ToTensor(),  # 将图片转化为张量
    ])

    # 应用预处理操作   C  H  W
    image_tensor = transform(image_pil)
    # 打印张量形状
    print("图像张量大小: ", image_tensor.shape)
    # 将张量转化为PIL图像
    image_pil_from_tensor = transforms.ToPILImage()(image_tensor)
    # 展示图片
    # image_pil_from_tensor.show()

    # 转为numpy
    image_numpy_from_tensor = numpy.squeeze(image_tensor.numpy())
    print(type(image_numpy_from_tensor))
    print(image_numpy_from_tensor.shape)

    # 按行累加
    sum_per_row = np.sum(image_numpy_from_tensor, axis=1)
    print(sum_per_row.shape)
    print(type(sum_per_row))
    print(sum_per_row.shape)
    # 最大值的索引
    max_index = np.argmax(sum_per_row)
    # 第二大值的索引
    second_max_index = np.argpartition(sum_per_row, -2)[-2]
    print(max_index, second_max_index)