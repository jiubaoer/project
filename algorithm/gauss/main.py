import cv2
import numpy as np


if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)
    # 定义高斯核大小和标准差
    ksize = (5, 5)
    sigma = 1.0

    # 应用高斯滤波
    blurred_image = cv2.GaussianBlur(image, ksize, sigma)

    # 显示原始图像和处理后的图像
    cv2.imshow('Original Image', image)
    cv2.imshow('Blurred Image', blurred_image)

    # 等待用户按下任意键后关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()

