import cv2
import numpy as np

if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)

    # 使用Scharr滤波器进行边缘增强
    scharr_x = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    scharr_y = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])

    edge_x = cv2.filter2D(image, -1, scharr_x)
    edge_y = cv2.filter2D(image, -1, scharr_y)

    # 将水平和垂直增强的结果合并
    edge_enhanced = cv2.addWeighted(edge_x, 0.5, edge_y, 0.5, 0)

    # 显示原始图像和边缘增强结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Edge Enhancement (Scharr)', edge_enhanced)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
