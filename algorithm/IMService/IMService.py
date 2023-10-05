import cv2
import numpy as np
import yaml

f = open('./config/config.yml', encoding="utf-8")
data = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()

# 图像灰度化
def IMGray(img, li=data["sunny"]["li"]):
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    garyImg = li[0] * r + li[1] * g + li[2] * b
    garyImg = garyImg.astype(np.uint8)
    return garyImg

# 图像二值化
def IMBin(garyImg, t=data["sunny"]["t"]):
    garyImg[garyImg < t] = 0
    garyImg[garyImg >= t] = 255
    return garyImg

# 图像投影(针对二值化图像进行投影)
def IMProject(img):

    height, width = img.shape

    # 对列求和投影
    data = img.sum(axis=0) / height
    data = data.astype(np.uint8)
    return data

# 图像距离计算
def IMDisCal(data):
    leftBegin, leftEnd, rightBegin, rightEnd = 0, 0, 0, 0
    for i in range(len(data)):
        if leftBegin == 0:
            if data[i] == 0:
                leftBegin = i
        elif leftEnd == 0:
            if data[i] == 1:
                leftEnd = i - 1
        elif rightBegin == 0:
            if data[i] == 0:
                rightBegin = i
        else:
            if data[i] == 1:
                rightEnd = i - 1
                break

    return (rightEnd + rightBegin - leftBegin - leftEnd) / 2