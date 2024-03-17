from genericpath import isfile
import os
from typing import Type
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

#wenn grafikarte genutzt wird
#kwargs = {"num_workers": 1, "pin_memory": True}


#bei nicht benutzung der grafikarte
kwargs = {}

trainloader = DataLoader(datasets.MNIST("data", train=True, download=True, 
                                   transform=transforms.Compose([transforms.ToTensor(), 
                                   transforms.Normalize((0.1307,), (0.3081,))])),
                                    batch_size=64,shuffle=True, **kwargs
                    )

testloader = DataLoader(datasets.MNIST("data", train=False, download=False, 
                                   transform=transforms.Compose([transforms.ToTensor(), 
                                   transforms.Normalize((0.1307,), (0.3081,))])),
                                    batch_size=64,shuffle=True, **kwargs
                    )


class MeinNetz(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super(MeinNetz,self).__init__(*args, **kwargs)
        self.conv1 = nn.Conv2d(1,10,kernel_size=5)
        self.conv2 = nn.Conv2d(10,20, kernel_size=5)
        self.conv_dropout = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 60)
        self.fc2 = nn.Linear(60,10)
        
        
    def forward(self,x):
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)
        x = F.relu(x)
        x = self.conv2(x)
        x = self.conv_dropout(x)
        
        x = F.max_pool2d(x)
        x = F.relu(x)
        return x
    
    def num_flat_features(self,x):
        size = x.size()[1:]
        num = 1
        for i in size:
            num *= i
        return num

model = MeinNetz()

optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.8)





def train(epoch: int):
    model.train()
    for batch_id, (data, target) in enumerate(trainloader):
        data = Variable(data)
        target = Variable(target)
        optimizer.zero_grad()
        out = model(data)
        criterien = F.nll_loss
        loss  = criterien(out, target)
        loss.backward()
        optimizer.step()
        print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
            epoch, batch_id * len(data), len(trainloader.dataset),
            100. * batch_id / len(trainloader), loss.item()))

for epoch in range(30):
    train(epoch)
        

