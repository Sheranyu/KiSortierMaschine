from abc import ABC, abstractmethod
import flet as ft

from StatusMeldungen.messageinfo import ClassCreatorSettingsMessage as CCSM
from StatusMeldungen.status import WarnStatus
from libcomponents.CustomTextField import TextFieldBCB
from modele.InterneDatenModele import Erkanntermodus, ModelTyp


class AnwendungstartPageDesign(ft.Column, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.optionsbutton = ft.IconButton(ft.icons.SETTINGS, bgcolor="blue", highlight_color="green", on_click=self.change_setting_window)
        self.laufzeit = TextFieldBCB(label="laufzeit", value="N/A", read_only=True, adaptive=True)
        self.erkanntesobject = TextFieldBCB(label="Erkanntes Objekt: ",read_only=True, value="N/A", adaptive=True)
        self.erkanntermodus = TextFieldBCB(label="Erkannter Modus: ", read_only=True,value="N/A",adaptive=True)
        self.anzahlsortierterobjekte = TextFieldBCB(label="anzahl", value="N/A", read_only=True, adaptive=True)
        self.title = ft.Text("Start Application", theme_style="headlineMedium")
        self.startbutton = ft.ElevatedButton(
            "Start", bgcolor=ft.colors.BLUE, on_click=self.start_camera
        )
        self.abbruchbutton = ft.ElevatedButton(
            "Abbruch", bgcolor=ft.colors.RED, on_click=self.abbruch, visible=False
        )
        

        self.alertwarntext = ft.Text("Entweder das Model wurde nicht geladen oder die Kamera wurde nicht erkannt")
        self.bildvideo = ft.Image("./",fit=ft.ImageFit.CONTAIN)
        self.alertwarn = ft.AlertDialog(
            modal=False,
            title=ft.Text("Ein Fehler ist aufgetreten"),
            content=self.alertwarntext
        )
        self.pr = ft.ProgressRing(width=32, height=32, stroke_width=3, visible=False)

    
    @abstractmethod
    def change_setting_window(self,e):
        pass
    
    @abstractmethod
    def start_camera(self):
        pass

    @abstractmethod
    def abbruch(self):
        pass


class CreateModelPageDesign(ABC, ft.Column):
    def __init__(self) -> None:
        super().__init__()
        border_radius = 6
        self.maxeingelesendatenseatz = TextFieldBCB(border_radius=border_radius,label="Max Dateneinlesen", value=100, input_filter=ft.NumbersOnlyInputFilter(), filled=True)
        
        self.epoches = TextFieldBCB(border_radius=border_radius,label="Epoches", value=30, input_filter=ft.NumbersOnlyInputFilter(), filled=True)
        self.lernratetextfield = TextFieldBCB(border_radius=border_radius,label="Lern Rate", value=0.001, tooltip="lernrate zwischen 0.001 und 0.01",
                                              input_filter=ft.InputFilter(regex_string=r"^[0-9.-]*$"), filled=True)
        self.batchsizetext = ft.Text("Batch Size")
        self.batchsize = ft.Slider(value=16, min=16, max=64, divisions=3, label="{value}", height=20)
        


        #self.lernrate = ft.Slider(value=0.001, min=0.001, max=0.03, divisions=33, label="{value}", round=4)
        self.settingbuttonclass = ft.FloatingActionButton(content=ft.Icon(ft.icons.SETTINGS), on_click=lambda _: self.Open_Settings_Class())
        
        self.zeigemomentanbildintext = TextFieldBCB(label="BildNummer", value="N/A", read_only=True, color=ft.colors.RED)
        self.CameraContainer = ft.Image(src="./")
        self.progressring = ft.ProgressRing(visible=False,width=32, height=32, stroke_width=3 )
        self.classzeahler = 1
        self.boxshadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=0.4,
            color=ft.colors.BLACK,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )

      

        self.cameraaufnahmebutton = ft.FilledButton("Start Aufnahme", on_click=lambda e,anzahl=self.classzeahler :self.StartCamera(e,anzahl))
        #self.breakvideocapture = ft.FilledButton("beenden") findet man in der funktion: LadeListe()
        self.firstclasstexteingabe = TextFieldBCB(label="class name")
        self.deleteclassbutton = ft.IconButton(icon=ft.icons.DELETE,bgcolor=ft.colors.RED, on_click=lambda e,index=self.classzeahler: self.DeleteClass(e,index) )
        
        self.floatedbutton = ft.FloatingActionButton(col=1,content=ft.Icon(ft.icons.ADD),on_click=lambda _: self._CreateNewTrainingClass())
        

        self.title = ft.Text("Modell erstellen", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.instructions = ft.Text("Neues Modell erstellen")
        self.model_name = TextFieldBCB(label="Modell Name")
        self.warnhinweis_title_text = ft.Text("Warnhinweis", text_align="center")
        self.save_file_pfad = ft.Text()
        self.modeltyplist = ft.Dropdown(
            width=200,
            value=ModelTyp.TORCH,
            options=[
                ft.dropdown.Option(ModelTyp.KERAS, "Kera Model"),
                ft.dropdown.Option(ModelTyp.TORCH, "PyTorch Model"),
            ],
            border_color=ft.colors.BLUE,
        )
        self.abbruchtrainingbtn = ft.ElevatedButton("abbruch",ft.icons.CANCEL, 
                                                    bgcolor=ft.colors.RED, on_click=self.cancel_ki_training, visible=False)

        self.fortschrittbalkentext = ft.Text("Aktueller fortschrit", text_align=ft.TextAlign.CENTER)
        self.fortschrittbalken = ft.ProgressBar(width=300, color=ft.colors.BLUE, bar_height=5, value=0.01)

        self.pick_files_dialog = ft.FilePicker(on_result=self._save_file_result)
        self.loadmodelbuttonpicker = ft.ElevatedButton(
            "Wähle Speicherort",
            icon=ft.icons.FILE_UPLOAD,
            on_click=lambda _: self.pick_files_dialog.get_directory_path(),
        )

        self.warhinweistext = ft.Text(
                WarnStatus.ONLY_CPU + "\n--------\n" + WarnStatus.FORBIDDEN_TWO_TRAINING, text_align=ft.TextAlign.CENTER,
                width=300
        )
        self.alertWarnhinweis = ft.AlertDialog(
            modal=False, title=self.warnhinweis_title_text, content=ft.Column([ft.Divider(),self.warhinweistext],tight=True)
        )

        self.bannerfailtextcontent = ft.Text(
            "Model Name und SpeicherOrt muss angeben werden", color=ft.colors.BLACK
        )

        self.warningbanner = ft.Banner(
            bgcolor=ft.colors.YELLOW,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, size=40),
            content=self.bannerfailtextcontent,
            actions=[ft.TextButton("Ok", on_click=self._close_banner)],
        )

        self.start_training_btn = ft.ElevatedButton(
            "Starte Training",
            bgcolor=ft.colors.GREEN_900,
            on_click=self.start_create_model,
            elevation=0,
        )
    
    @abstractmethod
    def cancel_ki_training(self):
        pass

    @abstractmethod
    def Open_Settings_Class(self):
        pass
        
    @abstractmethod
    def DeleteClass(self):
        pass

    @abstractmethod
    def StartCamera(self):
        pass

    @abstractmethod
    def _CreateNewTrainingClass(self):
        pass

    @abstractmethod
    def _save_file_result(self):
        pass

    @abstractmethod
    def _close_banner(self):
        pass

    @abstractmethod
    def start_create_model(self):
        pass


