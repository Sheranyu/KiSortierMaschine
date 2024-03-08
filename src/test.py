class MyClass:
    def __init__(self, value,value3):
        self.value = value

    @classmethod
    def create_instance_with_default_value(cls):
        # Klassenmethode erstellt eine neue Instanz mit einem Standardwert
        default_value = 42
        testvalue = 50
        return cls(default_value,testvalue)

# Verwende die Klassenmethode, um eine Instanz zu erstellen
my_instance = MyClass.create_instance_with_default_value()

# Zugriff auf die Instanzvariable
print(my_instance.value)  # Gibt 42 aus
