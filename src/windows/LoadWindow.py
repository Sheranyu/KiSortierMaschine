import json
from typing import List
from Designer.design import CreateModelPageDesign, LoadModelPageDesign
from StatusMeldungen.status import WarnStatus
import flet as ft

from logic.aufnahme import WebcamAufnahme, ZeigeBildan
from modele.InterneDatenModele import KIModelsaverData, KiClassList

class LoadModelPage(LoadModelPageDesign):
    def __init__(self):
        super().__init__()
        self.kimodeldata: KIModelsaverData = KIModelsaverData()
        
    def build(self):
        self.ismodelloadedrow = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        self.isloadedcheckbox, padding=ft.padding.only(right=10)
                    ),
                    self.loadmodelbutton,
                ]
            ),
            padding=ft.padding.only(left=20),
        )

        self.islabelloaderrow = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        self.isloadedcheckboxlabel, padding=ft.padding.only(right=20)
                    ),
                    self.loadlabelbutton,
                ]
            ),
            padding=ft.padding.only(left=20),
        )

        self.columncardoben = ft.Column(
            [
                self.text_model_laden,
                self.ismodelloadedrow,
                self.text_lade_label,
                self.islabelloaderrow,
                self.selected_files,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.containeroben = ft.Container(self.columncardoben)

        self.columncardunten = ft.Column(
            [
                self.loaddatabutton,
                self.cardseperator,
                self.modelhinweistextue,
                self.modelhinweistext,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.containerunten = ft.Container(self.columncardunten)

        self.cardcolum = ft.Column(
            [self.containeroben, self.containerunten],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.cardcontainer = ft.Container(
            self.cardcolum,
            margin=ft.margin.all(5),
            padding=ft.padding.all(5),
            width=300,
        )
        self.card = ft.Card(content=self.cardcontainer)
        self.columcontainer = ft.Column(
            controls=[self.title, self.card], spacing=10, expand=True
        )
        self.rowcontainer = ft.Row([self.columcontainer],alignment=ft.MainAxisAlignment.CENTER)

        return self.rowcontainer

    def loaddata(self, e):
        if self.sind_alle_nicht_none() == False:
            self.warnbanner.open = True
            self.page.update()
            return

        with open("./modeldata.json","w") as json_file:
            json.dump(self.kimodeldata.__dict__, json_file,indent=4)
            
        self.page.session.set("kimodel", self.kimodeldata.__dict__)

    def close_banner(self, e):
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

        self.kimodeldata.label_datei_name = e.files[0].name
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

    def check_data_in_filepicker(self, e):
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
            for attr in [
                "ModelName",
                "label_datei_name",
                "pfad_model",
                "pfad_label",
                "modeltyp",
            ]
        )