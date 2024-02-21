import flet as ft
from mainwindow.fletmaininhalt import Mainwindow, secondclass

class Router:
    def __init__(self, page: ft.Page) -> None:

        self.page = page
       
        self.pageseite = Mainwindow(self.page)
        self.routes = {
            "/second": ft.View("/second",controls=[
                                secondclass(self.page)], appbar=ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT))
        }
   
    def view_pop(self,view):
        
        print("hallo welt")
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
    def routechange(self,route):
        self.page.views.clear()
        self.page.views.append(
            ft.View("/",controls=[self.pageseite.mainwindow()], appbar=ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT))
        )  
        for key, value in self.routes.items():
            if self.page.route == key:
                self.page.views.append(value)

        
        self.page.update()

    # def route_change(self, route: ft.RouteChangeEvent):
    #     self.body.content = self.routes[route.route]
    #     self.body.page.scroll = ft.ScrollMode.ALWAYS
    #     self.body.update()