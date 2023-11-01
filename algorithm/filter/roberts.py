import cv2
import numpy as np

if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)

    # 创建Roberts滤波器的卷积核
    roberts_x = np.array([[1, 0], [0, -1]])
    roberts_y = np.array([[0, 1], [-1, 0]])

    # 使用Roberts滤波器进行边缘增强
    edge_x = cv2.filter2D(image, -1, roberts_x)
    edge_y = cv2.filter2D(image, -1, roberts_y)

    # 将水平和垂直增强的结果合并
    edge_enhanced = cv2.addWeighted(edge_x, 0.5, edge_y, 0.5, 0)

    # 显示原始图像和边缘增强结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Edge Enhancement (Roberts)', edge_enhanced)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
