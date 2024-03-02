# Bestehende Variable mit einem bestimmten Namen
meine_variable = 42

# Name der Variable als Zeichenkette
variablen_name = "meine_variable"

# Zugriff auf die Variable mithilfe des Namens als Zeichenkette
wert_der_variable = globals()[variablen_name]

print(wert_der_variable)  # Ausgabe: 42
