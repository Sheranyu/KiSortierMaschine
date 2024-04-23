import flet as ft
from windows.AnwendunglaufWindow import StartApplicationPage
#from windows.subseiten.ClassCreatorSettingsWindow import SettingsClassCreator
from windows.CreateWindow import CreateModelPage
from windows.LoadWindow import LoadModelPage
from windows.SettingsWindow import SettingsWindow
from windows.StatistikWindow import Statistiken

from windows.fletmaininhalt import Mainwindow
from windows.info_window import Infoseite

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
            ft.View("/",controls=[Mainwindow(self.page)], 
                    appbar=ft.AppBar(title=ft.Text("Sortiermaschine"),
                                     actions=[ft.IconButton(ft.icons.INFO,ft.colors.BLACK,40, on_click=lambda _: self.page.go("/info"))],
                    bgcolor=ft.colors.BLUE),
                    
                    )
        )  
        for route in self.view_list:
            for key, value in self.routes.items():
                if route.startswith(key):
                    self.page.views.append(value)
        
        self.page.update()


    def register_route(self) -> None:
        self.create_model_view = ft.View("/create-model", controls=[CreateModelPage()],
                appbar=ft.AppBar(title=ft.Text("Modell erstellen"), bgcolor=ft.colors.SURFACE_VARIANT), 
                )
        
        self.load_model_view = ft.View("/load-model", controls=[LoadModelPage()], 
                appbar=ft.AppBar(title=ft.Text("Modell laden"), bgcolor=ft.colors.SURFACE_VARIANT),
                )
        
        self.start_application_view = ft.View("/start-application",scroll=True, controls=[StartApplicationPage() ], 
                appbar=ft.AppBar(title=ft.Text("Anwendung starten"), bgcolor=ft.colors.SURFACE_VARIANT),
                
                )
        
        self.statistik_view = ft.View("/statistik", controls=[Statistiken()],
                appbar=ft.AppBar(title=ft.Text("Statisiken"), bgcolor=ft.colors.SURFACE_VARIANT),
                )
        
        self.settings_view = ft.View("/settings", controls=[SettingsWindow()],
                appbar=ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT)
                )
        
        # self.classcreatorsettings_view = ft.View("/classcreatorsettings", controls=[SettingsClassCreator(self.page)],
        #                                          appbar=ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT))
        
        self.infoview = ft.View("/info",controls=[Infoseite()], 
                                appbar=ft.AppBar(title=ft.Text("info")))
        
        self.routes = {
            "/create-model": self.create_model_view,
            "/load-model": self.load_model_view,
            "/start-application": self.start_application_view,
            "/statistik": self.statistik_view,
            "/settings": self.settings_view,
            "/info": self.infoview,
            #"/classcreatorsettings": self.classcreatorsettings_view
        }
        
    # def route_change(self, route: ft.RouteChangeEvent):
    #     self.body.content = self.routes[route.route]
    #     self.body.page.scroll = ft.ScrollMode.ALWAYS
    #     self.body.update()
    
    
