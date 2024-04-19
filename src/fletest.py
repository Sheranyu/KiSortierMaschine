from enum import Enum
from typing import List, Type, Union
from pydantic import BaseModel, Field



class SchanzenBecher(Enum):
    B1: str = "b1"
    B2: str = "b2"
    B3: str = "b3"
    B4: str = "b4"





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
    
def select_schanze_class(becher: SchanzenBecher) -> Union[Type[SchanzeB1], Type[SchanzeB2], Type[SchanzeB3], Type[SchanzeB4]]:
    class_mapping = {
        SchanzenBecher.B1: SchanzeB1,
        SchanzenBecher.B2: SchanzeB2,
        SchanzenBecher.B3: SchanzeB3,
        SchanzenBecher.B4: SchanzeB4,
    }
    try:
        return class_mapping[becher]
    except KeyError:
        raise ValueError("Ungültiger SchanzenBecher-Wert")


# Test


test = SchanzenSteuerung()
test.acht.Form = ["hallo","test"]
print(test.model_dump())
# selected_class = select_schanze_class(SchanzenBecher.B1)
# instance = selected_class()
# print(instance.model_dump())
