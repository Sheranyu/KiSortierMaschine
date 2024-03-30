import base64
import os
import time
from typing import Any, Generator
import cv2
from flet import Image
from configordner.settings import LaufZeitConfig, SaveDictName
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import (
    AufnahmeDaten,
    ClassCreatorSettingsModel,
    KiClassList,
)
from flet import ProgressRing, TextField


class WebcamAufnahme:
    def __init__(self) -> None:
        self.width = 640  # Mögliche Kameraauflösungen (bei mir): 640x380, 640x380, 640x640, 1280x720
        self.height = 480
        # WebCam Rahmen, Region of Interest
        self.rw = 256
        self.rh = 256
        self.cx = self.width // 2 - self.rw // 2  # Im Moment zentrierte Bildaufnahme
        self.cy = self.height // 2 - self.rh // 2
        self.p1 = (self.cx - 2, self.cy - 2)
        self.p2 = (self.cx + self.rw + 2, self.cy + self.rh + 2)
        self.size = (self.rw, self.rh)
        self.CCSWSettings = None
        # Weitere Einstellungen
        self.framegap = 0.05  # für automatisierte Bildaufnahme, delay muss in der Schleife einkommentiert werden
        self.MEINEFARBE = (255, 255, 255)
        self.THICKNESS1 = 2

    def changeSettings(self):
        self.CCSWSettings = KiDataManager.ladeDaten(
            SaveDictName.classcreatorsettings, ClassCreatorSettingsModel
        )
        self.framegap = 1/self.CCSWSettings.aufnahmeges

    def StarteAufnahme(
        self, classdata: KiClassList, pr: ProgressRing
    ) -> Generator[AufnahmeDaten, Any, None]:
        self.changeSettings()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        path = f"{classdata.speicherpfad}"
        img_path = path
        i = 0

        cur_class = classdata.classname

        img_path = f"{path}\{cur_class}"
        print(img_path)

        print(f"Label: {cur_class}")
        if not os.path.exists(f"{img_path}"):
            os.system(f"mkdir {img_path}")
        print(os.path.exists(f"{img_path}"))
        if LaufZeitConfig.islaufzeit == False:
            return
        pr.visible = False
        pr.update()
        while True:
            
            if LaufZeitConfig.ispauseactive:
                time.sleep(0.1)
                if LaufZeitConfig.islaufzeit == False:
                    return
                continue
            time.sleep(self.framegap)

            # Lies ein Bild
            ret, frame = cap.read()
            if not ret:
                cap.release()  # Freigabe der Kamera-Ressourcen, falls erforderlich
                raise cv2.error("Fehler beim Öffnen der Kamera")
            l, w, _ = frame.shape

            cv2.rectangle(frame, self.p1, self.p2, self.MEINEFARBE, self.THICKNESS1)
            img_part = frame[
                self.cy : self.cy + self.rh, self.cx : self.cx + self.rw, :
            ]
            bildername = f"/{cur_class}{str(i).zfill(5)}.png"
            imagewrite = img_path + bildername
            cv2.imwrite(imagewrite, img_part)
            i += 1
            print(i)
            # f"{str(i).zfill(4)} Bild, Klasse: {cur_class} Aufloesung: {l}x{w}, x-Richtung: {self.cx}...{self.cx + self.rw}, y-Richtung: {self.cy}...{self.cy + self.rh} {img_path + f'/{str(i).zfill(4)}.png'}"

            # Bild anzeigen, Leertaste beendet
            yield AufnahmeDaten(imagedata=frame, aufnahmefotoname=bildername)
            if cv2.waitKey(1) % 0xFF == ord(" ") or LaufZeitConfig.islaufzeit == False:
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


def Aktuelletextanzeige(zeigemomentanbildintext: TextField, frame: AufnahmeDaten):
    zeigemomentanbildintext.value = frame.aufnahmefotoname
    zeigemomentanbildintext.update()