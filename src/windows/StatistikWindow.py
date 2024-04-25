import flet as ft
from Designer.design import StatistikPageDesign
from db.db_and_models.models import EndStastik
from logic.Statistikloader import KIStatistikLoader
from logic.datenverarbeitung import Stastikverarbeiter
class Statistiken(StatistikPageDesign):
    def __init__(self):
        super().__init__()
        # Initialize UI elements
        self.Statistiklaoder = KIStatistikLoader()

    def build(self):
        # Create the title element
        title = ft.Text("Alle Statistiken", size=20, text_align="center")

        # Create buttons column


        # Central column for all elements
        main_layout = ft.Column(controls=[
            title,
            self.search_statistikdata,
            self.teile_sortiert,
            self.modus_anzeige,
            self.durchschnittsprozent,
            self.avg_erkennung,
            self.laufzeit_anzeige,
        ], expand=True)

        # Container for the main layout
        center_container = ft.Container(content=main_layout, expand=True)

        return center_container

    def loadinitdata(self,e):
        pass
        
        
    def getdata(self, e):
        # Implementation for loading data
        pass

    def close_anchor(self, e: ft.ControlEvent):
        text = f"{e.control.title.value}"
        data = self.Statistiklaoder.loadendstatistik(e.control.data)
        
        laufzeitdata = self.Statistiklaoder.loadstatistik(e.control.data)
      
        lzddurchschnitt = Stastikverarbeiter().getDurchnschnittDaten(laufzeitdata)
            
        if data:
            self.laufzeit_anzeige.value = data.laufzeit
            self.teile_sortiert.value = data.stueckzahl
            self.avg_erkennung.value = lzddurchschnitt.max_vorkommen
            self.durchschnittsprozent.value = lzddurchschnitt.durchschnitprozent
            self.modus_anzeige.value = lzddurchschnitt.modus
        else:
            self.laufzeit_anzeige.value = "N/A"
            self.teile_sortiert.value = "N/A"
            
        self.search_statistikdata.close_view(text)
        self.update()

    def savedata(self, e):
        # Implementation for saving data
        pass

    def on_enter_search(self, e):
        # Implementation for the search function
        pass
    
    def on_change_search(self,e: ft.TapEvent):
        pass
    
    
    def will_unmount(self):
        self.search_statistikdata.controls.clear()
    
    def did_mount(self):
        result = KIStatistikLoader().loaddatum()
        for data in result:
            listdata = ft.ListTile(5,title=ft.Text(data.Datum), on_click=self.close_anchor,data=data.Id)
            self.search_statistikdata.controls.append(listdata)
        self.search_statistikdata.controls.reverse()
        self.update()
