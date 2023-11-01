import cv2
import numpy as np

if __name__ == "__main__":
    # 读取图像
    img = cv2.imread('2.jpg', cv2.IMREAD_COLOR)
    # 转化为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 执行LSD边缘检测
    lsd = cv2.createLineSegmentDetector(0)
    lines, width, prec, nfa = lsd.detect(gray)
    # 绘制线段
    for line in lines:
        x1, y1, x2, y2 = map(int, line[0])
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow('LSD', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

