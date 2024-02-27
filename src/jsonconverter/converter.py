import json

def converttoJson(inhalt):
    json_data = json.dumps(inhalt.__dict__, indent=2)
    return json_data