import torch
import torch.nn as nn
from torchvision import models


class CustomResNet(nn.Module):
    def __init__(self):
        super(CustomResNet, self).__init__()
        resnet = models.resnet18(pretrained=True)

        # Freeze all layers in the network
        for param in resnet.parameters():
            param.requires_grad = False

        # Replace the last fully connected layer
        # ResNet18's fc layer has 512 input features
        num_ftrs = resnet.fc.in_features

        # resnet.fc = nn.Linear(num_ftrs, 3)
        resnet.fc = nn.Linear(num_ftrs, 1)

        self.resnet = resnet

    def forward(self, x):
        return torch.sigmoid(self.resnet(x))


class CustomMultiClassResNet(nn.Module):
    def __init__(self, n_classes):
        super(CustomMultiClassResNet, self).__init__()
        resnet = models.resnet18(pretrained=True)

        # Freeze all layers in the network
        for param in resnet.parameters():
            param.requires_grad = False

        # Replace the last fully connected layer
        # ResNet18's fc layer has 512 input features
        num_ftrs = resnet.fc.in_features

        resnet.fc = nn.Linear(num_ftrs, n_classes)  # Output for multi-class classification

        self.resnet = resnet

    def forward(self, x):
        return self.resnet(x)
