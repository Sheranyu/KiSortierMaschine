


from configordner.settings import SaveDictName
from logic.KiDatenManager import KiDataManager
from modele.InterneDatenModele import CameraSettingsModel


class RecordSettings:
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
        self.loadRecordSettings()
        
    def loadRecordSettings(self):
        data = KiDataManager.ladeDaten(SaveDictName.camerasettings,CameraSettingsModel)
        self.choicedcamera = data