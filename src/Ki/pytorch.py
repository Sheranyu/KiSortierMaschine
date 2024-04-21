
from os.path import isdir
import os
import random
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
from torchvision import  transforms
from PIL import Image
from os import listdir
from configordner.settings import LaufZeitConfig
from modele.KImodels import MeinNetz
from modele.InterneDatenModele import KIModelsaverData, KiModeltrainingConfigdata
from flet import ProgressBar

class KiTraining():
    def __init__(self, progress: ProgressBar) -> None:
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
        self.progress = progress
        self.bachsize = 32
        # hier können paramter init werden
        pass

    def starte_ki_training(self, data: KIModelsaverData):
        self.kidata = data
       
        self._Dateneinlesen(data.pfad_model)
        self._train_start()

    def Set_Settings(self, configdata: KiModeltrainingConfigdata):#
        self.learnrate = float(configdata.lernrate)
        self.maxepoche = int(configdata.epoches)
        self.bachsize = int(configdata.bachsize)
        self.maxdatenseatze = int(configdata.maxdatenseatze)
        self.normalize = transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229, 0.224, 0.225])
        # self.transformation = transforms.Compose([
        #     transforms.Resize(256),transforms.CenterCrop(256),
        #     transforms.ToTensor(),
        #     self.normalize
        # ])
        self.transformation = transforms.Compose([
            transforms.Resize(256),  # Größenanpassung
            transforms.RandomHorizontalFlip(),  # Zufällige horizontale Spiegelung
            transforms.RandomRotation(degrees=10),  # Zufällige Rotation um bis zu 10 Grad
            transforms.RandomResizedCrop(224),
            #transforms.RandomAdjustSharpness(2, p=0.1),
            transforms.RandomGrayscale(),
            # Zufällige Skalierung und Zuschneiden
            #transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),  # Farbtransformationen
            transforms.ToTensor(),  # Konvertierung in Tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            # Normalisierung
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
        
    def _schreibe_label_daten(self):
        with open(self.kidata.ModelName +"_label.txt", 'w') as datei:
            for item in self.subfoldernameslist:
                datei.write(str(item) + "\n")

    def _train_start(self):
        self.model = MeinNetz(len(self.subfoldernameslist))
        if os.path.isdir(self.kidata.ModelName):
            self.loadkidata()
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.learnrate, momentum=0.9)
        self._schreibe_label_daten()
        for epoche in range(1,self.maxepoche+1):
            self.train(epoche=epoche)
            if LaufZeitConfig.istrainingactive == False:
                break


    def train(self,epoche: int):
        self.model.train()
        batch_id = 0
        for data,target in self.train_data:
            target = torch.Tensor(target)
            data = Variable(data)
            target = Variable(target)
            self.optimizer.zero_grad()
            out = self.model(data)
            criterien = F.cross_entropy 
            loss  = criterien(out, target)
            loss.backward()
            self.optimizer.step()
            batch_id += 1
            print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                epoche, batch_id * len(data), len(self.train_data),
                100. * batch_id / len(self.train_data), loss.item()))
            if LaufZeitConfig.istrainingactive == False:
                break
         
        self.progress.value = epoche/self.maxepoche
        self.savekidata()
        self.progress.update()

    def loadkidata(self):
    
        self.model = torch.load(self.kidata.ModelName + ".pt")
    
    def savekidata(self):
        torch.save(self.model, self.kidata.ModelName + ".pt")
        
    
    def _Dateneinlesen(self, main_pfad):
        folders = self.scan_subfolders(main_pfad)
        
        for folder in folders:
            if isdir(folder):
                listdata = listdir(folder)
                self.files.extend(listdata)
            else:
                print(f"{folder} ist kein gültiger Ordner.")
        
        print(self.files)
        listlenge = len(self.files)

        for i in range(len(self.files)):
            
            f = random.choice(self.files)
            self.files.remove(f)
    
            ordnersubpfad = self.getcurrentordner(f)
            self._vergleichBildmitOrdnerName_GetCurrentOrdnerName(f)
            
            img  = Image.open(main_pfad + f"/{ordnersubpfad}/{f}")
            
            img_tensor = self.transformation(img)
            self.train_data_list.append(img_tensor)
            self.target_list.append(self.target)
            print(self.target_list)
            self.target = []
            if len(self.train_data_list) >= self.bachsize:
                self.train_data.append((torch.stack(self.train_data_list), self.target_list))
                self.target_list = []
                self.train_data_list = []
                
                # print('Loaded batch ', len(self.train_data), 'of ', int(listlenge/self.bachsize))
                # print('Percentage Done: ', 100*len(self.train_data)/int(listlenge/self.bachsize), '%')
                if len(self.train_data) > self.maxdatenseatze:
                    break
