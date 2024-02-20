import flet as ft
from mainwindow.fletmaininhalt import Mainwindow 
from Router import Router

def main(page: ft.Page):
    page.title = "Flet"
    page.padding = 0
    page.bgcolor = ft.colors.BLUE_GREY_200
    router = Router(page)
    page.on_route_change = router.routechange
    page.go("/")
    


ft.app(target=main)