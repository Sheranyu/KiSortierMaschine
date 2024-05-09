from sqlalchemy import Sequence

from db.db_and_models.models import Statistik
import pandas as pd

from modele.InterneDatenModele import Statistikausgewertet


class Stastikverarbeiter():
    def getDurchnschnittDaten(self, statistikdaten: Sequence[Statistik])-> Statistikausgewertet:
        
        df = pd.DataFrame([vars(d) for d in statistikdaten])

# Entferne alle Zeilen, in denen label_name "background" ist
        df['label_name'] = df['label_name'].str.strip()
        df = df[df['label_name'] != 'background']
        
        max_vorkommen = df["label_name"].value_counts().idxmax()
        modus = df["modus"][0]
        print(modus)
        durhschhnitprozent = df["confidence_score"].mean()        
        
        durchschnitdaten = Statistikausgewertet(modus=str(modus),max_vorkommen=str(max_vorkommen),durchschnitprozent=str(durhschhnitprozent))
        
        return durchschnitdaten