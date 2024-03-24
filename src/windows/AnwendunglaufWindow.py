import base64
import flet as ft
import cv2
from Designer.design import AnwendungstartPageDesign
from configordner.settings import LaufZeitConfig
from logic.kilauflogic import KiDatenVerarbeitung

from modele.InterneDatenModele import KIModelsaverData, KiData


class StartApplicationPage(AnwendungstartPageDesign):
    def __init__(self):
        super().__init__()
        self.ki_logic = KiDatenVerarbeitung()
        
    def build(self):

        self.colum1 = ft.Row([self.title])
        self.startrow = ft.Row([self.startbutton, self.abbruchbutton])
        self.bildvideoRow = ft.Row([self.bildvideo])
     
        self.columendcontainerlinks = ft.Container(ft.Column(
            [self.colum1, self.pr, self.startrow, self.bildvideoRow],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ))
        self.columcontainerechts = ft.Container(
            ft.Column(
                [
                    self.erkanntesobject,
                    self.erkanntermodus,
                    self.laufzeit,
                    self.anzahlsortierterobjekte,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.all(5),
            height=100
        )
        self.rowtest = ft.Row([self.columendcontainerlinks], alignment=ft.MainAxisAlignment.CENTER)
        self.anzeigekarte = ft.Card(content=self.columcontainerechts)
        # self.rowbilder = ft.Row([self.rowtest, self.anzeigekarte])
        self.gridview = ft.GridView(
                runs_count=2,
                child_aspect_ratio=1,
                controls=[self.rowtest, self.anzeigekarte],  
        )
        # self.container = ft.Container(content=self.columendcontainer, alignment=ft.alignment.center)
        self.rowcont = ft.Container(self.gridview, width=self.page.width)
        self.endrow = ft.Row([self.rowcont], alignment=ft.MainAxisAlignment.CENTER)
        return self.endrow

    def start_camera(self, e):
        self.pr.visible = True
        # load configdata
        # daten = Statistik(class_name="testneu",  confidence_score=80)
        # DataCreater().savestatistik(daten)
        LaufZeitConfig.islaufzeit = True
        toggle_two_buttons(self, False, True)
        try:
            for data in self.ki_logic.start_application(self.CamAnzeige, self.pr):
                if LaufZeitConfig.islaufzeit == False:
                    return
                self.DatenAnzeige(data)
        except Exception as err:
            print(f"Fehler: {err}")
            self.openwarndialog()
            

        toggle_two_buttons(self, True, False)

    def DatenAnzeige(self, kidaten: KiData):
        self.erkanntesobject.value = kidaten.label_name
        self.laufzeit.value = round(kidaten.laufzeit,2)
        self.anzahlsortierterobjekte.value = kidaten.anzahl
        self.erkanntermodus.value = kidaten.erkannter_modus

    def CamAnzeige(self, frame: cv2.typing.MatLike):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8") # type: ignore
        self.bildvideo.src_base64 = frame_base64
    
        self.update()

    def abbruch(self, e):
        toggle_two_buttons(self, True, False)
        LaufZeitConfig.islaufzeit = False
        self.update()

    def will_unmount(self):
        LaufZeitConfig.islaufzeit = False

        
    def openwarndialog(self):
        self.pr.visible = False
        self.page.dialog = self.alertwarn # type: ignore
        self.alertwarn.open = True
        LaufZeitConfig.islaufzeit == False
        self.page.update()# type: ignore


def toggle_two_buttons(self, start_visible, abbruch_visible):
    self.startbutton.visible = start_visible
    self.abbruchbutton.visible = abbruch_visible
    self.update()
