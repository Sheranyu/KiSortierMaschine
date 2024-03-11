import flet as ft

class Statistiken(ft.UserControl):
    def __init__(self):
        super().__init__()
        # Initialize UI elements
        self.teile_sortiert = ft.TextField(label="Sortierte Teile", value="0", read_only=True)
        self.modus_anzeige = ft.TextField(label="Modus", value="N/A", read_only=True)
        self.mehr_sortiert = ft.TextField(label="Mehr sortiert (Farbe/Form)", value="N/A", read_only=True)
        self.laufzeit_anzeige = ft.TextField(label="Laufzeit", value="0", read_only=True)
        self.motor_drehung = ft.TextField(label="Motor Drehung", value="0", read_only=True)
        self.laden_button = ft.ElevatedButton(text="Daten laden", on_click=self.getdata)
        self.speichern_button = ft.ElevatedButton(text="Daten speichern", on_click=self.savedata)
        self.bekomme_daten_button = ft.ElevatedButton(text="Bekomme Daten", on_click=self.getdata)
        self.search_statistikdata = ft.SearchBar(on_submit=self.on_enter_search, divider_color=ft.colors.AMBER)

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
