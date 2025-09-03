from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
import umath as m
from pybricks.tools import multitask, run_task

hub = PrimeHub()

hub.system.set_stop_button({Button.BLUETOOTH})
lmA=Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
rmB=Motor(Port.D)
lmk=Motor(Port.F)
rmk=Motor(Port.B)
radius = 31.2
drb = DriveBase(lmA, rmB, 62.4, 158)
#drb.heading_control.enabled = True
strecke = (m.radians(lmA.angle())*radius+m.radians(rmB.angle())*radius)/2
alteStrecke = strecke
x = 0
y = 0
var = 0
drb.use_gyro(True)

def menu(starting_number=1):
    showing = starting_number
    while True:
        if hub.buttons.pressed()=={Button.LEFT}:
            while hub.buttons.pressed()=={Button.LEFT}:
                continue
            showing -=1
            print(showing)
        elif hub.buttons.pressed()=={Button.RIGHT}:
            while hub.buttons.pressed()=={Button.RIGHT}:
                continue
            showing +=1
            print(showing)
        elif hub.buttons.pressed()=={Button.CENTER}:
            while hub.buttons.pressed()=={Button.CENTER}:
                continue
            return showing

def position_aktualisieren():
    global alteStrecke, x, y
    strecke = (m.radians(lmA.angle())*radius+m.radians(rmB.angle())*radius)/2
    sdStrecke = strecke - alteStrecke
    richtung = m.radians(hub.imu.heading())
    deltaX = m.cos(richtung) * sdStrecke
    deltaY = m.sin(richtung) * sdStrecke
    x += deltaX
    y += deltaY
    alteStrecke = strecke


def drive(xnewpos,ynewpos,speed,speed2=100):
    global x
    global y
    acceleration=10
    turnspeed = speed*3/4
    ankathete = xnewpos-x
    gegenkathete = ynewpos-y
    zufahrenstrecke = m.sqrt(ankathete**2+gegenkathete**2)
    while zufahrenstrecke>0.7:
        if abs(speed2)/50>zufahrenstrecke:
            speed2 = zufahrenstrecke*50*speed2/abs(speed2)
        elif speed2<speed:
            speed2 = speed2+acceleration
        elif speed2>speed:
            speed2=speed-acceleration
        position_aktualisieren()
        ankathete = xnewpos-x
        gegenkathete = ynewpos-y
        winkel = m.atan(gegenkathete/ankathete)
        zufahrenstrecke = m.sqrt(ankathete**2+gegenkathete**2)
        if ankathete/abs(ankathete)==-1:
            lmA.run(speed2-(winkel+m.pi-m.radians(hub.imu.heading()))*-turnspeed)
            rmB.run(speed2+(winkel+m.pi-m.radians(hub.imu.heading()))*-turnspeed)
        else:
            lmA.run(speed2-(winkel-m.radians(hub.imu.heading()))*-turnspeed)
            rmB.run(speed2+(winkel-m.radians(hub.imu.heading()))*-turnspeed)
    lmA.brake()
    rmB.brake()


def heading():
    if hub.imu.heading()>0:
        heading = abs(hub.imu.heading())%360
    else:
        heading = 360-(abs(hub.imu.heading())%360)
    return heading


def lmkmove(distance,speed):
    lmk.reset_angle(0)
    while abs(lmk.angle())<distance:
        lmk.run(speed)
    lmk.brake()


def rmkmove(distance,speed):
    rmk.reset_angle(0)
    while abs(rmk.angle())<distance:
        rmk.run(speed)
    rmk.brake()


def move(speed,acceleration, endbedingung, distance = 0,speed2=0,brake1 = True):
    weiterfahren = True
    lmA.reset_angle(0)
    rmB.reset_angle(0)
    gyrostart=hub.imu.heading()
    gyroende=hub.imu.heading()
    while weiterfahren:
        togo = distance-abs(lmA.angle())
        if abs(speed2)/5>togo and endbedingung == "distance":
            speed2 = togo*5*speed2/abs(speed2)
        elif speed2<speed:
            speed2 = speed2+acceleration
        elif speed2>speed:
            speed2 = speed2-acceleration           
        aditional = (rmB.angle())-(lmA.angle())
        gyro=gyrostart-hub.imu.heading()
        gyroextra=gyroende-hub.imu.heading()
        lmA.run(speed2*1+aditional*0+(gyro*3-gyroextra*1))    
        rmB.run(speed2*1-aditional*0-(gyro*3-gyroextra*1))
        gyroende=hub.imu.heading()
        if endbedingung == 2:
            weiterfahren = ls2.reflection() > 9
        elif endbedingung == 1:
            weiterfahren = distance > abs(lmA.angle())
    if brake1== True:
        lmA.hold()
        rmB.hold()


def turn(speed, angle):
    acceleration = 5
    speed2=100
    stopdis = 10
    while abs(heading()-angle)>1:
        position_aktualisieren()
        if heading()-angle>180:
            if abs(speed2)/stopdis>360-(heading()+angle)%360:
                speed2 = (360-(heading()+angle)%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(speed2)
            rmB.run(-speed2)
        elif (heading()-angle)/(abs(heading()-angle))==-1:
            if abs(speed2)/stopdis>angle-heading():
                speed2 = ((abs(heading()-angle))%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(speed2)
            rmB.run(-speed2)
        else:
            if abs(speed2)/stopdis>abs(angle-heading())%360:
                speed2 = (abs(angle-heading())%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(-speed2)
            rmB.run(speed2)
    lmA.brake()
    rmB.brake()


def drivedis(speed,distance,speed2):
    global x
    global y
    acceleration=10
    turnspeed = 10
    winkel = 0
    ankathete = m.cos(hub.imu.heading())*distance
    gegenkathete = m.sin(hub.imu.heading())*distance
    drive(ankathete+x,gegenkathete+y,speed,speed2)


def drb_m(distance,speed,acceleration=900,second_function = None,dist2=0,speed2=0):
    #drb.heading_control.enabled = True
    print("start function")
    drb.settings(speed,acceleration,90, 500)
    print("finish settings")
    drb.straight(distance,Stop.HOLD,False)
    print("move done")
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            '''global var
            var=var-1'''
            raise SystemExit("ENDE GELÄNDE!")
            



def drb_t(angle,speed,acceleration=500,second_function = None,dist2=0,speed2=0):
    #drb.heading_control.enabled = True
    print(hub.imu.heading())
    drb.settings(400,400,speed,acceleration)
    drb.turn(angle,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            '''global var
            var=var-1'''
            raise SystemExit("ENDE GELÄNDE!")

