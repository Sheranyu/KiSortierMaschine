

#datei ist nur zum testen von paar sachen#

class ModelDataSingelton():
    KiModelpfad = None
    Modelname = None
    @classmethod
    def __init__(cls, KiModelpfad=None,Modelname=None) -> None:
        cls.KiModelpfad = KiModelpfad
        cls.Modelname = Modelname

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ModelData(metaclass=SingletonMeta):
    def __init__(self, KiModelpfad, Modelname):
        self.KiModelpfad = KiModelpfad
        self.Modelname = Modelname

# Beispiel der Verwendung des Singleton
singleton_instance_1 = ModelData("Pfad1", "Modell1")
singleton_instance_2 = ModelData("Pfad2", "Modell2")

print(singleton_instance_1 is singleton_instance_2)  # Ausgabe: True






# Erstellen von Instanzen der Klasse
objekt1 = ModelDataSingelton(KiModelpfad="Pfad1", Modelname="Modell1")
objekt2 = ModelDataSingelton(KiModelpfad="Pfad2", Modelname="Modell2")

# Zugriff auf Klassenattribute
print(objekt1.KiModelpfad)  # Ausgabe: Pfad2
print(objekt2.Modelname)    # Ausgabe: Modell2
