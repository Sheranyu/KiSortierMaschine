
import customtkinter as ctk


class Mainwindows(ctk.CTkFrame):
    def __init__(self,master) -> None:
        super().__init__(master)
        self.button = ctk.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(anchor="w")
        print("test")

    def button_callbck(self):
        print("button clicked")