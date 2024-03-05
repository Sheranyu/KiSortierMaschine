import flet as ft

def main(page: ft.Page):


    button1 = ft.CupertinoButton("Test")
    button2 = ft.CupertinoButton("Testneu")

    containterresrow = ft.ResponsiveRow([button1,button2])
    col1 = ft.Column(col=1, controls=[ft.Text("Column 1")])
    col2 =      ft.Column(col=1, controls=[ft.Text("Column 2")])

    res =  ft.ResponsiveRow([
                col1,col2,
                ])
    page.add(
       res
    )

ft.app(target=main)