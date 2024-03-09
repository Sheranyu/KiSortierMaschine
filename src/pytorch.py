import torch
import torch.nn as nn
import torch.nn.functional as F

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

print(netz)

# print(torch.add(x,y))