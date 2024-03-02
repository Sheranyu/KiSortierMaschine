from enum import Enum

class ModelTyp(Enum):
    KERAS = "kera"
    ONNX = "onnx"
    TORCH = "torch"

# Zugriff auf Enum-Werte
print(ModelTyp(0))      # Gibt ModelTyp.KERAS aus
print(ModelTyp.ONNX.value)  # Gibt "onnx" aus

# Iteration über Enum-Werte
for model_typ in ModelTyp:
    print(model_typ)

# Vergleich von Enum-Werten
if ModelTyp.TORCH.value == "torch":  # Gibt False aus, da die Typen unterschiedlich sind
    print("Gleich")
else:
    print("Ungleich")
