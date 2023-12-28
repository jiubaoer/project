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
    conv1 = nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, padding=1, stride=1)
    x = torch.randn(2, 1, 576, 720)
    x /= torch.max(x)
    x *= 255
    # x = x.to(torch.uint8)
    y = conv1(x)
    print(y.shape)