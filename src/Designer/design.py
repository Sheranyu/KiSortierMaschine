from abc import ABC, abstractmethod
import flet as ft

class StartSeitePageDesign(ft.UserControl,ABC):
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text("Start Application", theme_style="headlineMedium")
        self.startbutton = ft.ElevatedButton("Start",bgcolor=ft.colors.BLUE, on_click=self.start)
        self.abbruchbutton = ft.ElevatedButton("Abbruch", bgcolor=ft.colors.RED, on_click=self.abbruch, visible=False)
        self.FarbeoderFormtext = ft.Text()
        self.bildvideo = ft.Image("")
        self.alertwarn = ft.AlertDialog(modal=False, title=ft.Text("Ein Fehler ist aufgetreten"), 
                                        content=ft.Text("Entweder das Model wurde nicht geladen oder die Kamera wurde nicht erkannt"))
        self.pr = ft.ProgressRing(width=32, height=32, stroke_width = 3, visible=False)
        
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def abbruch(self):
        pass
    
    
class CreateModelPageDesign(ABC,ft.UserControl):
    def __init__(self) -> None:
        pass
    
    
class LoadModelPageDesign(ABC,ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text("Modell Laden", theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.instructions = ft.Text("Wähle ein Modell zum laden aus.", text_align=ft.TextAlign.CENTER)
        
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.modelhinweistext = ft.Text("aktuell können nur Kera Modelle geladen werden", color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER)
        self.modelhinweistextue = ft.Text("Hinweis", color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER)
        self.cardseperator = ft.Divider(thickness=2)
        self.selected_files = ft.Text(visible=False)
        
        self.loadmodelbutton = ft.FilledTonalButton("Lade KIModel",icon=ft.icons.UPLOAD_FILE, 
                                                on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False))
    @abstractmethod   
    def pick_files_result():
        pass
    
