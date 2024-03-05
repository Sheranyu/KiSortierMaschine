import math

import flet as ft
import flet.canvas as cv

def main(page: ft.Page):
    cp = cv.Canvas(
        [
           
            cv.Line(x1=100,x2=100,y1=100,y2=25, 
                    paint=ft.Paint(
                        style=ft.PaintingStyle.STROKE,
                        color=ft.colors.RED,
                        stroke_width=4
                ))
          
        ],
        width=float("inf"),
        expand=True,
    )

    page.add(cp)

ft.app(main)