import base64
from datetime import date
import os
import sys
from typing import List
import cv2
import flet as ft
from StatusMeldungen.status import WarnStatus
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


class Mainwindow(BaseWindow):
    def __new__(self, page: ft.Page) -> ft.Row:

        self.weite = 500
        self.breite = 75
        self.page = page
        # cls.text1 = ft.Text("Neues Modell erstellen", theme_style=ft.TextTheme.label_large)

        self.button1 = ft.Container(
            content=ft.ElevatedButton(
                text="Neues Modell erstellen",
                on_click=lambda e: self.page.go("/create-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button2 = ft.Container(
            content=ft.ElevatedButton(
                text="Modell laden",
                on_click=lambda e: self.page.go("/load-model"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button3 = ft.Container(
            content=ft.ElevatedButton(
                text="Starte Anwendung",
                on_click=lambda e: self.page.go("/start-application"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button4 = ft.Container(
            content=ft.ElevatedButton(
                text="Statistiken",
                on_click=lambda e: self.page.go("/statistik"),
                bgcolor=ft.colors.BLUE,
            ),
            width=self.weite,
            height=self.breite,
        )
        self.button5 = ft.Container(
            content=ft.ElevatedButton(text="Exit!", on_click=self.exit_application,bgcolor=ft.colors.BLUE,),
            
            width=self.weite,
            height=self.breite,
        )

        self.row = ft.Column(
            controls=[
                self.button1,
                self.button2,
                self.button3,
                self.button4,
                self.button5,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        self.container = ft.Container(content=self.row, expand=True)
        self.container.alignment = ft.alignment.top_center
        return self.container

    def exit_application(self):
        self.page.window_close()

    def mainwindow(self):
        pass

