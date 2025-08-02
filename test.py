from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

# Hub und Motoren initialisieren
hub = PrimeHub()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Funktion: vorwärts fahren
def forward(speed, duration):
    left_motor.run(-speed)
    right_motor.run(speed)
    wait(duration)
    left_motor.stop()
    right_motor.stop()

# Funktion: rückwärts fahren
def backward(speed, duration):
    left_motor.run(speed)
    right_motor.run(-speed)
    wait(duration)
    left_motor.stop()
    right_motor.stop()

# Funktion: drehen nach links
def turn_left(speed, duration):
    left_motor.run(speed)
    right_motor.run(speed)
    wait(duration)
    left_motor.stop()
    right_motor.stop()

# Funktion: drehen nach rechts
def turn_right(speed, duration):
    left_motor.run(-speed)
    right_motor.run(-speed)
    wait(duration)
    left_motor.stop()
    right_motor.stop()

# Hauptprogramm – Roboter fährt wie durch viele Blöcke
while True:
    turn_left(200, 2025)
    forward(200, 500)
    turn_right(200, 2025)
    forward(200, 500)