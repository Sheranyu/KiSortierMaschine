
from modele.SchanzenModelle import SchanzeBase, SchanzenBecher, SchanzenSteuerung


def filterschanzendata(data: SchanzenSteuerung, becher: SchanzenBecher):
        if becher == SchanzenBecher.B1:
            return data.B1  
        elif becher == SchanzenBecher.B2:
            return data.B2
        elif becher == SchanzenBecher.B3:
            return data.B3
        elif becher == SchanzenBecher.B4:
            return data.B4
        else:
            raise ValueError("Ungültiger SchanzenBecher-Wert")
        
def filterschanzennachlabel(data: SchanzenSteuerung, label: str):
        label = label.strip()
        
        if label in data.B1.selected:
            return data.B1  
        elif label in data.B2.selected:
            return data.B2
        elif label in data.B3.selected:
            return data.B3
        elif label in data.B4.selected:
            return data.B4
        else:
            return None
      
    # for attr_name in data.model_fields.keys():
    #     # Prüfe, ob das Attribut ein Subtyp von SchanzeBase ist
    #     if isinstance(getattr(data, attr_name), SchanzeBase):
    #         # Prüfe, ob das Label mit dem ausgewählten Wert übereinstimmt
    #         if label == getattr(data, attr_name).selected:
    #             # Gib den entsprechenden SchanzenBase-Subtyp zurück
    #             return getattr(data, attr_name)
    # # Wenn kein passendes Label gefunden wurde, gib None zurück
    # return None