import flet as ft

from Router import Router
from logic.KiDatenManager import KiDataManager
#from Designer.designer import





def main(page: ft.Page):
    # RegisterDI(page)
    page.title = "Flet"
    page.padding = 0
    page.window_width = 1400
    page.window_height = 800
    page.window_center()
    page.window_min_height = 1400
    page.window_min_width = 800
    router = Router(page)
    KiDataManager.classinit(page)
    page.on_route_change = router.routechange
    page.on_view_pop = router.view_pop
    page.go("/")
    

ft.app(target=main)



# def RegisterDI(page):
#     DependencyInjector.register_class("aufnahme", WebcamAufnahme())
#     DependencyInjector.register_class("TrainiertesModel",TrainiertesModel(page))