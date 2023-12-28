import cv2
import numpy as np

if __name__ == "__main__":
    image = cv2.imread("../pytorch/images/2.jpg", cv2.IMREAD_GRAYSCALE)

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # 计算边缘梯度强度和方向
    magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    angle = np.arctan2(sobel_y, sobel_x)
    print(angle)

    # 保留垂直方向的边缘
    vertical_mask = np.logical_or(angle <= -np.pi/3, angle >= np.pi/3)
    print(vertical_mask.shape)
    print(vertical_mask)
    vertical_edges = magnitude * vertical_mask

    # 将梯度强度映射到0-255范围
    vertical_edges = np.uint8(255 * vertical_edges / np.max(vertical_edges))

    # 将梯度强度映射到0-255范围
    magnitude = np.uint8(255 * magnitude / np.max(magnitude))

    # 显示原始图像和边缘检测结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Sobel Edge Detection', magnitude)
    cv2.imshow('vertical Edges Detection', vertical_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()