import base64
import os
import time
from typing import Any, Generator
import cv2
from flet import Image
from configordner.settings import LaufZeitConfig
from modele.InterneDatenModele import KiClassList

class WebcamAufnahme():
    def __init__(self) -> None:
        self.width = 640  # Mögliche Kameraauflösungen (bei mir): 640x380, 640x380, 640x640, 1280x720
        self.height = 480
        # WebCam Rahmen, Region of Interest
        self.rw = 224
        self.rh = 224
        self.cx = self.width // 2 - self.rw // 2  # Im Moment zentrierte Bildaufnahme
        self.cy = self.height // 2 - self.rh // 2
        self.p1 = (self.cx - 2, self.cy - 2)
        self.p2 = (self.cx + self.rw + 2, self.cy + self.rh + 2)
        self.size = (self.rw, self.rh)

        # Weitere Einstellungen
        self.framegap = 0.1  # für automatisierte Bildaufnahme, delay muss in der Schleife einkommentiert werden
        self.MEINEFARBE = (255, 255, 255)
        self.THICKNESS1 = 2

    def changeSettings():
        pass

    def StarteAufnahme(self,classdata: KiClassList) -> Generator[cv2.typing.MatLike, Any, None]:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        
        path = './'
        img_path = path
        i = 0
        while True:
            time.sleep(self.framegap)

            cur_class = classdata.classname
            print(f"Label: {cur_class}")
            if not os.path.exists(f'./{cur_class}'):
                os.system(f'mkdir {cur_class}')
            img_path = path + cur_class
            
            

            # Lies ein Bild
            ret, frame = cap.read()
            if not ret:
                cap.release()  # Freigabe der Kamera-Ressourcen, falls erforderlich
                raise cv2.error("Fehler beim Öffnen der Kamera")
            l, w, _ = frame.shape

            cv2.rectangle(frame, self.p1, self.p2, self.MEINEFARBE, self.THICKNESS1)
            img_part = frame[self.cy:self.cy + self.rh, self.cx:self.cx + self.rw, :]

            # Taste "s" -> Bildaufnahme
            
            cv2.imwrite(img_path + f'/{str(i).zfill(5)}.png', img_part)
            i += 1
            print(i)
            #f"{str(i).zfill(4)} Bild, Klasse: {cur_class} Aufloesung: {l}x{w}, x-Richtung: {self.cx}...{self.cx + self.rw}, y-Richtung: {self.cy}...{self.cy + self.rh} {img_path + f'/{str(i).zfill(4)}.png'}"

            # Bild anzeigen, Leertaste beendet
            yield frame
            if cv2.waitKey(1) % 0xFF == ord(' ') or LaufZeitConfig.islaufzeit == False:
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def BeendeAufnahme(self):
        pass

def ZeigeBildan(frame: cv2.typing.MatLike, fletImage: Image):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8")
        fletImage.src_base64 = frame_base64
        fletImage.update()