class LoadModelPageDesign(ABC, ft.Column):
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text(
            "Modell Laden", theme_style=ft.TextThemeStyle.HEADLINE_LARGE, text_align=ft.TextAlign.CENTER
        )
        self.text_model_laden = ft.Text(
            "Wähle ein Modell zum laden aus.", text_align=ft.TextAlign.CENTER
        )
        self.text_lade_label = ft.Text(
            "Wähle das label dazu aus", text_align=ft.TextAlign.CENTER
        )
        self.segmenterkanntermodus = ft.SegmentedButton(
            on_change=self.changedsegment,
            selected_icon=ft.Icon(ft.icons.RADIO_BUTTON_CHECKED,color=ft.colors.GREEN), allow_empty_selection=False,
            selected={"1"},
            segments=[
                ft.Segment(value=Erkanntermodus.FARBE.value, 
                           label=ft.Text(Erkanntermodus.FARBE.value), 
                           icon=ft.Icon(ft.icons.LOOKS_ONE)),
                ft.Segment(value=Erkanntermodus.FORM.value, 
                           label=ft.Text(Erkanntermodus.FORM.value), 
                           icon=ft.Icon(ft.icons.LOOKS_TWO)),
            ]
        )

        self.isloadedcheckbox = ft.Icon(visible=True, color=ft.colors.GREEN)
        self.isloadedcheckboxlabel = ft.Icon(visible=True, color=ft.colors.GREEN)
        self.isloadedfinal = ft.Icon(visible=True, color=ft.colors.GREEN)

        self.bannertext = ft.Text(
            "Label oder Model wurde nicht gewählt", color=ft.colors.BLACK
        )
        self.warnbanner = ft.Banner(
            content=self.bannertext,
            bgcolor=ft.colors.YELLOW,
            actions=[ft.TextButton("ok", on_click=self.close_banner)],
        )

        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.pick_file_label = ft.FilePicker(on_result=self.pick_file_label_result)

        self.modelhinweistext = ft.Text(
"""Den Farbmodus nur wählen, wenn Sie das trainierte Farbmodel nutzen.
Bei allen anderen Modelen nutzen sie bitte den: """,

            color=ft.colors.YELLOW,
            spans=[ft.TextSpan("Formodus", style=ft.TextStyle(color=ft.colors.RED))],
            text_align=ft.TextAlign.CENTER,theme_style=ft.TextThemeStyle.BODY_LARGE
        )
        self.modelhinweistextue = ft.Text(
            "Hinweis", color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER, theme_style=ft.TextThemeStyle.BODY_LARGE
        )
        self.cardseperator = ft.Divider(thickness=2)
        self.selected_files = ft.Text(visible=False)

        self.loadmodelbutton = ft.FilledTonalButton(
            "Lade KIModel",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False),
        )
        self.loadlabelbutton = ft.FilledTonalButton(
            "Lade Label",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_file_label.pick_files(allow_multiple=False),
        )

        self.loaddatabutton = ft.ElevatedButton("Load Data", on_click=self.loaddata, bgcolor="blue")


    def changedsegment(self,e):
        pass

    def close_banner(self):
        pass

    def loaddata(self):
        pass

    def pick_file_label_result(self):
        pass

    def pick_files_result(self):
        pass

