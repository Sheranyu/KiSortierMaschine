class Datenverteiler():
    def __init__(self) -> None:
        self.shareddata:str = None

    def savedata(self, daten: str):
        self.shareddata = daten

    def loaddata(self):
        print(self.shareddata)


Shareddata = Datenverteiler()
