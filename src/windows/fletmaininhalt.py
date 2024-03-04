import base64
import os
import sys
import cv2
import flet as ft
from StatusMeldungen.status import WarnStatus
from logic.kilauflogic import KiDatenVerarbeitung
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.CRUD.Statistik import StatistikCreater
from PIL import Image
from configordner.settings import LaufZeitConfig
from db.db_and_models.models import Statistik
from db.db_and_models.session import sessiongen
from modele.InterneDatenModele import KIModel, KiData
from Designer.design import (
    CreateModelPageDesign,
    LoadModelPageDesign,
    StartSeitePageDesign,
)


class BaseWindow:
    _page = None  # Klassenattribut für das page-Objekt

    @classmethod
    def set_page(cls, page: ft.Page) -> None:
        cls._page = page

    def __init__(cls, page: ft.Page) -> None:
        cls._page = page


class Mainwindow(BaseWindow):
    def __new__(self, page: ft.Page) -> ft.Row:

        self.weite = 500
        self.breite = 75
        self.page = page
        # cls.text1 = ft.Text("Neues Modell erstellen", theme_style=ft.TextTheme.label_large)

        self.button1 = ft.Container(
            content=ft.CupertinoButton(
                text="Neues Modell erstellen",
                on_click=lambda e: self.page.go("/create-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button2 = ft.Container(
            content=ft.CupertinoButton(
                text="Modell laden",
                on_click=lambda e: self.page.go("/load-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button3 = ft.Container(
            content=ft.CupertinoButton(
                text="Starte Anwendung",
                on_click=lambda e: self.page.go("/start-application"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button4 = ft.Container(
            content=ft.CupertinoButton(
                text="Statistiken",
                on_click=lambda e: self.page.go("/statistik"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button5 = ft.Container(
            content=ft.CupertinoButton(text="Exit!", on_click=self.exit_application),
            bgcolor=ft.colors.BLUE,
            width=self.weite,
            height=self.breite,
        )
        self.row = ft.Column(
            controls=[
                self.button1,
                self.button2,
                self.button3,
                self.button4,
                self.button5,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        self.container = ft.Container(content=self.row, expand=True)
        self.container.alignment = ft.alignment.top_center
        return self.container

    def exit_application(self):
        self.page.window_close()

    def mainwindow(self):
        pass


# class secondclass(BaseWindow):
#     def __new__(cls, page: ft.Page) -> None:
#         cls.page = page
#         cls.button = ft.FloatingActionButton(text="Mehr Durstlöscher kaufen!", width=200, on_click=cls.pagegeher)
#         cls.row = ft.Row(controls=[cls.button])
#         return cls.button
#     def pagegeher(self):
#         self.page.go("/start-application")


class CreateModelPage(CreateModelPageDesign):
    def __init__(self):
        super().__init__()

    def build(self):

        self.classcolumntemplate = ft.Column()
        self.classcontainertempalte = ft.Container(content=self.classcolumntemplate)

        self.containercolum = ft.Column(
            controls=[
                self.title,
                self.instructions,
                self.model_name,
                self.modeltyplist, 
                self.save_file_pfad,
                self.submit_button,
            ],
            spacing=10,
        )

        self.container = ft.Container(content=self.containercolum)
        return self.container

    def StartCamera(self):
        return super().StartCamera()

    def CreateNewTrainingClass(self):
        return super().CreateNewTrainingClass()

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def openbanner(self,textinfo: str = None):
        if textinfo != None:
            self.bannerfailtextcontent.value = textinfo
            
        self.page.banner.open = True
        self.page.update()

    def save_file_result(self, e: ft.FilePickerResultEvent):
        self.save_file_pfad.value = e.path if e.path else "Cancelled!"
        if e.path is None:
            return

        self.save_file_pfad.update()

    def create_model(self, e):
        if self.model_name.value is None or self.model_name.value.strip() == "":
            self.openbanner(WarnStatus.PFAD_OR_MODELNAME_NICHT_GEWAHLT)
            return

        if self.modeltyplist.value == None:
            self.openbanner(WarnStatus.MODEL_NICHT_GEWAEHLT)
            return
        
        self.kimodelsaver = KIModel(self.model_name.value, self.save_file_pfad.value, self.modeltyplist.value)
        self.page.client_storage.set("kimodelsaver", self.kimodelsaver.__dict__)

    def did_mount(self):
        self.page.banner = self.warningbanner
        self.page.overlay.append(self.pick_files_dialog)
        self.page.dialog = self.alertWarnhinweis
        self.alertWarnhinweis.open = True
        self.page.update()


class LoadModelPage(LoadModelPageDesign):
    def __init__(self):
        super().__init__()
        self.kimodeldata: KIModel = KIModel()
        
    def build(self):
        self.ismodelloadedrow = ft.Container(ft.Row([ft.Container(self.isloadedcheckbox,padding=ft.padding.only(right=10)), self.loadmodelbutton]),
                                             padding=ft.padding.only(left=20)) 
        
        self.islabelloaderrow = ft.Container(ft.Row([ft.Container(self.isloadedcheckboxlabel,padding=ft.padding.only(right=20)),self.loadlabelbutton])
                                             ,padding=ft.padding.only(left=20))
        
    
       
        self.columncardoben = ft.Column([
                self.text_model_laden,
                self.ismodelloadedrow,
                self.text_lade_label,
                self.islabelloaderrow,
                self.selected_files],horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.containeroben = ft.Container(self.columncardoben)
        
        self.columncardunten = ft.Column([ 
                self.loaddatabutton,
                self.cardseperator,
                self.modelhinweistextue,
                self.modelhinweistext,],horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.containerunten = ft.Container(self.columncardunten)
        
        self.cardcolum = ft.Column(
            [
                self.containeroben,
                self.containerunten
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.cardcontainer = ft.Container(
            self.cardcolum, margin=ft.margin.all(5), padding=ft.padding.all(5),width=300
        )
        self.card = ft.Card(content=self.cardcontainer)
        self.columcontainer = ft.Column(controls=[self.title, self.card], spacing=10,expand=True)
        self.container = ft.SafeArea(content=self.columcontainer)

        return self.container

    def loaddata(self,e):
        if self.sind_alle_nicht_none() == False:  
            self.warnbanner.open = True
            self.page.update()  
            return
        
        self.page.session.set("kimodel", self.kimodeldata.__dict__)
    
    def close_banner(self,e):
        self.warnbanner.open = False
        self.page.update()
    
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if self.check_data_in_filepicker(e) is False:
            self.warnbanner.open = True
            return

        self.kimodeldata.ModelName = e.files[0].name
        self.kimodeldata.pfad_model = e.files[0].path
        self.isloadedcheckbox.name = ft.icons.CHECK_BOX_ROUNDED
        self.selected_files.value = "erfolgreich geladen"
        self.selected_files.visible = True
        self.selected_files.color = ft.colors.GREEN
        self.update()

    def pick_file_label_result(self, e: ft.FilePickerResultEvent):
        if self.check_data_in_filepicker(e) == False:
            return
        
        self.kimodeldata.label_name = e.files[0].name
        self.kimodeldata.pfad_label = e.files[0].path
        self.selected_files.value = "erfolgreich geladen"
        self.isloadedcheckboxlabel.name = ft.icons.CHECK_BOX_ROUNDED
        self.selected_files.visible = True
        self.selected_files.color = ft.colors.GREEN
        self.update()
    
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.overlay.append(self.pick_file_label)
        self.page.banner = self.warnbanner
       
    
    def check_data_in_filepicker(self,e):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        if self.selected_files.value == "Cancelled!":
            self.selected_files.visible = True
            self.selected_files.color = ft.colors.RED
            self.update()
            return False
        return True
    def sind_alle_nicht_none(self):
        return all(
            getattr(self.kimodeldata, attr) is not None
            for attr in ["ModelName", "label_name", "pfad_model", "pfad_label", "modeltyp"]
        )
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


class Statistiken(ft.UserControl):
    def __init__(self):
        super().__init__()
        

    def build(self):
        # oberflächeninhalt was ich brauche:
        #
        # Anzeige für wie viele teile Sortiert worden sind
        # Anzeige für wie viele dem entsprechenden Modus: Ob Farbe oder Form
        # Anzeige: Was wurde mehr sortiert Farbe oder Form
        # Anzeige: Laufzeit der Sortiermaschine
        # Funktion: Laden der vergangenen Daten reicht als Button
        # Bonus oder je nach Kontext: Speichern der statistik
        # Hinweiß: Speichern kann auch automatisch erfolgen
        # Bonus: wie weit sich der Motor drehen musste.
        self.title = ft.Text("Alle Statisiken", theme_style="headlineMedium")
        self.button = ft.CupertinoButton("Bekomme Daten", on_click=self.getdata)
        self.SearchStatistikdata = ft.SearchBar(
            on_submit=self.onEnterSearch, divider_color=ft.colors.AMBER
        )

        self.rowcontainer = ft.Row([self.title, self.button, self.SearchStatistikdata])
        return self.rowcontainer

    def close_anchor(self):
        self.SearchStatistikdata.close_view()

    def onEnterSearch(self, e):
        self.update()

    def getdata(self, e):
        pass


def toggle_two_buttons(self, start_visible, abbruch_visible):
    self.startbutton.visible = start_visible
    self.abbruchbutton.visible = abbruch_visible
    self.update()