#beschreibde den code   
 
class StatistikPageDesign(ft.Column,ABC):
    def __init__(self) -> None:
        super().__init__()
        self.teile_sortiert = ft.TextField(label="Sortierte Teile", value="0", read_only=True)
        self.modus_anzeige = ft.TextField(label="Modus", value="N/A", read_only=True)
        self.mehr_sortiert = ft.TextField(label="Mehr sortiert (Farbe/Form)", value="N/A", read_only=True)
        self.laufzeit_anzeige = ft.TextField(label="Laufzeit", value="0", read_only=True)
        self.motor_drehung = ft.TextField(label="Motor Drehung", value="0", read_only=True)
        self.laden_button = ft.ElevatedButton(text="Daten laden", on_click=self.getdata)
        self.speichern_button = ft.ElevatedButton(text="Daten speichern", on_click=self.savedata)
        self.bekomme_daten_button = ft.ElevatedButton(text="Bekomme Daten", on_click=self.getdata)
        self.search_statistikdata = ft.SearchBar(on_submit=self.on_enter_search, divider_color=ft.colors.AMBER)

    @abstractmethod
    def getdata(self):
        raise NotImplementedError()
    @abstractmethod
    def on_enter_search(self):
        raise NotImplementedError()
    
    
    
class ClassCreatorDesignPage(ft.UserControl,ABC):
    def __init__(self) -> None:
        super().__init__(self)
    # Kommentiert den ausgewählten Code

        self.aufnahmegestext = ft.Text(CCSM.GESSLIDERTEXT, text_align=ft.TextAlign.CENTER)
    # Slider zur Auswahl der Aufnahmegeschwindigkeit mit Standardwert von 10% und einem Bereich von 10% bis 30%
        self.aufnahmeges = ft.Slider(value=10, label="{value} BPS",divisions=20, min=10, max=30, on_change=lambda e:self.on_change(e))
        self.aufnahmegestextausgabe = ft.Text(value=self.aufnahmeges.value, text_align=ft.TextAlign.CENTER)
        # Text zur Beschreibung der Aufnahmegeschwindigkeit

        # Textfeld mit dem Label "test"
        self.textbox = ft.TextField(label="test")
    
    @abstractmethod    
    def on_change(self):
        raise NotImplementedError()
    
    
    
class SettingsPageDesign(ft.Column,ABC):
    def __init__(self) -> None:
        super().__init__()
        
        
        