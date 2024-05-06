
import torch.nn as nn
import torch.nn.functional as F



class MeinNetz(nn.Module):
    def __init__(self, outputs, *args, **kwargs):
        super(MeinNetz, self).__init__(*args, **kwargs)
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 12, kernel_size=5)
        self.conv3 = nn.Conv2d(12, 18, kernel_size=5)
        self.conv4 = nn.Conv2d(18, 24, kernel_size=5)  # Neu hinzugefügte Convolutional-Schicht
        self.fc1 = nn.Linear(24 * 10 * 10, 1500)  # Aktualisierte Eingangsgröße für die erste lineare Schicht
        self.fc2 = nn.Linear(1500, outputs)
        self.dropout = nn.Dropout(p=0.3)

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
        x = self.conv4(x)  # Neue Convolutional-Schicht
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = x.view(-1, 24 * 10 * 10)  # Aktualisierter Reshape für die erste lineare Schicht
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x