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
        self.pr = ft.ProgressRing(width=32, height=32, stroke_width = 3, visible=False)
        
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def abbruch(self):
        pass