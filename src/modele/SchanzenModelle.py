from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class SchanzeBase(BaseModel):
    Topf: str
    Farbe: List[str] = Field(default_factory=list)
    Form: List[str] = Field(default_factory=list)
    selected: str = Field(default="")

class SchanzeB1(SchanzeBase):
    Topf: str = "b1"

class SchanzeB2(SchanzeBase):
    Topf: str = "b2"

class SchanzeB3(SchanzeBase):
    Topf: str = "b3"

class SchanzeB4(SchanzeBase):
    Topf: str = "b4"
   
class SchanzenSteuerung(BaseModel):
    acht:SchanzeB1 = Field(default_factory=SchanzeB1)
    sechs: SchanzeB2 = Field(default_factory=SchanzeB2)
    zwanzig: SchanzeB3 = Field(default_factory=SchanzeB3)
    sonstig: SchanzeB4 = Field(default_factory=SchanzeB4)  
    
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
    
    

    