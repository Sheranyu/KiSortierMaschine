import json

def read_and_process_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            # Die "data"-Liste enthält die JSON-Strings
            for json_str in data["data"]:
                # JSON-String in ein Python-Objekt umwandeln
                json_obj = json.loads(json_str)
                # Auf einzelne Attribute zugreifen
                print(json_obj)
                
                # Die Daten ausgeben oder weiterverarbeiten
                
    except FileNotFoundError:
        print(f"Datei '{file_path}' nicht gefunden.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Dekodieren der JSON-Datei: {e}")

# Beispielaufruf
file_path = "output_2024-02-27_14-04-29.json"
read_and_process_json(file_path)
