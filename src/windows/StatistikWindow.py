import flet as ft
from Designer.design import StatistikPageDesign
class Statistiken(StatistikPageDesign):
    def __init__(self):
        super().__init__()
        # Initialize UI elements


    def build(self):
        # Create the title element
        title = ft.Text("Alle Statistiken", size=20, text_align="center")

        # Create buttons column
        buttons_column = ft.Column(controls=[
            self.bekomme_daten_button,
            self.laden_button,
            self.speichern_button
        ])

        # Central column for all elements
        main_layout = ft.Column(controls=[
            title,
            self.search_statistikdata,
            self.teile_sortiert,
            self.modus_anzeige,
            self.mehr_sortiert,
            self.laufzeit_anzeige,
            self.motor_drehung,
            buttons_column
        ], expand=True)

        # Container for the main layout
        center_container = ft.Container(content=main_layout, expand=True)

        return center_container

    def getdata(self, e):
        # Implementation for loading data
        pass

    def savedata(self, e):
        # Implementation for saving data
        pass

    def on_enter_search(self, e):
        # Implementation for the search function
        pass
