
import time
from typing import Any, Generator, Tuple
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
from torch.autograd import Variable
import numpy as np
from configordner.aufnahmesetting import RecordSettings
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import Erkanntermodus, KiData
from configordner.settings import LaufZeitConfig
import flet as ft
import torch
from torchvision import transforms
from PIL import Image



class TrainiertesModel(RecordSettings):

    
    def __init__(self) -> None:
        super().__init__()
        self.kidata = None
        self.model = None
        self.zeahler: int = 0
        self.isbackgroundvisible = False
        self.selectcamera = 0
        self.leerzeit = 0
        self.currenttime = 0
        
    def normalizedata(self):
        self.normalize = transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229, 0.224, 0.225])
        self.transformation = transforms.Compose([
            transforms.Resize(256),transforms.CenterCrop(224),
            
            transforms.ToTensor(),
            self.normalize,
        ])
    
    def UpdateZeahler(self,predicted_class:str, predictprozent: int):
        if "background" in predicted_class.lower().strip() and predictprozent > 0.5:
            print("drin")
            self.isbackgroundvisible = True
        elif self.isbackgroundvisible == True:
            self.zeahler += 1
            self.isbackgroundvisible = False

            
        
        
    def predict_image(self,image)-> Tuple[torch.Tensor,torch.Tensor]:
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        img_eval_tensor = self.transformation(pil_image)
        img_eval_tensor.unsqueeze_(0)
        data = Variable(img_eval_tensor)
        outputs = self.model(data)
        predictprozent, predicted_index = torch.max(outputs, 1)
        #print(predicted_index.size())
        predicted_class = predicted_index.item()
        

        return (predicted_class,predictprozent)
      
    def loadlabeldata(self):
        return open(self.kidata.pfad_label, "r").readlines()
    
    def loadmodelpytorch(self, progressring: ft.ProgressRing) -> Generator[Tuple[KiData,cv2.typing.MatLike], Any, Any]:

        self.kidata = KiDataManager.ladeKImodel()
        self.normalizedata()
       
        
        self.model = torch.load(self.kidata.pfad_model)
        if self.kidata is None:
            print("error")
            return
        self.model.eval()
        label_names = self.loadlabeldata()
       
        cap = cv2.VideoCapture(self.selectcamera) 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) # 0 steht für die erste angeschlossene Kamera
        start_time = time.time()
        progressring.visible = False
        progressring.update()
        if LaufZeitConfig.islaufzeit == False:
            self.destroycam(cap)
        
        while True:
            
            ret, frame = cap.read()
            cv2.rectangle(frame, self.p1, self.p2, self.MEINEFARBE, self.THICKNESS1)
            img_part = frame[
                self.cy : self.cy + self.rh, self.cx : self.cx + self.rw, :
            ]
            confidence_class,prediction_score = self.predict_image(img_part)

            label_name = label_names[confidence_class]
            self.UpdateZeahler(label_name,prediction_score.item())
            currenttime = round(time.time() - start_time,2)
            erkannt = Erkanntermodus.FARBE


            kidaten = KiData(label_name=label_name,confidence_score=int(np.round(confidence_class * 100)),erkannter_modus=erkannt, laufzeit=currenttime,anzahl=self.zeahler)
            yield (kidaten, frame)
            print("nach yield")
            self.leerzeit = time.time() - self.currenttime
            keyboard_input = cv2.waitKey(1)
            if keyboard_input == 27 or LaufZeitConfig.islaufzeit == False: 
                break
        
        cap.release()  # Gib die Ressourcen der Webcam frei
        cv2.destroyAllWindows()
        
    def destroycam(self,cap: cv2.VideoCapture):
        cap.release()  # Gib die Ressourcen der Webcam frei
        cv2.destroyAllWindows()
       
    def loadmodelKera(self, progressring: ft.ProgressRing) -> Generator[Tuple[KiData,cv2.typing.MatLike], Any, Any]:
        self.kidata = KiDataManager.ladeKImodel()
        
        if self.kidata is None:
            print("error")
            return
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model(self.kidata.pfad_model, compile=False)

        # Load the labels
        class_label_names = open(self.kidata.pfad_label, "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        camera = cv2.VideoCapture(0)
        
        progressring.visible = False
        progressring.update()
        start_time = time.time()
        while True:
            
            # Grab the webcamera's image.
            ret, image = camera.read()
            # Resize the raw image into (256-height,256-width) pixels
            image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)
            # Make the image a numpy array and reshape it to the models input shape.
            imageresharp = np.asarray(image, dtype=np.float32).reshape(1, 256, 256, 3)
            # Normalize the image array
            imageresharp = (imageresharp / 127.5) - 1
            # Predicts the model
            prediction = model.predict(imageresharp)
            index = np.argmax(prediction)
            label_name = class_label_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            #print("Class:", class_name[2:], end="")
            self.currenttime = time.time() - start_time - self.leerzeit
            #print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            yield (KiData(label_name[2:],str(np.round(confidence_score * 100))[:-2],"form", laufzeit=self.currenttime), image)
            self.leerzeit = time.time() - self.currenttime
            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27 or LaufZeitConfig.islaufzeit == False:
                break

        self.destroycam(camera)

    
  
        
  

def bildtoImage(self,image: np.ndarray[np.floating[Any]]):
    pass
