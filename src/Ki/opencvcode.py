
import os
import time
from typing import Any, Generator, Tuple
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python

import numpy as np
from DIManager import DependencyInjector
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import KIModelsaverData, KiData
from configordner.settings import LaufZeitConfig
import flet as ft


class TrainiertesModel():

    
    def __init__(self) -> None:
        self.kidata = None
        
        

    def loadmodel(self, progressring: ft.ProgressRing) -> Generator[Tuple[KiData,cv2.typing.MatLike], Any, Any]:
        self.kidata = KiDataManager.ladeKIDaten()
        print(self.kidata)
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
            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            # Make the image a numpy array and reshape it to the models input shape.
            imageresharp = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
            # Normalize the image array
            imageresharp = (imageresharp / 127.5) - 1
            # Predicts the model
            prediction = model.predict(imageresharp)
            index = np.argmax(prediction)
            label_name = class_label_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            #print("Class:", class_name[2:], end="")
            currenttime = time.time() - start_time
            #print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            yield (KiData(label_name[2:],str(np.round(confidence_score * 100))[:-2],"form", laufzeit=currenttime), image)
            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27 or LaufZeitConfig.islaufzeit == False:
                break

        camera.release()
        cv2.destroyAllWindows()

    
  
        
  

def bildtoImage(self,image: np.ndarray[np.floating[Any]]):
    pass
