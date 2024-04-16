

import flet as ft
from Designer.design import SettingsPageDesign
from libcomponents.Components import BPSSlider, COMSelector, SelectCamera


class SettingsWindow(SettingsPageDesign):
    def __init__(self) -> None:
        super().__init__()
        self.bpsslider = BPSSlider()
        self.cameraselecter = SelectCamera()
        self.com = COMSelector()
        self.controls = [self.bpsslider,self.cameraselecter,self.com]
        
