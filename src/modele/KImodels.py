
import torch.nn as nn
import torch.nn.functional as F



class MeinNetz(nn.Module):
    def __init__(self, outputs, *args, **kwargs):
        super(MeinNetz, self).__init__(*args, **kwargs)
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 12, kernel_size=5)
        self.conv3 = nn.Conv2d(12, 18, kernel_size=5)
        self.fc1 = nn.Linear(18 * 4 * 4, 1000)  # 18 channels * 4x4 spatial dimensions
        self.fc2 = nn.Linear(1000, outputs)
        self.dropout = nn.Dropout(p=0.5)  # Dropout mit einer Wahrscheinlichkeit von 0.5

    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = self.conv3(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = x.view(-1, 18 * 4 * 4)  # Reshape, um die richtige Größe für die lineare Schicht zu erhalten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # Dropout-Schicht angewendet
        x = self.fc2(x)
        return x