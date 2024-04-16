import flet as ft
from StatusMeldungen.messageinfo import ClassCreatorSettingsMessage as CCSM
from configordner.settings import SaveDictName
from logic.KiDatenManager import KiDataManager
from logic.Systemcode.camera import Camera
from modele.InterneDatenModele import CameraSettingsModel


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


class SelectCamera(ft.Column):
    def __init__(self):
        super().__init__(self)

    def build(self):
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
        )
        self.progress = ft.ProgressRing(
            stroke_width=3, visible=False, bgcolor=ft.colors.BLUE
        )

        self.row = ft.Row([self.cameralist, self.progress])

        return ft.Column([self.row], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

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
        cameradata = self.cameras.get_camera_info()
        self.progress.visible = False
        self.update()
        if len(cameradata) > 0:
            for camdata in cameradata:
                index = camdata.get("camera_index")
                camera_name = camdata.get("camera_name")
                item = ft.dropdown.Option(index, camera_name)

                self.cameralist.options.append(item)
        else:
            self.page.dialog = self.dialog
            self.dialog.open = True
            self.page.update()
        self.update()
