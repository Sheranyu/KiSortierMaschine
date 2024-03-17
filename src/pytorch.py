
from genericpath import isfile
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim


class MeinNetz(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super(MeinNetz,self).__init__(*args, **kwargs)
        self.lin1 = nn.Linear(10,10)
        self.lin2 = nn.Linear(10,10)
        
        
    def forward(self,x):
        x = F.relu(self.lin1(x))
        x = self.lin2(x)
        return x
    
    def num_flat_features(self,x):
        size = x.size()[1:]
        num = 1
        for i in size:
            num *= i
        return num

netz = MeinNetz()


if os.path.isfile("meinnetz.pt"):
    netz = torch.load("meinnetz.pt")

for i in range(100):
    x = [1,0,0,0,1,0,0,0,1,1]
    input = Variable(torch.Tensor([x for _ in range(10)]))
    

    out = netz(input)

    x = [0,1,1,1,0,1,1,1,0,0]
    target = Variable(torch.Tensor([x for _ in range(10)]))


    criterum = nn.MSELoss()

    loss = criterum(out,target)
    print(loss)
    netz.zero_grad()
    loss.backward()
    optimizer = optim.SGD(netz.parameters(),lr=0.05)
    optimizer.step()
    
torch.save(netz,"meinNetz.pt")
