from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Port, Direction
from pybricks.tools import wait

hub = PrimeHub()
right_motor = Motor(Port.C)  

distance_count = 0
angle_count = 0
current_measurement = None 


wheel_diameter = 62
PI = 3.14159
wheel_circumference = wheel_diameter * PI

def angle_to_cm(angle_degrees):
    revolutions = angle_degrees / 360
    distance_mm = revolutions * wheel_circumference
    return distance_mm / 10  



hub.display.char('B')

while True:

    pressed = hub.buttons.pressed()

    if Button.RIGHT in pressed:
        if current_measurement == 'distance':
            right_angle = right_motor.angle()
            right_distance_cm = -angle_to_cm(right_angle)
            distance_count += 1
            print("drb_m(" + str(round(right_distance_cm, 1)) + ", 400)")

            right_motor.reset_angle(0)
            hub.display.char('M')

        elif current_measurement == 'angle':
            gyro_heading = hub.imu.heading()
            angle_count += 1
            print("drb_t(" + str(round(gyro_heading)) + ", 400)")

            right_motor.reset_angle(0)
            current_measurement = 'distance'
            hub.display.char('M')

        else:
            right_motor.reset_angle(0)
            current_measurement = 'distance'
            hub.display.char('M')

        while Button.RIGHT in hub.buttons.pressed():
            wait(10)

    elif Button.LEFT in pressed:
        if current_measurement == 'angle':
            gyro_heading = hub.imu.heading()
            angle_count += 1
            print("drb_t(" + str(round(gyro_heading)) + ", 400)")

            hub.imu.reset_heading(0)
            hub.display.char('T')

        elif current_measurement == 'distance':
            right_angle = right_motor.angle()
            right_distance_cm = -angle_to_cm(right_angle)
            distance_count += 1
            print("drb_m(" + str(round(right_distance_cm, 1)) + ", 400)")

            hub.imu.reset_heading(0)
            current_measurement = 'angle'
            hub.display.char('T')

        else:
            hub.imu.reset_heading(0)
            current_measurement = 'angle'
            hub.display.char('T')

        while Button.LEFT in hub.buttons.pressed():
            wait(10)

    elif Button.BLUETOOTH in pressed:
        if current_measurement == 'distance':
            right_angle = right_motor.angle()
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
