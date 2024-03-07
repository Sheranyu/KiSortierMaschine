import flet as ft


class Statistiken(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        # oberflächeninhalt was ich brauche:
        #
        # Anzeige für wie viele teile Sortiert worden sind
        # Anzeige für wie viele dem entsprechenden Modus: Ob Farbe oder Form
        # Anzeige: Was wurde mehr sortiert Farbe oder Form
        # Anzeige: Laufzeit der Sortiermaschine
        # Funktion: Laden der vergangenen Daten reicht als Button
        # Bonus oder je nach Kontext: Speichern der statistik
        # Hinweiß: Speichern kann auch automatisch erfolgen
        # Bonus: wie weit sich der Motor drehen musste.
        self.title = ft.Text("Alle Statisiken", theme_style="headlineMedium")
        self.button = ft.ElevatedButton("Bekomme Daten", on_click=self.getdata)
        self.SearchStatistikdata = ft.SearchBar(
            on_submit=self.onEnterSearch, divider_color=ft.colors.AMBER
        )

        self.rowcontainer = ft.Row([self.title, self.button, self.SearchStatistikdata])
        return self.rowcontainer

    def close_anchor(self):
        self.SearchStatistikdata.close_view()

    def onEnterSearch(self, e):
        self.update()

    def getdata(self, e):
        pass