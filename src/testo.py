from dataclasses import Field, dataclass


@dataclass
class test():
    name: str = Field(init=True)
    alter: int
    
    
    
testklasse = test("hallo", 10)
print(testklasse)