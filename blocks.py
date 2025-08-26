from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


rmk=Motor(Port.B)
lmk=Motor(Port.F)
lm=Motor(Port.D, positive_direction=Direction.CLOCKWISE)
rm=Motor(Port.E)
radius = 62,4
#drb = DriveBase(lm, rm, 55, 130) #alt noch ändern auf neuer roboter  
hub = PrimeHub()


def lkmmove(distance,speed):
    lmk.reset_angle(0)
    while abs(lmk.angle())<distance:
        lmk.run(speed)
    lmk.brake()

def rmkmove(distance,speed):
    rmk.reset_angle(0)
    while abs(rmk.angle())<distance:
        rmk.run(speed)
    rmk.brake()
    
def drb_m(distance,speed,acceleration=900,second_function = None,dist2=0,speed2=0):
    drb.settings(speed,acceleration,800,500)#max straight_speed=97(argument.1)
    drb.straight(distance,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise CompleteExit("ENDE GELÄNDE!")

def drb_t(angle,speed,acceleration=500,second_function = None,dist2=0,speed2=0):
    drb.use_gyro(True)
    print(hub.imu.heading())
    drb.settings(400,400,speed,acceleration)
    drb.turn(angle,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise CompleteExit("ENDE GELÄNDE!")