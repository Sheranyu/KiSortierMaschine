
import flet as ft

class Mainwindow():
    def __init__(self,page: ft.Page) -> ft.Row:
      self.page = page
    def mainwindow(self):
        self.button = ft.CupertinoButton(text="Hallo click mich", 
                                         on_click=lambda e: self.page.go("/second"),
                                         bgcolor=ft.colors.BLUE
                                         )

        self.row = ft.Row(controls=[self.button])
        self.container = ft.Container(content=self.row,expand=True, height=200)
        return self.container
    
class secondclass():
    def __new__(self, page: ft.Page) -> None:
        self.page = page
        self.button = ft.FloatingActionButton(text="CLick!", on_click=self.pagegeher)

        self.row = ft.Row(controls=[self.button],left=100)
        
        return self.row

    def pagegeher(self):
        self.page.go("/")
  