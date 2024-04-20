
import flet as ft
from StatusMeldungen.messageinfo import ClassCreatorSettingsMessage as CCSM
from configordner.settings import SaveDictName
from libcomponents.CustomTextField import TextFieldBCB
from libcomponents.filterdata import filterschanzendata
from logic.KiDatenManager import KiDataManager
from logic.Systemcode.camera import Camera
from modele.InterneDatenModele import CameraSettingsModel, SerialConfigModel
from flet import canvas as cv

from modele.SchanzenModelle import SchanzenBecher, SchanzenSteuerung

class BPSSlider(ft.Column):
    def __init__(self) -> None:
        super().__init__(self)

    def build(self) -> None:

        # Kommentiert den ausgewählten Code
        self.aufnahmegestext = ft.Text(
            CCSM.GESSLIDERTEXT, text_align=ft.TextAlign.CENTER
        )
        # Slider zur Auswahl der Aufnahmegeschwindigkeit mit Standardwert von 10% und einem Bereich von 10% bis 30%
        self.aufnahmeges = ft.Slider(
            value=10,
            label="{value} BPS",
            divisions=20,
            min=10,
            max=30,
            on_change=lambda e: self.on_change(e),
            active_color=ft.colors.BLUE,
        )
        self.aufnahmegestextausgabe = ft.Text(
            value=self.aufnahmeges.value, text_align=ft.TextAlign.CENTER
        )

        self.textausgabeBPS = ft.Container(
            self.aufnahmegestextausgabe, alignment=ft.alignment.center
        )
        
        self.columincontainer = ft.Container(ft.Column(
            [self.aufnahmegestext, self.aufnahmeges, self.textausgabeBPS]
        ), padding=ft.padding.all(5)
    )
        self.card = ft.Container(ft.Card(self.columincontainer))
        return ft.Column([self.card])

    def on_change(self, e: ft.ControlEvent):
        self.aufnahmegestextausgabe.value = f"{e.control.value} BPS"
        modeldata = CameraSettingsModel(aufnahmeges=int(e.control.value))
        # self.aufnahmegestext.value += str(e.control.value)
        self.page.client_storage.set(SaveDictName.camerasettings, modeldata)
        self.update()

    def did_mount(self):
        if self.page.client_storage.get(SaveDictName.camerasettings):

            data = KiDataManager.ladeDaten(
                SaveDictName.camerasettings, CameraSettingsModel
            )
            self.aufnahmeges.value = data.aufnahmeges
            self.aufnahmegestextausgabe.value = f"{data.aufnahmeges} BPS"
            self.update()


