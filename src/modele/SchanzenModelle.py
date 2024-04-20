from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from modele.InterneDatenModele import LeuchtFarbenLampe



class LabelData(BaseModel):
    labeldata: Optional[List[str]] = []


class SchanzeBase(BaseModel):
    Topf: str
    selected: str = Field(default="")
    formcolor: str

class SchanzeB1(SchanzeBase):
    Topf: str = "b1"
    formcolor: str = LeuchtFarbenLampe.BLAU.value
class SchanzeB2(SchanzeBase):
    Topf: str = "b2"
    formcolor: str = LeuchtFarbenLampe.ROT.value

class SchanzeB3(SchanzeBase):
    Topf: str = "b3"
    formcolor: str = LeuchtFarbenLampe.GELB.value
class SchanzeB4(SchanzeBase):
    Topf: str = "b4"
    formcolor: str = LeuchtFarbenLampe.SONSTIG.value
   
class SchanzenSteuerung(BaseModel):
    B1:SchanzeB1 = Field(default_factory=SchanzeB1)
    B2: SchanzeB2 = Field(default_factory=SchanzeB2)
    B3: SchanzeB3 = Field(default_factory=SchanzeB3)
    B4: SchanzeB4 = Field(default_factory=SchanzeB4)  
    
class SchanzenBecher(Enum):
    B1: str = "b1"
    B2: str = "b2"
    B3: str = "b3"
    B4: str = "b4"  
class SchanzenSteuerungformenum(Enum):
    acht:str = "acht"
    zwanzig: str = "zwanzig"
    sechs: str = "sechs"
    sonstig: str =  "sonstig"
    
    

    