import base64
from datetime import date
import os
import sys
from typing import List
import cv2
import flet as ft
from logic.kilauflogic import KiDatenVerarbeitung
from db.CRUD.DatumSpeicherung import CreateDatumSpeicherung
from db.CRUD.Statistik import StatistikCreater
from PIL import Image
from configordner.settings import LaufZeitConfig
from db.db_and_models.models import Statistik
from db.db_and_models.session import sessiongen
from modele.InterneDatenModele import KIModelsaverData, KiData, KiClassList
from Designer.design import (
    CreateModelPageDesign,
    LoadModelPageDesign,
    AnwendungstartPageDesign,
)
from logic.aufnahme import  WebcamAufnahme, ZeigeBildan


class BaseWindow:
    _page = None  # Klassenattribut für das page-Objekt

    @classmethod
    def set_page(cls, page: ft.Page) -> None:
        cls._page = page

    def __init__(cls, page: ft.Page) -> None:
        cls._page = page


class Mainwindow(ft.Column):
    def __init__(self, page: ft.Page) -> ft.Row:
        super().__init__()
        self.weite = 500
        self.breite = 75
        self.page = page
        self.animasizedur = ft.animation.Animation(100)
        # cls.text1 = ft.Text("Neues Modell erstellen", theme_style=ft.TextTheme.label_large)

        self.button1 = ft.Container(
            content=ft.ElevatedButton(
                text="Neues Modell erstellen",
                on_click=lambda e: self.page.go("/create-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
            on_hover=self.animatecontainer,
            animate_scale=self.animasizedur,
        )
        self.button2 = ft.Container(
            content=ft.ElevatedButton(
                text="Modell laden",
                on_click=lambda e: self.page.go("/load-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
            on_hover=self.animatecontainer,
            animate_scale=self.animasizedur,
        )
        self.button3 = ft.Container(
            content=ft.ElevatedButton(
                text="Starte Anwendung",
                on_click=lambda e: self.page.go("/start-application"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
            on_hover=self.animatecontainer,
            animate_scale=self.animasizedur,
        )
        self.button4 = ft.Container(
            content=ft.ElevatedButton(
                text="Statistiken",
                on_click=lambda e: self.page.go("/statistik"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
            on_hover=self.animatecontainer,
            animate_scale=self.animasizedur,
        )
        self.exitbutton = ft.Container(
            content=ft.ElevatedButton(text="Exit!", on_click=self.exit_application,bgcolor=ft.colors.BLUE,),
            
            width=self.weite,
            height=self.breite,
            on_hover=self.animatecontainer,
            animate_scale=self.animasizedur,
        )
        
        self.settingbutton = ft.Container(
            content=ft.ElevatedButton(text="settings", 
                                      on_click=lambda e: self.page.go("/settings"),
                                      bgcolor=ft.colors.BLUE,
                                    #   on_hover=self.animatecontainer,

                                    #   on_blur=self.animatecontainer,
                                      ),
            on_hover=self.animatecontainer,
            width=self.weite,
            height=self.breite,
            animate_scale=self.animasizedur,
             
        )
        

        self.finalcolumn = ft.Column(
            controls=[
                self.button1,
                self.button2,
                self.button3,
                self.button4,
                self.settingbutton,
                self.exitbutton,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
           
        )
        
        
        
        
        self.container = ft.Container(content=self.finalcolumn ,alignment=ft.alignment.center, height=self.page.height)
        #self.container.alignment = ft.alignment.top_center
        self.controls = [self.container]
        self.alignment = ft.MainAxisAlignment.CENTER

    def animatecontainer(self,e: ft.HoverEvent):          
            if e.control.scale == 0.95:     
                e.control.scale = 1
                e.control.update()
            else:
                e.control.scale = 0.95
                e.control.update()
           
  
    
    
    def exit_application(self,e):
        self.page.window_close()

    def mainwindow(self):
        pass

