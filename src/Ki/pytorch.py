
from os.path import isdir, join
import os
import random
from typing import Type
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image
from os import listdir

from modele.InterneDatenModele import KIModelsaverData

class MeinNetz(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super(MeinNetz,self).__init__(*args, **kwargs)
        self.conv1 = nn.Conv2d(3,6,kernel_size=5)
        self.conv2 = nn.Conv2d(6,12, kernel_size=5)
        self.conv3 = nn.Conv2d(12,18, kernel_size=5)
        self.conv4 = nn.Conv2d(18,24, kernel_size=5)
        self.fc1 = nn.Linear(3456, 1000)
        self.fc2 = nn.Linear(1000,2 )

    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x,2)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.max_pool2d(x,2)
        x = F.relu(x)
        x = self.conv3(x)
        x = F.max_pool2d(x,2)
        x = F.relu(x)
        x = self.conv4(x)
        x = F.max_pool2d(x,2)
        x = F.relu(x)
        x = x.view(-1,3456)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.sigmoid(x)

class KiTraining():
    def __init__(self) -> None:
        self.train_data_list = []
        self.target_list = []
        self.train_data = []
        self.files: list = []
        self.subfoldernameslist = []
        self.target = []
        self.maxdatenseatze = 50
        self.maxepoche = 20
        self.learnrate = 0.004
        # hier können paramter init werden
        pass

    def starte_ki_training(self, data: KIModelsaverData):
        self._Dateneinlesen(data.pfad_model)
        self._train_start()

    def Set_Settings(self):
        self.normalize = transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229, 0.224, 0.225])

        self.transformation = transforms.Compose([
            transforms.Resize(256),transforms.CenterCrop(256),
            transforms.ToTensor(),
            self.normalize
        ])

    def scan_subfolders(self,main_folder):
        subfolders = []
        # Überprüfen, ob der Hauptordner existiert und ein Verzeichnis ist
        if os.path.exists(main_folder) and os.path.isdir(main_folder):
            # Durch alle Elemente im Hauptordner iterieren
            for item in os.listdir(main_folder):
                # Den vollständigen Pfad zum Element erhalten
                self.subfoldernameslist.append(item)
                item_path = os.path.join(main_folder, item)
                # Überprüfen, ob das Element ein Verzeichnis ist
                if os.path.isdir(item_path):
                    # Wenn ja, den Ordner zur Liste der Unterordner hinzufügen
                    subfolders.append(item_path)
        else:
            print(f"{main_folder} ist kein gültiger Ordner oder existiert nicht.")
        return subfolders
    
    def _vergleichBildmitOrdnerName_GetCurrentOrdnerName(self,name_to_compare) ->str:
        ordnername = ""
        for name in self.subfoldernameslist:
            # Überprüfen, ob der Name passt
            if name == name_to_compare:
                self.target.append(1)
                ordnername = name
                  # Wenn der Name passt, füge 1 zur Ergebnisliste hinzu
            else:
                self.target.append(0) 
        return ordnername

    def _train_start(self):
        self.model = MeinNetz()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learnrate)
        for epoche in range(1,self.maxepoche):
            self.train(epoche=epoche)


    def train(self,epoche: int):
        self.model.train()
        batch_id = 0
        for data,target in self.train_data:
            target = torch.Tensor(target)
            data = Variable(data)
            target = Variable(target)
            self.optimizer.zero_grad()
            out = self.model(data)
            criterien = F.binary_cross_entropy 
            loss  = criterien(out, target)
            loss.backward()
            self.optimizer.step()
            batch_id += 1
            print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                epoche, batch_id * len(data), len(self.train_data),
                100. * batch_id / len(self.train_data), loss.item()))
        #torch.save(self.model, "katze_hunderkennung.pt")

    def _Dateneinlesen(self, main_pfad):
        folders = self.scan_subfolders(main_pfad)
        print(folders)
        for folder in folders:
            if isdir(folder):
                listdata = listdir(folder)
                self.files.extend(listdata)
            else:
                print(f"{folder} ist kein gültiger Ordner.")
        
        

        for i in range(len(self.files)):
            f = random.choice(self.files)
            self.files.remove(f)
            #geht noch nicht brauche kompletten pfad hier
            ordnername = self._vergleichBildmitOrdnerName_GetCurrentOrdnerName(f)
            img  = Image.open(main_pfad + f"/{ordnername}/{f}")
            img_tensor = self.transformation(img)
            self.train_data_list.append(img_tensor)
            
            self.target_list.append(self.target)
            if len(self.train_data_list) >= 64:
                self.train_data.append((torch.stack(self.train_data_list), self.target_list))
                self.target_list = []
                self.train_data_list = []
                self.target.clear()
                print('Loaded batch ', len(self.train_data), 'of ', int(len(listdir('./train/train/'))/64))
                print('Percentage Done: ', 100*len(self.train_data)/int(len(listdir('./train/train/'))/64), '%')
                if len(self.train_data) > self.maxdatenseatze:
                    break
