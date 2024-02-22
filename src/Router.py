import flet as ft
from mainwindow.fletmaininhalt import Mainwindow, secondclass, CreateModelPage, LoadModelPage, StartApplicationPage
class Router:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.register_route()
       
    def view_pop(self,view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
    def routechange(self,route):
        self.page.views.clear()
        
        self.page.views.append(
            ft.View("/",controls=[Mainwindow(self.page)], appbar=ft.AppBar(title=ft.Text("Sortiermaschine"), bgcolor=ft.colors.BLUE))
        )  
        for key, value in self.routes.items():
            if self.page.route == key:
                self.page.views.append(value)

        self.page.update()

    def register_route(self) -> None:
        self.routes = {
            "/second": ft.View("/second",controls=[secondclass(self.page)], 
                appbar=ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/create-model": ft.View("/create-model", controls=[CreateModelPage(self.page)],
                appbar=ft.AppBar(title=ft.Text("Modell erstellen"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/load-model": ft.View("/load-model", controls=[LoadModelPage(self.page)], 
                appbar=ft.AppBar(title=ft.Text("Modell laden"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/start-application": ft.View("/start-application", controls=[StartApplicationPage(self.page)], 
                appbar=ft.AppBar(title=ft.Text("Anwendung starten"), bgcolor=ft.colors.SURFACE_VARIANT))
        }
        
    # def route_change(self, route: ft.RouteChangeEvent):
    #     self.body.content = self.routes[route.route]
    #     self.body.page.scroll = ft.ScrollMode.ALWAYS
    #     self.body.update()