class SelectCamera(ft.Row):
    def __init__(self):
        super().__init__(self)

        self.cameralist = ft.Dropdown(
            on_change=self.button_clicked,
            expand=True,
            padding=ft.padding.all(5),
            border_width=3,
            border_radius=10,
            border_color=ft.colors.BLUE,
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            actions=[ft.TextButton("confirm", on_click=self.dismismodal)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=ft.Text("Keine Kamera gefunden"),
        )
        self.progress = ft.ProgressRing(
            stroke_width=3, visible=False, bgcolor=ft.colors.BLUE
        )
        self.controls = [self.cameralist, self.progress]
        self.row = ft.Row([self.cameralist, self.progress])

    def dismismodal(self, e):
        self.dialog.open = False
        self.page.update()

    def button_clicked(self, e: ft.TapEvent):

        camerasettings = KiDataManager.ladeDaten(
            SaveDictName.camerasettings, CameraSettingsModel
        )
        camerasettings.Camera = self.cameralist.value

        camerasettings.CameraName = self.cameralist.options[
            int(self.cameralist.value)
        ].text
        KiDataManager.saveclientdata(SaveDictName.camerasettings, camerasettings)
        self.update()

    def did_mount(self):
        cameradata = KiDataManager.ladeDaten(
            SaveDictName.camerasettings, CameraSettingsModel
        )
        self.cameralist.label = cameradata.CameraName

        self.progress.visible = True
        self.update()
        self.cameras = Camera()
        getnewcameradata = self.cameras.get_camera_info()
        self.progress.visible = False
        self.update()
        if getnewcameradata is not None and len(getnewcameradata) > 0:
            for camdata in getnewcameradata:
                index = camdata.get("camera_index")
                camera_name = camdata.get("camera_name")
                item = ft.dropdown.Option(index, camera_name)
                self.cameralist.options.append(item)
        else:
            self.page.dialog = self.dialog
            self.dialog.open = True
            self.page.update()
        self.update()


class COMSelector(ft.Row):
    def __init__(self) -> None:
       super().__init__()
       self.serialconfigdata = KiDataManager.ladeDaten(SaveDictName.serialsettings, SerialConfigModel)
       self.okbutton = ft.IconButton(icon=ft.icons.CHECK, on_click=self.savecomdata,highlight_color=ft.colors.GREEN)
       self.comtext = TextFieldBCB(on_submit=self.savecomdata, value=self.serialconfigdata.COM)
       self.controls = [self.comtext,self.okbutton]
       self.alignment = ft.MainAxisAlignment.CENTER
    
    def savecomdata(self,e):
        self.serialconfigdata.COM = self.comtext.value
        KiDataManager.saveclientdata(SaveDictName.serialsettings,self.serialconfigdata)



class EOverlay(ft.Container):
    def __init__(self) -> None:
        super().__init__()
        self.uetitle = ft.Row([ft.Text(text_align=ft.TextAlign.CENTER,
                                       style=ft.TextStyle(20,weight=ft.FontWeight.W_700),
                                       color=ft.colors.WHITE)],
                            alignment=ft.MainAxisAlignment.CENTER)
        self.bgcolor = ft.colors.BLACK
        
        self.width = 150
        
        self.radiogroup = ft.RadioGroup(ft.Column([
            
        ]),on_change=self.change_radio_inhalt)
        
        self.colum = ft.Column([self.uetitle,self.radiogroup])
        self.content = self.colum
        self.border_radius = 10
        self.shadow = ft.BoxShadow(2,2,ft.colors.BLUE)
     
    def change_radio_inhalt(self,e: ft.ControlEvent):
        self.data.selected = e.control.value
        #self.data ist ein teilobjekt von self.datenschanze 
        KiDataManager.saveSessionDaten(SaveDictName.topfmodus, self.dataschanze)
        

       
    def build(self):
        return super().build()
    
    
    def create_schanze_class(self,becher: SchanzenBecher):
        self.dataschanze = KiDataManager.ladeSessiondata(SaveDictName.topfmodus,SchanzenSteuerung)
        self.data = filterschanzendata(self.dataschanze,becher)
        return self.data
        

            
        
        
        



class EilmnerZeichner(ft.Container):
    def __init__(self, becher_text: SchanzenBecher,function_click,bottom=None, stroke_color: ft.colors = ft.colors.BLACK, stroke_innercolor: ft.colors = ft.colors.BLUE) -> None:
        super().__init__()
        self.becher_text = becher_text
        self.function_click = function_click
        self.stroke_color = stroke_color
        self.stroke_innercolor = stroke_innercolor
        self.innerbecher = cv.Path(
                [
                    cv.Path.MoveTo(25, 25),
                    cv.Path.LineTo(35, 90),
                    cv.Path.LineTo(70, 90),
                    cv.Path.LineTo(80, 25),
                    cv.Path.LineTo(25, 25),
                    cv.Path.Close()
                ],
                paint=ft.Paint(
                    
                    style=ft.PaintingStyle.FILL,
                    stroke_width=4,
                    color=self.stroke_innercolor
                ),
                    visible=False
                )
        
        cp = ft.Container(cv.Canvas(
        [
            cv.Path(
                [
                    cv.Path.MoveTo(25, 25),
                    cv.Path.LineTo(35, 90),
                    cv.Path.LineTo(70, 90),
                    cv.Path.LineTo(80, 25),
                    cv.Path.LineTo(25, 25),
                    cv.Path.Close()
                ],
                paint=ft.Paint(
                    
                    style=ft.PaintingStyle.STROKE,
                    stroke_width=4,
                    color=self.stroke_color
                ),
            ),
            self.innerbecher,
        ]
        ),height=90+25, width=80+25, on_click=self.anklickbarer_container,
                          ink=False,ink_color=ft.colors.BLUE)
        text = ft.TransparentPointer(ft.Text(self.becher_text.value,size=20),left=40,bottom=35)
        stack = ft.Stack([cp,text])
        self.content = stack
        self.bottom = bottom
        
        
    def anklickbarer_container(self,e: ft.ControlEvent):
        if self.function_click is not None:
            self.innerbecher.visible = not self.innerbecher.visible
            self.update()
            self.function_click(self.becher_text)
        
        
        