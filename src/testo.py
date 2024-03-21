import flet as ft

def main(page: ft.Page):

    colum = ft.Column([ft.FilledButton("hallo", on_click=clickme),ft.FilledButton("test2")])
    container = ft.Container(colum, animate=ft.animation.Animation(1000,ft.animation.AnimationCurve.BOUNCE_IN),visible=False)

    page.add(container)
    page.add(ft.FilledButton("click me", on_click=clickanimation))


def clickme(e):
    pass

def clickanimation():
    pass

ft.app(target=main)