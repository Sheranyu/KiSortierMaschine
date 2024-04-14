import os
import sys
from typing import List
from typing_extensions import deprecated
import cv2
from pygrabber.dshow_graph import FilterGraph
import pythoncom
import platform

# Ihr Code hier



@deprecated("Use SystemCode/camera")
def getCameras():
    if platform.system() == "Windows":
        pythoncom.CoInitialize()
        devices = FilterGraph().get_input_devices()

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name

        return available_cameras
    
@deprecated("Use SystemCode/camera")
def getCamerasOnlyIndex():
    cameras = []
    max_index_to_check = 6  # Maximale Indexnummer, die Sie überprüfen möchten
    
    # Speichern Sie die aktuelle Standardfehlerausgabe
    original_stderr = sys.stderr
    # Redirektieren Sie die Standardfehlerausgabe in eine Datei, um die Fehler zu unterdrücken
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull

        for i in range(max_index_to_check):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(cap)
# Stoppen Sie die Schleife, wenn Sie die gewünschte Anzahl von Kameras gefunden haben
    
    # Stellen Sie die Standardfehlerausgabe wieder her
    sys.stderr = original_stderr
    
    return cameras
    

