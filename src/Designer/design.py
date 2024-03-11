from abc import ABC, abstractmethod
import flet as ft

from modele.InterneDatenModele import ModelTyp


class StartSeitePageDesign(ft.UserControl, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.erkanntesobjectbeschreibung = ft.Text("Erkanntes Objekt: ")
        self.erkanntesobject = ft.Text()
        self.erkanntermodus = ft.Text()

        self.title = ft.Text("Start Application", theme_style="headlineMedium")
        self.startbutton = ft.ElevatedButton(
            "Start", bgcolor=ft.colors.BLUE, on_click=self.start
        )
        self.abbruchbutton = ft.ElevatedButton(
            "Abbruch", bgcolor=ft.colors.RED, on_click=self.abbruch, visible=False
        )
        
        self.bildvideo = ft.Image("")
        self.alertwarn = ft.AlertDialog(
            modal=False,
            title=ft.Text("Ein Fehler ist aufgetreten"),
            content=ft.Text(
                "Entweder das Model wurde nicht geladen oder die Kamera wurde nicht erkannt"
            ),
        )
        self.pr = ft.ProgressRing(width=32, height=32, stroke_width=3, visible=False)

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def abbruch(self):
        pass


class CreateModelPageDesign(ABC, ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.CameraContainer = ft.Image()

        self.classzeahler = 1
        self.boxshadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=0.4,
            color=ft.colors.BLACK,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )

      

        self.cameraaufnahmebutton = ft.FilledButton("Start Aufnahme", on_click=lambda e,anzahl=self.classzeahler :self.StartCamera(e,anzahl))
        #self.breakvideocapture = ft.FilledButton("beenden") findet man in der funktion: LadeListe()
        self.firstclasstexteingabe = ft.TextField(label="class name")
        self.deleteclassbutton = ft.IconButton(icon=ft.icons.DELETE,bgcolor=ft.colors.RED, on_click=lambda e,index=self.classzeahler: self.DeleteClass(e,index) )
        
        self.floatedbutton = ft.FloatingActionButton(col=1,content=ft.Icon(ft.icons.ADD),on_click=lambda _: self.CreateNewTrainingClass())
        

        self.title = ft.Text("Modell erstellen", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.instructions = ft.Text("Neues Modell erstellen")
        self.model_name = ft.TextField(label="Modell Name")
        self.warnhinweis_title_text = ft.Text("Warnhinweis")
        self.save_file_pfad = ft.Text()
        self.modeltyplist = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option(ModelTyp.KERAS, "Kera Model"),
                ft.dropdown.Option(ModelTyp.TORCH, "PyTorch Model"),
            ],
        )

        self.pick_files_dialog = ft.FilePicker(on_result=self.save_file_result)
        self.loadmodelbuttonpicker = ft.ElevatedButton(
            "Wähle Speicherort",
            icon=ft.icons.FILE_UPLOAD,
            on_click=lambda _: self.pick_files_dialog.get_directory_path(),
        )

        self.warhinweistext = ft.Text(
            "Trainieren eines Models funktioniert nur mit einer Nvidea GPU"
        )
        self.alertWarnhinweis = ft.AlertDialog(
            modal=False, title=self.warnhinweis_title_text, content=self.warhinweistext
        )

        self.bannerfailtextcontent = ft.Text(
            "Model Name und SpeicherOrt muss angeben werden", color=ft.colors.BLACK
        )

        self.warningbanner = ft.Banner(
            bgcolor=ft.colors.YELLOW,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, size=40),
            content=self.bannerfailtextcontent,
            actions=[ft.TextButton("Ok", on_click=self.close_banner)],
        )

        self.submit_button = ft.ElevatedButton(
            "Starte Training",
            bgcolor=ft.colors.GREEN_900,
            on_click=self.create_model,
            elevation=0,
        )
        
    @abstractmethod
    def DeleteClass(self):
        pass

    @abstractmethod
    def StartCamera(self):
        pass

    @abstractmethod
    def CreateNewTrainingClass(self):
        pass

    @abstractmethod
    def save_file_result(self):
        pass

    @abstractmethod
    def close_banner(self):
        pass

    @abstractmethod
    def create_model(self):
        pass


class LoadModelPageDesign(ABC, ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text(
            "Modell Laden", theme_style=ft.TextThemeStyle.HEADLINE_LARGE
        )
        self.text_model_laden = ft.Text(
            "Wähle ein Modell zum laden aus.", text_align=ft.TextAlign.CENTER
        )
        self.text_lade_label = ft.Text(
            "Wähle das label dazu aus", text_align=ft.TextAlign.CENTER
        )

        self.isloadedcheckbox = ft.Icon(visible=True, color=ft.colors.GREEN)
        self.isloadedcheckboxlabel = ft.Icon(visible=True, color=ft.colors.GREEN)

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
            "aktuell können nur Kera Modelle geladen werden",
            color=ft.colors.YELLOW,
            text_align=ft.TextAlign.CENTER,
        )
        self.modelhinweistextue = ft.Text(
            "Hinweis", color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER
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

        self.loaddatabutton = ft.FilledButton("Load Data", on_click=self.loaddata)

    def close_banner(self):
        pass

    def loaddata(self):
        pass

    def pick_file_label_result(self):
        pass

    def pick_files_result(self):
        pass
