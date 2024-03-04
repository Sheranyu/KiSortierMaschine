import flet as ft

class Counter():
    def __new__(cls) -> None:
        cls.fttext = ft.Text("neu")
        cls.fttext1 = ft.Text("neu")
        cls.fttext2 = ft.Text("neu")


        cls.button = ft.FilledButton("testbutton",expand=True)

        cls.row = ft.Row([cls.fttext,cls.button],expand=True)
        

        cls.columtest = ft.Column([cls.row,cls.row,cls.row,cls.row])


        cls.container = ft.Row(controls=[cls.columtest],expand=True)
        return cls.container
        

def main(page):
    page.add(Counter())

ft.app(target=main)