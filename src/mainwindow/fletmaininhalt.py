
import flet as ft

class Mainwindow():
    def __init__(self,page: ft.Page) -> ft.Row:
      self.page = page
    def mainwindow(self):
        
        self.button = ft.CupertinoButton(text="Hallo click mich", 
                                         on_click=lambda e: self.page.go("/second"),
                                         bgcolor=ft.colors.BLUE
                                         
                                         )

        self.row = ft.Row(controls=[self.button], alignment=ft.MainAxisAlignment.CENTER)
        self.container = ft.Container(content=self.row,expand=True, height=200)
        self.container.alignment = ft.alignment.top_center
        return self.container
    
class secondclass():
    def __new__(self, page: ft.Page) -> None:
        self.page = page
        self.button = ft.FloatingActionButton(text="CLick!", on_click=self.pagegeher)

        self.row = ft.Row(controls=[self.button])
        
        return self.row

    def pagegeher(self):
        self.page.go("/")
  