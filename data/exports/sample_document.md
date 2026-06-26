# 深度学习课程讲解文档：卷积神经网络（CNN）

> 本文档由 MultiAgent 学习系统自动生成，针对学生画像中"CNN 架构"子知识点掌握度较低（70分）的情况，提供针对性讲解。

---

## 一、学习目标

通过本文档的学习，你将能够：

1. 理解卷积神经网络的基本工作原理
2. 掌握经典 CNN 架构（LeNet、AlexNet、VGG、ResNet）的设计思想
3. 理解残差连接如何解决深层网络训练问题
4. 能够使用 PyTorch 搭建一个简单的 CNN 模型

---

## 二、知识讲解

### 2.1 为什么需要 CNN 架构设计？

单独的卷积层和池化层只能提取局部特征，要构建能够解决实际问题的深度模型，需要将多个卷积层、池化层和全连接层以特定方式组合起来，形成**网络架构**。

好的架构设计能够：
- 提取从简单到复杂的层次化特征
- 控制模型参数量，防止过拟合
- 加速训练收敛

### 2.2 经典 CNN 架构演进

#### LeNet-5（1998，Yann LeCun）

| 层级 | 类型 | 说明 |
|------|------|------|
| 输入 | 图像 | 32×32 灰度图像 |
| C1 | 卷积 | 6 个 5×5 卷积核 |
| S2 | 池化 | 2×2 平均池化 |
| C3 | 卷积 | 16 个 5×5 卷积核 |
| S4 | 池化 | 2×2 平均池化 |
| C5 | 卷积 | 120 个 5×5 卷积核 |
| F6 | 全连接 | 84 个神经元 |
| 输出 | 全连接 | 10 个神经元（对应 10 个数字） |

> 💡 **要点**：LeNet 奠定了"卷积-池化-卷积-池化-全连接"的基本范式。

#### AlexNet（2012，ImageNet 冠军）

创新点：
- 使用 **ReLU** 激活函数（替代 Sigmoid，加速训练）
- 引入 **Dropout** 防止过拟合
- 使用 **GPU** 进行并行训练
- 网络深度：8 层（5 个卷积层 + 3 个全连接层）

```python
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            # Conv1: 96 个 11×11 卷积核，stride=4
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # Conv2: 256 个 5×5 卷积核
            nn.Conv2d(96, 256, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # Conv3, Conv4, Conv5: 3×3 卷积核
            nn.Conv2d(256, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
```

#### VGGNet（2014）

核心思想：**全部使用 3×3 小卷积核堆叠**，增加深度但保持参数量合理。

> 💡 **为什么要使用小卷积核？**
> 两个 3×3 卷积核的感受野等于一个 5×5 卷积核，但参数量更少，非线性更多。

| 架构 | 层数 | 说明 |
|------|------|------|
| VGG-16 | 16 层 | 最常用版本 |
| VGG-19 | 19 层 | 更深版本 |

#### ResNet（2015，何恺明）

核心创新：**残差连接（Skip Connection）**

\[
\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{x}
\]

解决的问题：当网络超过一定深度后，继续增加层数反而导致性能下降（非过拟合，而是优化困难）。

残差连接使得梯度可以直接反向传播到浅层，缓解了梯度消失问题。

```python
class ResNetBlock(nn.Module):
    """ResNet 基础残差块"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResNetBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        # 当维度不匹配时使用 1×1 卷积调整
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Conv2d(in_channels, out_channels,
                                      kernel_size=1, stride=stride)
    
    def forward(self, x):
        identity = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity   # 残差连接
        out = self.relu(out)
        return out
```

### 2.3 各架构对比

| 架构 | 年份 | 深度 | 创新点 | 参数量 |
|------|------|------|--------|--------|
| LeNet-5 | 1998 | 7 层 | 卷积池化范式 | ~60K |
| AlexNet | 2012 | 8 层 | ReLU、Dropout、GPU | ~60M |
| VGG-16 | 2014 | 16 层 | 小卷积核堆叠 | ~138M |
| ResNet-50 | 2015 | 50 层 | 残差连接 | ~25M |

---

## 三、代码实践

### 任务：使用 PyTorch 搭建一个简单 CNN 进行 MNIST 分类

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 定义 CNN 模型
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            # 第一卷积块
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 输出: (32, 14, 14)
            # 第二卷积块
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 输出: (64, 7, 7)
        )
        self.fc_layers = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x

# 训练函数（简化版）
def train(model, dataloader, epochs=5, lr=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
        
        print(f"Epoch {epoch+1}/{epochs} | "
              f"Loss: {total_loss/len(dataloader):.4f} | "
              f"Acc: {100.*correct/total:.2f}%")

# 运行训练（需要准备 MNIST 数据）
# transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
# train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
# train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
# model = SimpleCNN()
# train(model, train_loader)
```

---

## 四、知识检测

请回答以下问题，检验你的学习效果：

1. **（基础）** 为什么 VGGNet 全部使用 3×3 卷积核而不是更大的卷积核？
2. **（进阶）** ResNet 的残差连接是如何解决深层网络训练困难的？请用数学公式说明梯度传播过程。
3. **（应用）** 如果你要设计一个用于医学影像分割的 CNN，你会选择哪种架构作为基础？为什么？

---

## 五、推荐资源

- 📹 视频：[3Blue1Brown - 卷积神经网络可视化](https://www.bilibili.com/video/BV1bx411M7Zx/)
- 📄 论文：He et al., "Deep Residual Learning for Image Recognition" (ResNet 原论文)
- 💻 代码：[PyTorch 官方 ResNet 实现](https://github.com/pytorch/vision/blob/main/torchvision/models/resnet.py)

---

*本文档由 MultiAgent 学习系统生成，最后更新时间：2024-12-20*
