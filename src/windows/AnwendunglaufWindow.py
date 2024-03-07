import base64
import flet as ft
import cv2
from Designer.design import StartSeitePageDesign
from configordner.settings import LaufZeitConfig
from logic.kilauflogic import KiDatenVerarbeitung

from modele.InterneDatenModele import KiData


class StartApplicationPage(StartSeitePageDesign):
    def __init__(self):
        super().__init__()
        self.ki_logic = KiDatenVerarbeitung()

    def build(self):
        self.colum1 = ft.Row([self.title])
        self.startrow = ft.Row([self.startbutton, self.abbruchbutton])
        self.bildvideoRow = ft.Row([self.bildvideo])
        self.columendcontainer = ft.Column(
            [self.colum1, self.pr, self.startrow, self.bildvideoRow]
        )
        self.container = ft.Container(content=self.columendcontainer)
        return self.container

    def start(self, e):
        self.pr.visible = True
        # load configdata
        # daten = Statistik(class_name="testneu",  confidence_score=80)
        # DataCreater().savestatistik(daten)
        LaufZeitConfig.islaufzeit = True
        toggle_two_buttons(self, False, True)
        try:
            for data in self.ki_logic.start_application(self.CamAnzeige, self.pr):
                self.DatenAnzeige(data)
        except:
            self.openwarndialog()

        toggle_two_buttons(self, True, False)

    def DatenAnzeige(self, kidaten: KiData):
        print(kidaten.label_name)

    def CamAnzeige(self, frame: cv2.typing.MatLike):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8")
        self.bildvideo.src_base64 = frame_base64
        self.update()

    def abbruch(self, e):
        toggle_two_buttons(self, True, False)
        LaufZeitConfig.islaufzeit = False
        self.update()

    def will_unmount(self):
        LaufZeitConfig.islaufzeit = False

    def openwarndialog(self):

        self.page.dialog = self.alertwarn
        self.alertwarn.open = True
        self.page.update()
        
def toggle_two_buttons(self, start_visible, abbruch_visible):
    self.startbutton.visible = start_visible
    self.abbruchbutton.visible = abbruch_visible
    self.update()