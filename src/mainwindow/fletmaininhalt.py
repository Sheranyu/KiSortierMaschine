
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
        cls.button = ft.CupertinoButton(text="Hallo click mich", 
                                            on_click=lambda e: cls.page.go("/second"),
                                            bgcolor=ft.colors.BLUE,
                                            )

        cls.row = ft.Row(controls=[cls.button], alignment=ft.MainAxisAlignment.CENTER)
        cls.container = ft.Container(content=cls.row,expand=True)
        cls.container.alignment = ft.alignment.top_center
        return cls.container
    def mainwindow(self):
        pass
        
    
class secondclass(BaseWindow):
    def __new__(cls, page: ft.Page) -> None:
        cls.page = page
        cls.button = ft.FloatingActionButton(text="CLick!", on_click=cls.pagegeher)

        cls.row = ft.Row(controls=[cls.button])
        
        return cls.button

    def pagegeher(self):
        self.page.go("/")
  