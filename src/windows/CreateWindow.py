from datetime import date
from typing import Any, List

from Designer.design import CreateModelPageDesign
from StatusMeldungen.status import WarnStatus, check_and_warn
import flet as ft
from configordner.settings import LaufZeitConfig
from flet_core.control import Control, OptionalNumber
from logic.aufnahme import Aktuelletextanzeige, WebcamAufnahme, ZeigeBildan
from Ki.pytorch import KiTraining
from modele.InterneDatenModele import (
    KIModelsaverData,
    KiClassList,
    KiModeltrainingConfigdata,
)
from windows.subseiten.ClassCreatorSettingsWindow import SettingsClassCreator


class CreateModelPage(CreateModelPageDesign):
    def __init__(self):
        super().__init__()

        self.dynabstandadder = 700 / 5
        self.aufnahme = WebcamAufnahme()
        self.listederaufgabenlocalspeicher = []
        self.kitrainer = KiTraining(self.fortschrittbalken)

    def build(self):
        """Builds the UI for the create model page.

        Builds the full page layout, including:

        - ListView for displaying model training status
        - ExpansionPanel for model training settings
        - Webcam and image display
        - Progress bar and text for tracking training
        - NavigationDrawer for settings page
        - Responsive grid layout
        """
        
        self.listview = ft.ListView(spacing=8, padding=15, auto_scroll=False, height=40)

        self.batchsizecard = ft.Card(
            ft.Container(
                ft.Column([self.batchsizetext, self.batchsize]),
                padding=ft.padding.all(3),
                border=ft.border.all(2),
                border_radius=ft.border_radius.all(2),
            )
        )

        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            width=300,
            divider_color=ft.colors.AMBER,
            controls=[
                ft.ExpansionPanel(
                    header=ft.Container(
                        ft.Column([self.start_training_btn, self.abbruchtrainingbtn]),
                        padding=ft.padding.all(5),
                    ),
                    content=ft.Container(
                        ft.Column(
                            [
                                self.modeltyplist,
                                self.epoches,
                                self.lernratetextfield,
                                self.maxeingelesendatenseatz,
                                self.batchsizecard,
                            ]
                        ),
                        padding=ft.padding.all(5),
                    ),
                )
            ],
        )

        self.listcontainer = ft.Container(
            content=self.listview,
            bgcolor=ft.colors.BLACK87,
            border_radius=ft.border_radius.all(7),
            shadow=self.boxshadow,
            col=9,
        )

        self.containercolum = ft.Column(
            controls=[
                ft.Container(
                    ft.Column(
                        [
                            self.title,
                            self.instructions,
                            self.model_name,
                            self.loadmodelbuttonpicker,
                            self.save_file_pfad,
                            self.panel,
                            self.CameraContainer,
                            self.zeigemomentanbildintext,
                        ]
                    )
                )
            ],
            col=3,
        )

        self.canvastrenner = ft.canvas.Canvas(
            [
                ft.canvas.Path(
                    [
                        ft.canvas.Path.MoveTo(25, 25),
                        ft.canvas.Path.LineTo(35, 25),
                        ft.canvas.Path.LineTo(35, 400),
                        ft.canvas.Path.LineTo(25, 400),
                    ]
                )
            ],
            width=float("inf"),
            expand=True,
            col=1,
        )

        self.buttonwithpr = ft.Column(
            [self.floatedbutton, self.settingbuttonclass, self.progressring],
            col=3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.anzeigerechts = ft.Column(
            [
                self.fortschrittbalkentext,
                self.fortschrittbalken,
            ],
            col=3,
            visible=False,
        )
        self.listwithbutton = ft.ResponsiveRow([self.listcontainer, self.buttonwithpr])

        self.columleft = ft.Column([self.listwithbutton], col=4)
        self.divider = ft.Container(
            bgcolor=ft.colors.BLUE_300, width=30, expand=True, col=1
        )

        self.enddrawer = ft.NavigationDrawer([SettingsClassCreator()])
        self.pageletseite = ft.Pagelet(
            content=self.columleft,
            col=4,
            width=self.page.width,
            height=self.page.height,
            drawer=self.enddrawer,
        )

        self.rowcontainer = ft.ResponsiveRow(
            [
                self.pageletseite,
                self.containercolum,
                self.canvastrenner,
                self.anzeigerechts,
            ]
        )

        self.endcontainer = ft.Container(content=self.rowcontainer)

        self.stack = ft.Stack([self.endcontainer])
        return self.stack

    # ---Beginn der Logic-----#
    def start_create_model(self, e):

        if self.model_name.value is None or self.model_name.value.strip() == "":
            self._openbanner(WarnStatus.PFAD_OR_MODELNAME_NICHT_GEWAHLT)
            return

        if self.modeltyplist.value == None:
            self._openbanner(WarnStatus.MODEL_NICHT_GEWAEHLT)
            return

        self.kimodelsaver = KIModelsaverData(
            self.model_name.value, self.save_file_pfad.value, self.modeltyplist.value
        )
        self.anzeigerechts.visible = True
        self.update()

        configdata = KiModeltrainingConfigdata(
            bachsize=self.batchsize.value,
            epoches=self.epoches.value,
            lernrate=self.lernratetextfield.value,
            maxdatenseatze=self.maxeingelesendatenseatz.value
        )

        self.start_training_btn.visible = False
        self.abbruchtrainingbtn.visible = True
        self.update()

        LaufZeitConfig.Enable_istrainingactive()
        self.kitrainer.Set_Settings(configdata)
        self.kitrainer.starte_ki_training(self.kimodelsaver)
        LaufZeitConfig.Disable_istrainingactive()
        self.anzeigerechts.visible = False
        self.start_training_btn.visible = True
        self.abbruchtrainingbtn.visible = False
        self.update()

    def cancel_ki_training(self, e):
        LaufZeitConfig.Disable_istrainingactive()
        self.start_training_btn.visible = True
        self.abbruchtrainingbtn.visible = False
    def delete_drawer(self,e):
        self.page.views[1].end_drawer.clean()
        
        


    def Open_Settings_Class(self):
        self.enddrawer.open = True
        self.enddrawer.update()
        #self.page.go("/classcreatorsettings")

    def DeleteClass(self, e, classitem):
        
        daten = self.page.session.get("listederaufgabenlocalspeicher")  # type: ignore
        daten = [
            item for item in daten if item["classindex"] != classitem["classindex"]  # type: ignore
        ]
        self.page.session.set("listederaufgabenlocalspeicher", daten)  # type: ignore
        if len(self.listview.controls) <= 5:
            self.listview.height -= self.dynabstandadder  # type: ignore

        self._ladeliste()

    def ZeigeaktuelelBilder(self, e):
        # print("zeige aktuelel bilder")
        pass
    
    def check_and_warn(self,condition, warn_status):
        if condition:
            self._openbanner(warn_status)
            return True
        return False
    
    def StartCamera(self, classitem, textfield: ft.TextField):
        if check_and_warn(self._openbanner,self.save_file_pfad.value == "Cancelled!" or self.save_file_pfad.value is None, WarnStatus.PFAD_IS_EMPTY):
            return
        if check_and_warn(self._openbanner,textfield.value is None or textfield.value == "", WarnStatus.CLASS_NAME_EMPTY):
            return
        if check_and_warn(self._openbanner,LaufZeitConfig.islaufzeit, WarnStatus.FORBIDDEN_TWO_VIDEO_REC):
            return

        textfield.disabled = True
        self.changebutton(classitem, False, True)
        LaufZeitConfig.islaufzeit = True
        self.progressring.visible = True
        newdata = KiClassList(
            classitem["classindex"], textfield.value, self.save_file_pfad.value
        )
        self.update()

        # starte aufnahme
        for frame in self.aufnahme.StarteAufnahme(newdata, self.progressring):
            ZeigeBildan(frame.imagedata, self.CameraContainer)
            Aktuelletextanzeige(self.zeigemomentanbildintext, frame)
        # self.beendevideoaufnahme(classitem)

    def beendevideoaufnahme(self, classitem):
        self.changebutton(classitem, True, False)
        LaufZeitConfig.islaufzeit = False

    def _saveclassnameeingabe(self, e: ft.ControlEvent, item):
        if self.page is not None and self.page.session is not None:
            daten = self.page.session.get("listederaufgabenlocalspeicher")
        else:
            return

        if daten == None:
            return
        for oneitem in daten:
            if oneitem["classindex"] == item["classindex"]:
                oneitem["classname"] = e.data

        
        self.page.session.set("listederaufgabenlocalspeicher", daten)
        self.page.update()

    
    def pause_aufnahme(self,e):
        if LaufZeitConfig.ispauseactive:
            LaufZeitConfig.ispauseactive = False
        else:
            LaufZeitConfig.ispauseactive = True
            
                
    def _ladeliste(self):
        self.listederaufgabenlocalspeicher = self.page.session.get(
            "listederaufgabenlocalspeicher"
        )
        
        self.listview.controls.clear()
        self.listdict = {}
        for item in self.listederaufgabenlocalspeicher:

            self.newtextfiel = ft.TextField(
                label="class name",
                value=item["classname"],
                on_change=lambda e, item=item: self._saveclassnameeingabe(e, item),
            )
            self.newcameraaufnahmebutton = ft.FilledButton(
                "Start Aufnahme",
                on_click=lambda e, anzahl=item, text=self.newtextfiel: self.StartCamera(
                    anzahl, text
                ),
            )
            
            self.pausevideo = ft.ElevatedButton(content=ft.Icon(ft.icons.PLAY_ARROW),on_click=self.pause_aufnahme)
            
            self.breakvideocapture = ft.ElevatedButton(
                "beenden",
                bgcolor=ft.colors.RED,
                on_click=lambda e, item=item: self.beendevideoaufnahme(item),
                visible=False,
            )
            self.deleteclassbuttonnew = ft.IconButton(
                icon=ft.icons.DELETE,
                bgcolor=ft.colors.RED,
                on_click=lambda e, classobject=item: self.DeleteClass(e, classobject),
            )
            self.newdeleandcamerarow = ft.Row(
                [
                    self.newcameraaufnahmebutton,
                    self.breakvideocapture,
                    self.pausevideo,
                    self.deleteclassbuttonnew,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            self.newclasscolumntemplate = ft.Column(
                [self.newtextfiel, self.newdeleandcamerarow]
            )
            self.newclasscontainertempalte = ft.Container(
                content=self.newclasscolumntemplate,
                padding=ft.padding.all(10),
                on_click=self.ZeigeaktuelelBilder,
            )
            self.newcardtemp = ft.Card(content=self.newclasscontainertempalte)
            self.listview.controls.append(self.newcardtemp)
            self.listdict[item["classindex"]] = self.newdeleandcamerarow

        self.listview.update()

    def _CreateNewTrainingClass(self):
        neue_class = {
            "classindex": self.classzeahler,
            "classname": None,
        }

        self.listederaufgabenlocalspeicher.append(neue_class)
        self.page.session.set(
            "listederaufgabenlocalspeicher", self.listederaufgabenlocalspeicher
        )
        self.classzeahler += 1
        if self.listview.height < 700:
            self.listview.height += self.dynabstandadder
            
        self._ladeliste()

    def _close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def _openbanner(self, textinfo: str = None):
        if textinfo != None:
            self.bannerfailtextcontent.value = textinfo

        self.page.banner.open = True
        self.page.update()

    def _save_file_result(self, e: ft.FilePickerResultEvent):
        self.save_file_pfad.value = e.path if e.path else "Cancelled!"
        if e.path is None:
            return

        self.save_file_pfad.update()

    

    def will_unmount(self):
        self.page.session.remove("listederaufgabenlocalspeicher")
        LaufZeitConfig.islaufzeit = False#
        LaufZeitConfig.Disable_istrainingactive()
        self.progressring.visible = False
        self.page.banner.clean()
        self.page.overlay.clear()
        self._close_banner(None)
        self.page.update()

    def did_mount(self):
        if self.page is None:
            print("fehler beim mounten")
            return
        
        
        self.listederaufgabenlocalspeicher = []
        self._CreateNewTrainingClass()
        self.page.banner = self.warningbanner
        self.page.overlay.append(self.pick_files_dialog)
        self.page.dialog = self.alertWarnhinweis
        self.alertWarnhinweis.open = True

        self.page.update()


    def changebutton(self, classitem, startbutton: bool, beendenbutton: bool):
        rowdata: ft.Row = self.listdict[classitem["classindex"]]

        rowdata.controls[0].visible = startbutton
        rowdata.controls[1].visible = beendenbutton
        rowdata.update()