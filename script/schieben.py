from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Port, Direction
from pybricks.tools import wait

# Hub und Motoren initialisieren
hub = PrimeHub()
right_motor = Motor(Port.C)  # Nur rechter Motor wird verwendet

# Variablen initialisieren
distance_count = 0
angle_count = 0
current_measurement = None  # None, 'distance' oder 'angle'


# Radparameter
wheel_diameter = 62  # mm
PI = 3.14159
wheel_circumference = wheel_diameter * PI  # mm

# Funktion zur Umrechnung von Motorwinkel in cm
def angle_to_cm(angle_degrees):
    # Umrechnung: Grad -> Umdrehungen -> Strecke in mm -> cm
    revolutions = angle_degrees / 360
    distance_mm = revolutions * wheel_circumference
    return distance_mm / 10  # in cm

# Hauptprogramm - Smiley am Anfang anzeigen


hub.display.char('B')

while True:
    # Warte auf Taste gedrückt
    pressed = hub.buttons.pressed()

    if Button.RIGHT in pressed:
        if current_measurement == 'distance':
            # Move-Messung beenden und neue starten
            right_angle = right_motor.angle()
            # Vorwärts = negative Werte, Rückwärts = positive Werte
            right_distance_cm = -angle_to_cm(right_angle)
            distance_count += 1
            print("drb_m(" + str(round(right_distance_cm, 1)) + ", 400)")

            # Neue Move-Messung sofort starten
            right_motor.reset_angle(0)
            hub.display.char('M')

        elif current_measurement == 'angle':
            # Turn-Messung beenden und Move starten
            gyro_heading = hub.imu.heading()
            angle_count += 1
            print("drb_t(" + str(round(gyro_heading)) + ", 400)")

            # Move-Messung starten
            right_motor.reset_angle(0)
            current_measurement = 'distance'
            hub.display.char('M')

        else:
            # Erste Move-Messung starten
            right_motor.reset_angle(0)
            current_measurement = 'distance'
            hub.display.char('M')

        # Warte bis Taste losgelassen wird
        while Button.RIGHT in hub.buttons.pressed():
            wait(10)

    elif Button.LEFT in pressed:
        if current_measurement == 'angle':
            # Turn-Messung beenden und neue starten
            gyro_heading = hub.imu.heading()
            angle_count += 1
            print("drb_t(" + str(round(gyro_heading)) + ", 400)")

            # Neue Turn-Messung sofort starten
            hub.imu.reset_heading(0)
            hub.display.char('T')

        elif current_measurement == 'distance':
            # Move-Messung beenden und Turn starten
            right_angle = right_motor.angle()
            # Vorwärts = negative Werte, Rückwärts = positive Werte
            right_distance_cm = -angle_to_cm(right_angle)
            distance_count += 1
            print("drb_m(" + str(round(right_distance_cm, 1)) + ", 400)")

            # Turn-Messung starten
            hub.imu.reset_heading(0)
            current_measurement = 'angle'
            hub.display.char('T')

        else:
            # Erste Turn-Messung starten
            hub.imu.reset_heading(0)
            current_measurement = 'angle'
            hub.display.char('T')

        # Warte bis Taste losgelassen wird
        while Button.LEFT in hub.buttons.pressed():
            wait(10)

    # Prüfen ob Programm beendet werden soll
    elif Button.BLUETOOTH in pressed:
        # Aktuelle Messung beenden falls vorhanden
        if current_measurement == 'distance':
            right_angle = right_motor.angle()
            # Vorwärts = negative Werte, Rückwärts = positive Werte
            right_distance_cm = -angle_to_cm(right_angle)
            distance_count += 1
            print("drb_m(" + str(round(right_distance_cm, 1)) + ", 400)")
        elif current_measurement == 'angle':
            gyro_heading = hub.imu.heading()
            angle_count += 1
            print("drb_t(" + str(round(gyro_heading)) + ", 400)")

        break

    wait(10)

hub.display.off()
