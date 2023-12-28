# Sobel

```python
image = cv2.imread("2.jpg", cv2.IMREAD_GRAYSCALE)

sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# 计算边缘梯度强度和方向
magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
angle = np.arctan2(sobel_y, sobel_x)

# 将梯度强度映射到0-255范围
magnitude = np.uint8(255 * magnitude / np.max(magnitude))

# 显示原始图像和边缘检测结果
cv2.imshow('Original Image', image)
cv2.imshow('Sobel Edge Detection', magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()
```





> 零填充



> 水平卷积核

```python
-1  0  1
-2  0  2
-1  0  1
```

> 垂直卷积核

```cmd
-1 -2 -1
 0  0  0
 1  2  1
```





通过两个卷积核分别计算在水平方向和垂直方向的亮度梯度, 之后计算两个梯度的合成梯度和方向





# pytorch 



## nn.Conv2d 和 F.Conv2d

**F.Conv2d**

```python
import torch.nn.functional as F
input_tensor = torch.randn(1, 1, 28, 28)
conv_kernel = torch.randn(1, 1, 3, 3)
conv_output = F.conv2d(input_tensor, conv_kernel, stride=1, padding=0)
```

- pytorch中的functional模块, F.conv2d是该模块卷积函数
- 是一个函数, 不是类, 可以直接调用, 不需要实例化对象
- 接收输入张量和卷积核张量, 以及其他参数

**nn.Conv2d**

```python
import torch.nn as nn
conv_layer = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=0)

# 对输入进行卷积
input_tensor = torch.randn(1, 1, 28, 28)
conv_output = conv_layer(input_tensor)
```

- nn 表示pytorch中的neural networks模块, nn.Conv2d是该模块的二维卷积层类
- 是一个类, 需要实例化对象才能使用
- 更常用于构建神经网络模型, 可以与其它层一起使用, 不仅仅是一个独立的函数调用

## 卷积核

通常都是四维

- 输出通道数 out channels : 卷积核的数量, 决定输出通道数
- 输入通道数 in channels : 输入数据的通道数, 卷积层接收的通道数
- 卷积核高度 kernel height
- 卷积核宽度 kernel width
