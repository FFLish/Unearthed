print("Hebel-Berechnung (in g und cm)\n")

# Eingaben
gewicht_arm = float(input("Gewicht Arm (g): "))
gewicht_gegenarm = float(input("Gewicht Gegenarm (g): "))
last1 = float(input("Zusätzliche Last auf Seite 1 (g): "))
laenge1 = float(input("Länge Arm (cm): "))
laenge2 = float(input("Länge Gegenarm (cm): "))

# Gesamtkraft auf den Arm
gesamt1 = gewicht_arm + last1

# Drehmoment auf den Arm
moment1 = gesamt1 * laenge1

# Berechnung der benötigten Gesamtmasse auf Gegenarm
gesamt2 = moment1 / laenge2

# Benötigte zusätzliche Last auf Gegenarm
last2 = gesamt2 - gewicht_gegenarm

print("\nErgebnis:")
print(f"Benötigte zusätzliche Last auf Gegenarm: {last2:.2f} g")



