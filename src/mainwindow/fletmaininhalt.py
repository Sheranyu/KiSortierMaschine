import flet as ft

class BaseWindow:
    _page = None  # Klassenattribut für das page-Objekt

    @classmethod
    def set_page(cls, page: ft.Page) -> None:
        cls._page = page
    
    def __init__(cls,page: ft.Page) -> None:
        cls._page = page

class Mainwindow(BaseWindow):
    def __new__(cls,page: ft.Page) -> ft.Row:
        cls.page = page
        cls.button1 = ft.CupertinoButton(text="Hallo click mich", on_click=lambda e: cls.page.go("/second"), bgcolor=ft.colors.BLUE)
        cls.button2 = ft.CupertinoButton(text="Neues Modell erstellen", on_click=lambda e: cls.page.go("/create-model"), bgcolor=ft.colors.BLUE)
        cls.button3 = ft.CupertinoButton(text="Modell laden", on_click=lambda e: cls.page.go("/load-model"), bgcolor=ft.colors.BLUE)
        cls.button4 = ft.CupertinoButton(text="Sortieren!!!", on_click=lambda e: cls.page.go("/start-application"), bgcolor=ft.colors.BLUE)
        cls.row = ft.Row(controls=[cls.button1, cls.button2, cls.button3, cls.button4], alignment=ft.MainAxisAlignment.CENTER)
        cls.container = ft.Container(content=cls.row, expand=True)
        cls.container.alignment = ft.alignment.top_center
        return cls.container
    
    def mainwindow(self):
        pass
        
class secondclass(BaseWindow):
    def __new__(cls, page: ft.Page) -> None:
        cls.page = page
        cls.button = ft.FloatingActionButton(text="Mehr Durstlöscher kaufen!", width=200, on_click=cls.pagegeher)
        cls.row = ft.Row(controls=[cls.button])
        return cls.button

    def pagegeher(self):
        self.page.go("/home")
    
class CreateModelPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
    def build(self):
        self.title = ft.Text("Modell erstellen", style="headlineMedium")
        self.instructions = ft.Text("Neues Modell erstellen")
        self.model_name = ft.TextField(label="Modell Name")
        self.submit_button = ft.ElevatedButton(text="erstellen", on_click=self.create_model)

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
        self.title = ft.Text("Modell Laden", style="headlineMedium")
        self.instructions = ft.Text("Wähle ein Modell zum laden aus.")
        #self.file_picker = ft.FilePicker(accept=".model", on_result=self.load_model)

        return ft.Column(
            controls=[self.title, self.instructions],
            spacing=10
        )
    
    def load_model(self, e):
        pass

class StartApplicationPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    
    def build(self):
        self.title = ft.Text("Start Application", style="headlineMedium")
        self.instructions = ft.Text("Wähle deine Sortieroptionen.")
        
        self.sorting_options = ft.Dropdown(
            label="Sortieren nach",
            options=[
                #ft.DropdownOption("Farbe", "farbe"),
                #ft.DropdownOption("Form", "form")
            ]
        )
        self.start_button = ft.ElevatedButton(text="Start", on_click=self.start_application)

        return ft.Column(
            controls=[self.title, self.instructions, self.sorting_options, self.start_button],
            spacing=10
        )
    
    def start_application(self, e):
        pass

  