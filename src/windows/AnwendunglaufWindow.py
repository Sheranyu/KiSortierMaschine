import base64
import flet as ft
import cv2
from Designer.design import AnwendungstartPageDesign
from configordner.settings import LaufZeitConfig
from logic.kilauflogic import KiDatenVerarbeitung

from modele.InterneDatenModele import KIModelsaverData, KiData
from windows.subseiten.AnwendungSettings import AnwendungSetting


class StartApplicationPage(AnwendungstartPageDesign):
    def __init__(self):
        super().__init__()
        self.ki_logic = KiDatenVerarbeitung()
        self.settingseite = AnwendungSetting()
    def build(self):
        centermain = ft.MainAxisAlignment.CENTER

        self.titlecolum = ft.Row([self.title],alignment=centermain)
        self.startrow = ft.Row([self.startbutton, self.abbruchbutton,self.optionsbutton],alignment=centermain)
        self.bildvideoRow = ft.Row([self.bildvideo],alignment=centermain)
        
        self.floatbutton = ft.FloatingActionButton("test")

        self.columendcontainerlinks = ft.Container(
            ft.Column(
                [self.titlecolum, 
                 self.pr, 
                 self.startrow, 
                 self.bildvideoRow,
                 
                 ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            
            expand=True,
            alignment=ft.alignment.top_center,
        )
        
        #settingspage
        
        self.floatingpos = ft.FloatingActionButtonLocation.END_TOP
        self.floatingsettingexit = ft.Container(
            ft.FloatingActionButton(
                icon=ft.icons.CLOSE, 
                bgcolor=ft.colors.SURFACE,
                on_click=self.change_setting_window
                ),
            padding=ft.padding.all(5))
        self.settingpage = ft.Pagelet(content=AnwendungSetting(), 
                                      bgcolor=ft.colors.SURFACE_VARIANT, 
                                      visible=True, 
                                      floating_action_button=self.floatingsettingexit, 
                                      floating_action_button_location=self.floatingpos,
                                      
                                      )
        self.settingocntainer = ft.Container(self.settingpage, border_radius=8, 
                                             animate_scale=ft.animation.Animation(700,ft.AnimationCurve.EASE),
                                             scale=ft.Scale(0)
                                             )
        
        #settingspageende
        self.stack = ft.Stack([self.columendcontainerlinks,self.settingocntainer])
        self.columcontainerechts = ft.Container(
            ft.Column(
                [
                    self.erkanntesobject,
                    self.erkanntermodus,
                    self.laufzeit,
                    self.anzahlsortierterobjekte,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(5),
            height=100,
        )
        
        self.anzeigekarte = ft.Card(content=self.columcontainerechts)
        # self.rowbilder = ft.Row([self.rowtest, self.anzeigekarte])
        self.gridview = ft.GridView(
            runs_count=2,
            child_aspect_ratio=1,
            controls=[self.stack, self.anzeigekarte],
        )
        # self.container = ft.Container(content=self.columendcontainer, alignment=ft.alignment.center)
        
        
        
        return self.gridview

    def change_setting_window(self,e):
        if self.settingocntainer.scale == 1:
            self.settingocntainer.scale = 0
            #self.settingpage.visible = True
        else:
            self.settingocntainer.scale = 1
            #self.settingpage.visible = False
            
        self.update()



    def start_camera(self, e):
        self.pr.visible = True
        # load configdata
        # daten = Statistik(class_name="testneu",  confidence_score=80)
        # DataCreater().savestatistik(daten)
        LaufZeitConfig.islaufzeit = True
        toggle_two_buttons(self, False, True)
        try:
            self.ki_logic.start_application(self.CamAnzeige, self.pr, self.DatenAnzeige)
            if LaufZeitConfig.islaufzeit == False:
                return

        except Exception as err:
            print(f"Fehler: {err}")
            self.openwarndialog(err)

        toggle_two_buttons(self, True, False)

    def DatenAnzeige(self, kidaten: KiData):
        self.erkanntesobject.value = kidaten.label_name
        self.laufzeit.value = kidaten.laufzeit
        self.anzahlsortierterobjekte.value = kidaten.anzahl
        self.erkanntermodus.value = kidaten.erkannter_modus.value
        pass

    def CamAnzeige(self, frame: cv2.typing.MatLike):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8")  # type: ignore
        self.bildvideo.src_base64 = frame_base64

        self.update()

    def abbruch(self, e):
        toggle_two_buttons(self, True, False)
        LaufZeitConfig.islaufzeit = False
        self.update()

    def will_unmount(self):
        LaufZeitConfig.islaufzeit = False

    def openwarndialog(self, err: str = None):
        self.pr.visible = False
        self.page.dialog = self.alertwarn  # type: ignore
        self.alertwarn.open = True

        if err:
            self.alertwarntext.value = err

        LaufZeitConfig.islaufzeit == False
        self.page.update()  # type: ignore


def toggle_two_buttons(self, start_visible, abbruch_visible):
    self.startbutton.visible = start_visible
    self.abbruchbutton.visible = abbruch_visible
    self.update()
