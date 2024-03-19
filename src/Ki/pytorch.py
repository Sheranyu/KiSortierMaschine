
from genericpath import isfile
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
from modele.KImodels import MeinNetz
from modele.InterneDatenModele import KIModelsaverData

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
        self.kidata = None
        # hier können paramter init werden
        pass

    def starte_ki_training(self, data: KIModelsaverData):
        self.kidata = data
        self.Set_Settings()
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
                item_path = os.path.join(main_folder, item)
                if not os.path.isfile(item_path):
                    self.subfoldernameslist.append(item)
                    # Wenn ja, den Ordner zur Liste der Unterordner hinzufügen
                    subfolders.append(item_path)
        else:
            print(f"{main_folder} ist kein gültiger Ordner oder existiert nicht.")
        return subfolders
                
    def getcurrentordner(self, name_to_compare):
        ordnername = ""
        for name in self.subfoldernameslist:
            if name in name_to_compare:
                ordnername = name                          
        return ordnername
    def _vergleichBildmitOrdnerName_GetCurrentOrdnerName(self,name_to_compare) ->str:
        for name in self.subfoldernameslist:
            # Überprüfen, ob der Name passt
            if name in name_to_compare:
                self.target.append(1)
                  # Wenn der Name passt, füge 1 zur Ergebnisliste hinzu
            else:
                self.target.append(0) 
        

    def _train_start(self):
        self.model = MeinNetz(len(self.subfoldernameslist))
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learnrate)
        for epoche in range(1,self.maxepoche):
            self.train(epoche=epoche)


    def train(self,epoche: int):
        self.model.train()
        batch_id = 0
        for data,target in self.train_data:
            print(data.size())
            
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
        self.savekidata()

    def loadkidata(self):
        self.model = torch.load(self.kidata.ModelName)
    
    def savekidata(self):
        torch.save(self.model, self.kidata.ModelName + ".pt")
        #TODO: save labelist
    
    def _Dateneinlesen(self, main_pfad):
        folders = self.scan_subfolders(main_pfad)
        
        for folder in folders:
            if isdir(folder):
                listdata = listdir(folder)
                self.files.extend(listdata)
            else:
                print(f"{folder} ist kein gültiger Ordner.")
        
        listlenge = len(self.files)

        for i in range(len(self.files)):
            f = random.choice(self.files)
            self.files.remove(f)
            #geht noch nicht brauche kompletten pfad hier
            ordnersubpfad = self.getcurrentordner(f)
            self._vergleichBildmitOrdnerName_GetCurrentOrdnerName(f)
           # print(main_pfad + f"/{ordnersubpfad}/{f}")
            
            img  = Image.open(main_pfad + f"/{ordnersubpfad}/{f}")
          
            img_tensor = self.transformation(img)
            self.train_data_list.append(img_tensor)
            
            self.target_list.append(self.target)
            self.target = []
            if len(self.train_data_list) >= 64:
                self.train_data.append((torch.stack(self.train_data_list), self.target_list))
                self.target_list = []
                self.train_data_list = []
                
                print('Loaded batch ', len(self.train_data), 'of ', int(listlenge/64))
                print('Percentage Done: ', 100*len(self.train_data)/int(listlenge/64), '%')
                if len(self.train_data) > self.maxdatenseatze:
                    break
