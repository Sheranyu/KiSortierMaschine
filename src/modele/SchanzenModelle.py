from enum import Enum
from pydantic import BaseModel, Field


class SchanzeAcht(BaseModel):
    name:str = Field(default="acht")
    Topf:str = Field(default="b1")

class SchanzeSechs(BaseModel):
    name:str = Field(default="sechs")
    Topf:str = Field(default="b2")

class Schanzezwanzig(BaseModel):
    name:str = Field(default="zwanzig")
    Topf:str = Field(default="b3")

class SchanzeSonstig(BaseModel):
    name:str = Field(default="sonstig")
    Topf:str = Field(default="b4")

class SchanzenSteuerungForm(BaseModel):
    acht:SchanzeAcht
    sechs: SchanzeSechs
    zwanzig: Schanzezwanzig
    sonstig: SchanzeSonstig
    background: str = Field(default="background")
    
    
class SchanzenSteuerungformenum(Enum):
    acht:str = "acht"
    zwanzig: str = "zwanzig"
    sechs: str = "sechs"
    sonstig: str =  "sonstig"
    