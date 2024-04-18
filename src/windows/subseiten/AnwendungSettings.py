
from typing import Any, Dict, Tuple
import flet as ft

from libcomponents.Components import EOverlay, EilmnerZeichner

class AnwendungSetting(ft.Container):
    def __init__(self, content: ft.Control | None = None, appbar: ft.AppBar | ft.CupertinoAppBar | None = None, navigation_bar: ft.NavigationBar | ft.CupertinoNavigationBar | None = None, bottom_app_bar: ft.BottomAppBar | None = None, bottom_sheet: ft.Control | None = None, drawer: ft.NavigationDrawer | None = None, end_drawer: ft.NavigationDrawer | None = None, floating_action_button: ft.FloatingActionButton | None = None, floating_action_button_location: ft.FloatingActionButtonLocation | None | ft.Offset | Tuple[float | int, float | int] = None, bgcolor: str | None = None, ref: ft.Ref | None = None, width: None | int | float = None, height: None | int | float = None, left: None | int | float = None, top: None | int | float = None, right: None | int | float = None, bottom: None | int | float = None, expand: None | bool | int = None, expand_loose: bool | None = None, col: Dict[str, int | float] | int | float | None = None, opacity: None | int | float = None, rotate: None | int | float | ft.Rotate = None, scale: None | int | float | ft.Scale = None, offset: None | ft.Offset | Tuple[float | int, float | int] = None, aspect_ratio: None | int | float = None, animate_opacity: None | bool | int | ft.Animation = None, animate_size: None | bool | int | ft.Animation = None, animate_position: None | bool | int | ft.Animation = None, animate_rotation: None | bool | int | ft.Animation = None, animate_scale: None | bool | int | ft.Animation = None, animate_offset: None | bool | int | ft.Animation = None, on_animation_end=None, tooltip: str | None = None, visible: bool | None = None, disabled: bool | None = None, data: Any = None, key: str | None = None, adaptive: bool | None = None):
        super().__init__(content, appbar, navigation_bar, bottom_app_bar, bottom_sheet, drawer, end_drawer, floating_action_button, floating_action_button_location, bgcolor, ref, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, key, adaptive)
        
        
        self.textbox = ft.Text("das ist ein test",bgcolor="red")
        self.button = ft.FilledButton("hallo")
        self.cp = EilmnerZeichner("b1",stroke_color=ft.colors.BLUE)
        self.cp2 = EilmnerZeichner("b2")
        self.cp3 = EilmnerZeichner("b3")
        self.cp4 = EilmnerZeichner("b4")
        overlay1 = EOverlay()
        
        
        self.eilmercontainerrow = ft.Container(ft.Row([self.cp,self.cp2, self.cp3,self.cp4], 
                                         alignment=ft.MainAxisAlignment.CENTER),bgcolor="blue")
        self.expanendcontainer = ft.TransparentPointer(ft.Container(height=300,bgcolor="red"))
        self.expanedstack = ft.Stack([self.expanendcontainer,self.eilmercontainerrow])
        
        self.platzhalter = ft.Container(bgcolor=ft.colors.TRANSPARENT,expand=True, expand_loose=True)
        self.columcon =  ft.Column([self.textbox, self.button,self.platzhalter,self.expanedstack])
        self.padding = ft.padding.all(10)
        self.content = self.columcon
        