import flet as ft
from windows.fletmaininhalt import Mainwindow 
from Router import Router
#from Designer.designer import 

def main(page: ft.Page):
    page.title = "Flet"
    page.padding = 0
    page.window_width = 1400
    page.window_height = 800
    
    page.window_center()
    router = Router(page)
    page.on_route_change = router.routechange
    page.on_view_pop = router.view_pop
    page.go("/")

ft.app(target=main, view=ft.AppView.FLET_APP_WEB)

