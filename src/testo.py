import json

# Beispiel-Dictionary
data = ["hi","test","testnbeu"]

# Pfad zur Textdatei, in die die Daten geschrieben werden sollen
dateipfad = "daten.txt"

# Daten als JSON in die Textdatei schreiben
with open(dateipfad, 'w') as datei:
    for item in data:
        datei.write(str(item) + "\n")

print("Daten wurden erfolgreich in die Datei geschrieben.")
