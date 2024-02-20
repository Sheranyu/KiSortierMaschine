import customtkinter as cck
import tkinter as tk
from mainwindow.inhalt import Mainwindows

class App(cck.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")

        mainwindow = Mainwindows(self)
        
        mainwindow.pack(side="bottom")

      

if __name__ == "__main__":
    app = App()
    app.mainloop()