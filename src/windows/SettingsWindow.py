

import flet as ft
from Designer.design import SettingsPageDesign
from lib.Components import BPSSlider, SelectCamera


class SettingsWindow(SettingsPageDesign):
    def __init__(self) -> None:
        super().__init__()
        
        
    def build(self):
        self.bpsslider = BPSSlider()
        self.cameraselecter = SelectCamera()
        
        self.columend = ft.Column([self.bpsslider,self.cameraselecter])
        return self.columend
        
    def did_mount(self):
        
        pass