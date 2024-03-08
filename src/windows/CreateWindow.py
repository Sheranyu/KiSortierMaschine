from typing import List
from Designer.design import CreateModelPageDesign
from StatusMeldungen.status import WarnStatus
import flet as ft
from configordner.settings import LaufZeitConfig

from logic.aufnahme import WebcamAufnahme, ZeigeBildan
from modele.InterneDatenModele import KIModelLoader, KiClassList

class CreateModelPage(CreateModelPageDesign):
    def __init__(self):
        super().__init__()
        self.dynabstandadder = 700/5
        self.aufnahme = WebcamAufnahme()
        self.listederaufgabenlocalspeicher: List = []
        
    def build(self):
        self.listview = ft.ListView(spacing=8, padding=15, auto_scroll=False,height=40)

        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            width=300,
            divider_color=ft.colors.AMBER,
            controls=[
                ft.ExpansionPanel(
                    header=ft.Container(self.submit_button, padding=ft.padding.all(5)),
                    content=ft.Container(
                        ft.Column([self.modeltyplist]), padding=ft.padding.all(5)
                    ),
                )
            ],
        )

        self.listcontainer = ft.Container(
            content=self.listview,
            bgcolor=ft.colors.BLACK87,
            border_radius=ft.border_radius.all(7),
            shadow=self.boxshadow,
            col=4,
            
            
        )

        self.containercolum = ft.Column(
            controls=[
               ft.Container(ft.Column([
                    self.title,
                    self.instructions,
                    self.model_name,
                
                    self.loadmodelbuttonpicker,
                    self.save_file_pfad,
                    self.panel,
                    self.CameraContainer
                    
               ]))
            ],
           col=3,
        )
    
        
        #self.floatingactionstack = ft.Stack(controls=[self.floatedbutton],height=200,width=200)
        self.listwithbutton = ft.ResponsiveRow([self.listcontainer,self.floatedbutton],columns=5)
        self.columleft = ft.Column([self.listwithbutton],col=3)
       
        
        self.rowcontainer = ft.ResponsiveRow([self.columleft ,self.containercolum])
        self.endcontainer = ft.Container(content=self.rowcontainer,expand=True)
        return self.endcontainer
    
    

    def DeleteClass(self,e,classitem):
        print(classitem)
        daten = self.page.session.get("listederaufgabenlocalspeicher")
        daten = [item for item in daten if item["classindex"] != classitem["classindex"] ]
        self.page.session.set("listederaufgabenlocalspeicher", daten)
        if len(self.listview.controls) <=5:
            self.listview.height -= self.dynabstandadder

        self.ladeliste()

    def ZeigeaktuelelBilder(self, e):
        #print("zeige aktuelel bilder")
        pass

    def StartCamera(self, classitem,textfield:ft.TextField):
        print("instartcamera")
        if self.save_file_pfad.value == "Cancelled!" or self.save_file_pfad.value == None:
            self.openbanner(WarnStatus.PFAD_IS_EMPTY)
            return
        if textfield.value == None or textfield.value == "":
            self.openbanner(WarnStatus.CLASS_NAME_EMPTY)
            return
        
        textfield.disabled = True
        self.changebutton(classitem,False,True)
        LaufZeitConfig.islaufzeit = True
        newdata = KiClassList(classitem["classindex"], textfield.value,self.save_file_pfad.value)
        self.update()
        #starte aufnahme
        for frame in self.aufnahme.StarteAufnahme(newdata):
            ZeigeBildan(frame,self.CameraContainer)

        #self.beendevideoaufnahme(classitem)
    def changebutton(self,classitem, startbutton: bool, beendenbutton: bool):
        rowdata: ft.Row = self.listdict[classitem["classindex"]]
        
        rowdata.controls[0].visible = startbutton
        rowdata.controls[1].visible = beendenbutton
        rowdata.update()
        
    def beendevideoaufnahme(self,classitem):
        self.changebutton(classitem,True,False)
        LaufZeitConfig.islaufzeit = False   
    
    def saveclassnameeingabe(self,e:ft.ControlEvent, item):
        daten = self.page.session.get("listederaufgabenlocalspeicher")
        
        
        for oneitem in daten:
            if oneitem["classindex"] == item["classindex"]:
                oneitem["classname"] = e.data
                
        print(daten)
        self.page.session.set("listederaufgabenlocalspeicher",daten)
        self.page.update()

    def ladeliste(self):
        self.listederaufgabenlocalspeicher = self.page.session.get("listederaufgabenlocalspeicher")
        print(self.listederaufgabenlocalspeicher)
        self.listview.controls.clear()
        self.listdict = {}
        for item in self.listederaufgabenlocalspeicher:
            
            self.newtextfiel = ft.TextField(label="class name",value=item["classname"], on_change=lambda e,item=item: self.saveclassnameeingabe(e,item))
            self.newcameraaufnahmebutton = ft.FilledButton(
                "Start Aufnahme", on_click=lambda e,anzahl=item,text=self.newtextfiel: self.StartCamera(anzahl,text)
            )
            self.breakvideocapture = ft.ElevatedButton("beenden",bgcolor=ft.colors.RED, on_click=lambda e,item=item: self.beendevideoaufnahme(item), visible=False)
            self.deleteclassbuttonnew = ft.IconButton(icon=ft.icons.DELETE,bgcolor=ft.colors.RED,
                                                    on_click=lambda e,classobject= item :self.DeleteClass(e,classobject))
            self.newdeleandcamerarow = ft.Row([self.newcameraaufnahmebutton,self.breakvideocapture ,self.deleteclassbuttonnew], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
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
        
        

    def CreateNewTrainingClass(self):
        neue_class = {
            "classindex": self.classzeahler,
            "classname": None,
        }

        self.listederaufgabenlocalspeicher.append(neue_class)
        self.page.session.set("listederaufgabenlocalspeicher", self.listederaufgabenlocalspeicher)
        self.classzeahler += 1
        if self.listview.height < 700:
            self.listview.height += self.dynabstandadder
            print(self.listview.height)
        self.ladeliste()
        


    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def openbanner(self, textinfo: str = None):
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

        self.kimodelsaver = KIModelLoader(
            self.model_name.value, self.save_file_pfad.value, self.modeltyplist.value
        )
        self.page.session.set("kimodelsaver", self.kimodelsaver.__dict__)

    def will_unmount(self):
        self.page.session.remove("listederaufgabenlocalspeicher")
        print(self.page.session.get("listederaufgabenlocalspeicher"))
        LaufZeitConfig.islaufzeit = False
        self.page.update()

    def did_mount(self):
        self.listederaufgabenlocalspeicher = []
        self.CreateNewTrainingClass()
        self.page.banner = self.warningbanner
        self.page.overlay.append(self.pick_files_dialog)
        self.page.dialog = self.alertWarnhinweis
        self.alertWarnhinweis.open = True

        self.page.update()