
import base64
from re import S
import cv2
import flet as ft
from logic.kilauflogic import KiDatenVerarbeitung
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.CRUD.Statistik import StatistikCreater
from PIL import Image
from configordner.settings import LaufZeitConfig
from db.db_and_models.models import Statistik
from db.db_and_models.session import sessiongen
class BaseWindow:
    _page = None  # Klassenattribut für das page-Objekt

    @classmethod
    def set_page(cls, page: ft.Page) -> None:
        cls._page = page
    
    def __init__(cls,page: ft.Page) -> None:
        cls._page = page

class Mainwindow(BaseWindow):
    def __new__(self,page: ft.Page) -> ft.Row:
        
        self.weite = 500
        self.breite = 75
        self.page = page
        #cls.text1 = ft.Text("Neues Modell erstellen", theme_style=ft.TextTheme.label_large)

        self.button1 = ft.Container(
            content=ft.CupertinoButton(text="Neues Modell erstellen", on_click=lambda e: self.page.go("/create-model"), bgcolor=ft.colors.BLUE),
            width=self.weite,
            height=self.breite,
        )
        self.button2 = ft.Container(
            content=ft.CupertinoButton(text="Modell laden", on_click=lambda e: self.page.go("/load-model"), bgcolor=ft.colors.BLUE),
            width=self.weite,
            height=self.breite,
        )
        self.button3 = ft.Container(
            content=ft.CupertinoButton(text="Starte Anwendung", on_click=lambda e: self.page.go("/start-application"), bgcolor=ft.colors.BLUE),
            width=self.weite,
            height=self.breite,
        )
        self.button4 = ft.Container(
            content=ft.CupertinoButton(text="Statistiken", on_click=lambda e: self.page.go("/statistik"), bgcolor=ft.colors.BLUE),
            width=self.weite,
            height=self.breite,
        )
        self.button5 = ft.Container(
            content=ft.CupertinoButton(text="Exit!", on_click=lambda e: self.exit_application(page), bgcolor=ft.colors.BLUE),
            width=self.weite,
            height=self.breite,
        )
        self.row = ft.Column(controls=[
                        self.button1, self.button2, self.button3, self.button4, self.button5],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        )
        self.container = ft.Container(content=self.row, expand=True)
        self.container.alignment = ft.alignment.top_center
        return self.container
    
    def exit_application(cls):
        pass

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



 
class CreateModelPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
    def build(self):
        self.title = ft.Text("Modell erstellen", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.instructions = ft.Text("Neues Modell erstellen")
        self.model_name = ft.TextField(label="Modell Name")
        self.submit_button = ft.FloatingActionButton(text="erstellen", on_click=self.create_model)
 
        self.submit_button = ft.FloatingActionButton(on_click=self.create_model,content=ft.Row(
            [ft.Icon(ft.icons.ADD)], alignment="center", spacing=5
        ))

        return ft.Column(
            controls=[self.title, self.instructions, self.model_name, self.submit_button],
            spacing=10
        )

    def create_model(self, e):
        pass

class LoadModelPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
    def build(self):
        self.title = ft.Text("Modell Laden", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.instructions = ft.Text("Wähle ein Modell zum laden aus.")

        return ft.Column(
            controls=[self.title, self.instructions],
            spacing=10
        )
    
    def load_model(self, e):
        pass

class StartApplicationPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.ki_logic = KiDatenVerarbeitung() 
        
        
    def build(self):
        self.title = ft.Text("Start Application", theme_style="headlineMedium")
        self.startbutton = ft.ElevatedButton("Start",bgcolor=ft.colors.BLUE, on_click=self.start)
        self.abbruchbutton = ft.ElevatedButton("Abbruch", bgcolor=ft.colors.RED, on_click=self.abbruch, visible=False)
        self.bildvideo = ft.Image("")
        self.colum1 = ft.Row([self.title])
        self.startrow = ft.Row([self.startbutton, self.abbruchbutton])
        self.bildvideoRow= ft.Row([self.bildvideo])
        self.columendcontainer = ft.Column([self.colum1, self.startrow,self.bildvideoRow])
        self.container = ft.Container(content=self.columendcontainer)
        return self.container
    
    def start(self,e):
        # load configdata
        # daten = Statistik(class_name="testneu",  confidence_score=80)
        # DataCreater().savestatistik(daten)
        LaufZeitConfig.islaufzeit = True
        toggle_two_buttons(self,False, True)
        
        self.ki_logic.start_application(self.CamAnzeige)
            
        toggle_two_buttons(self,True, False)


    def CamAnzeige(self,frame: cv2.typing.MatLike):
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        self.bildvideo.src_base64 = frame_base64
        self.update()
    
    def abbruch(self,e):
        toggle_two_buttons(self,True,False)
        LaufZeitConfig.islaufzeit = False
        self.update()
    
    def will_unmount(self):
        LaufZeitConfig.islaufzeit = False
        
    


class Statistiken(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
    def build(self):
        #oberflächeninhalt was ich brauche:
        #
        #Anzeige für wie viele teile Sortiert worden sind
        #Anzeige für wie viele dem entsprechenden Modus: Ob Farbe oder Form
        #Anzeige: Was wurde mehr sortiert Farbe oder Form
        #Anzeige: Laufzeit der Sortiermaschine
        #Funktion: Laden der vergangenen Daten reicht als Button
        #Bonus oder je nach Kontext: Speichern der statistik
        #Hinweiß: Speichern kann auch automatisch erfolgen
        #Bonus: wie weit sich der Motor drehen musste. 
        self.title = ft.Text("Alle Statisiken", theme_style="headlineMedium")
        self.button = ft.CupertinoButton("Bekomme Daten", on_click=self.getdata)
        self.SearchStatistikdata = ft.SearchBar(on_submit=self.onEnterSearch,divider_color=ft.colors.AMBER)

        self.rowcontainer = ft.Row([self.title,self.button, self.SearchStatistikdata])
        return self.rowcontainer
    
    def close_anchor(self):
        self.SearchStatistikdata.close_view()

    def onEnterSearch(self,e): 
        self.update()
    
    def getdata(self,e):
        pass
    
    




def toggle_two_buttons(self, start_visible, abbruch_visible):
    self.startbutton.visible = start_visible
    self.abbruchbutton.visible = abbruch_visible
    self.update()