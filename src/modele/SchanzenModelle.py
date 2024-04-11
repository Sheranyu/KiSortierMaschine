from pydantic import BaseModel, Field




class SchanzeAcht(BaseModel):
    name:str = Field(default="acht")
    Topf:str = Field(default="b1")

class SchwanzeSechs(BaseModel):
    name:str = Field(default="sechs")
    Topf:str = Field(default="b2")

class Schanzezwanzig(BaseModel):
    name:str = Field(default="zwanzig")
    Topf:str = Field(default="b3")

class SchwanzeSonstig(BaseModel):
    name:str = Field(default="sonstig")
    Topf:str = Field(default="b4")

class SchanzenSteuerungForm(BaseModel):
    acht:SchanzeAcht
    sechs: SchwanzeSechs
    zwanzig: Schanzezwanzig
    sonstig: SchwanzeSonstig
    background: str = Field(default="background")