
import customtkinter as ctk
import tkinter as tk


class Mainwindows(ctk.CTkFrame):
    def __init__(self,master) -> None:
        super().__init__(master)
        self.button = ctk.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(padx=5,pady=20)
        

        print("test")

    def button_callbck(self):
        print("button clicked")