
import os
from typing import Any, Generator
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from modele.InterneDatenModele import KiData
from configordner.settings import LaufZeitConfig
from configordner.settings import ModelDataClass



class TrainiertesModel():
    def __init__(self) -> None:
        modeldata = ModelDataClass()

    def loadmodel(self) -> Generator[KiData, Any, Any]:
        aktueller_ordner = os.path.dirname(os.path.abspath(__file__))
      # Übergeordneter Ordner (A) erhalten
        #uebergeordneter_ordner = os.path.dirname(aktueller_ordner)
        # Pfad zum Ordner C erstellen
        Kidatei = os.path.join(aktueller_ordner, "kimodel", "keras_model.h5")
        # Pfad zur gewünschten Datei in Ordner C erstellen
        label = os.path.join(aktueller_ordner,"kimodel","labels.txt")
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model(Kidatei, compile=False)

        # Load the labels
        class_label_names = open(label, "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        camera = cv2.VideoCapture(0)

        while True:
            # Grab the webcamera's image.
            ret, image = camera.read()

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Show the image in a window
            cv2.imshow("Webcam Image", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image)
            index = np.argmax(prediction)
            label_name = class_label_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            #print("Class:", class_name[2:], end="")
            
            
            #print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            yield KiData(label_name[2:],str(np.round(confidence_score * 100))[:-2],"form")
            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27 or LaufZeitConfig.islaufzeit == False:
                break

        camera.release()
        cv2.destroyAllWindows()
