import cv2
import tkinter as tk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.canvas = Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", width=10, command=self.snapshot)
        self.btn_snapshot.pack(padx=10, pady=10)

        self.update()
        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print("Snapshot taken!")

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = self.convert_to_photoimage(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.window.after(10, self.update)

    def convert_to_photoimage(self, frame):
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(image=image)
        return photo

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Hauptprogramm
root = tk.Tk()
app = WebcamApp(root, "Webcam App")
