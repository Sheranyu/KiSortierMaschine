import flet as ft
from windows.fletmaininhalt import Mainwindow, CreateModelPage, LoadModelPage, StartApplicationPage, Statistiken
class Router:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.register_route()
        self.view_list = []
        self.vorherigelement = ""
       
    def view_pop(self,view):
        self.page.views.pop()
        self.view_list.pop()    
        top_view = self.page.views[-1]
        self.vorherigelement = top_view.route
        self.page.go(top_view.route)
        
    def routechange(self,route):
        
        if self.vorherigelement != self.page.route:
            self.view_list.append(self.page.route)
            
        self.page.views.clear()
        
        self.page.views.append(
            ft.View("/",controls=[Mainwindow(self.page)], appbar=ft.AppBar(title=ft.Text("Sortiermaschine"), bgcolor=ft.colors.BLUE))
        )  
        for route in self.view_list:
            for key, value in self.routes.items():
                if route.startswith(key):
                    self.page.views.append(value)
        print(self.view_list)
        self.page.update()

    def register_route(self) -> None:
        self.routes = {
            "/create-model": ft.View("/create-model", controls=[CreateModelPage(self.page)],
                appbar=ft.AppBar(title=ft.Text("Modell erstellen"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/load-model": ft.View("/load-model", controls=[LoadModelPage(self.page)], 
                appbar=ft.AppBar(title=ft.Text("Modell laden"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/start-application": ft.View("/start-application", controls=[StartApplicationPage()], 
                appbar=ft.AppBar(title=ft.Text("Anwendung starten"), bgcolor=ft.colors.SURFACE_VARIANT)),
            "/statistik": ft.View("/statistik", controls=[Statistiken(self.page)],
                appbar=ft.AppBar(title=ft.Text("Statisiken"), bgcolor=ft.colors.SURFACE_VARIANT)),
        }
        
    # def route_change(self, route: ft.RouteChangeEvent):
    #     self.body.content = self.routes[route.route]
    #     self.body.page.scroll = ft.ScrollMode.ALWAYS
    #     self.body.update()