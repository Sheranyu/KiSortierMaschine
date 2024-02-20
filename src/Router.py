import flet as ft
from mainwindow.fletmaininhalt import Mainwindow, secondclass

class Router:
    def __init__(self, page: ft.Page) -> None:
        pageseite = Mainwindow(page)

        self.page = page
        self.routes = {
            "/": pageseite.mainwindow(),
            "/second": secondclass(page)
        }

        self.container = ft.Container(content=self.routes["/"])
        self.page.add(self.container)

        
    def routechange(self,route):
        self.page.views.clear()
        self.page.views.append(
            self.routes[self.page.route]
        )
        self.page.update()

    # def route_change(self, route: ft.RouteChangeEvent):
    #     self.body.content = self.routes[route.route]
    #     self.body.page.scroll = ft.ScrollMode.ALWAYS
    #     self.body.update()