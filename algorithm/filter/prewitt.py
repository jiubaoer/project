import cv2
import numpy as np

if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)

    # 使用Prewitt滤波器进行边缘增强
    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

    enhanced_image_x = cv2.filter2D(image, -1, prewitt_x)
    enhanced_image_y = cv2.filter2D(image, -1, prewitt_y)

    # 将水平和垂直增强的结果合并
    enhanced_image = cv2.addWeighted(enhanced_image_x, 0.5, enhanced_image_y, 0.5, 0)

    # 显示原始图像和边缘增强结果
    cv2.imshow('Original Image', image)
    cv2.imshow('Edge Enhancement (Prewitt)', enhanced_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
