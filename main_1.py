from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
import umath as m
from pybricks.tools import multitask, run_task

hub = PrimeHub()

digits = {
    "1": [
        [0,1,1,0,0],
        [1,1,1,0,0],
        [0,1,1,0,0],
        [0,1,1,0,0],
        [1,1,1,1,1],
    ],
    "2": [
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    "3": [
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,1,1,1,0],
        [0,0,0,0,1],
        [1,1,1,1,0],
    ],
    "4": [
        [1,0,0,1,0],
        [1,0,0,1,0],
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,0,1,0],
    ],
    "5": [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,0,1],
        [1,1,1,1,0],
    ],
    "6": [
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ],
    "7": [
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,0,0,0,0],
    ],
    "8": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    "9": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,1],
        [0,0,0,0,1],
        [0,1,1,1,0],
    ],
}
hub.system.set_stop_button({Button.BLUETOOTH})
lmA=Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
rmB=Motor(Port.F)
lmk=Motor(Port.D)
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

#print(menu())
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
    drb.use_gyro(False)
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
    drb.use_gyro(False)
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


def run1():
    try:
        # drb.straight(300, Stop.HOLD, False)
        drb_m(500,500)
        drb_t(90,500)
        drb_m(500,500)
        drb_t(90,500)
        drb_m(500,500)
        drb_t(90,500)
        drb_m(500,500)
        drb_t(90,500)
        drb_m(500,500) 
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("2","3","4","5","6","7","8","9","1"))
    print("var")

def run2():
    try:
        drb_m(500,500)
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("3","4","5","6","7","8","9","1","2",))


def run3():
    try:
        drb_m(500,500)
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","9","1","2","3"))


def run4():
    try:
        drb_m(250,300)
        drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("5","6","7","8","9","1","2","3","4"))


def run5():
    try:
        drb_m(570,400,500)
        drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("6","7","8","9","1","2","3","4","5"))
    


def run6():
    try:

        lmkmove(100,100)
        drb_m(50,500)
        drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("7","8","9","1","2","3","4","5","6"))


def run7():
    try:
        drb_m(-500,900)
        drb.stop()
        lmk.brake()
        rmk.brake()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("8","9","1","2","3","4","5","6","7"))


def run8():
    try:
        drb_m(200,300)
        drb.stop()
        lmk.brake()
        rmk.brake()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("9","1","2","3","4","5","6","7","8"))


def run9():
    try:
        drb_m(50000,900,1500)
        drb.stop()
        lmk.brake()
        rmk.brake()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9"))


var = int(hub_menu("1","2","3","4","5","6","7","8","9",))
print(var)

while True:
    if var ==1:
        print("run1")
        run1() 
    if var ==2:
        print("run2")
        run2()
    if var==3:
        print("run3")
        run3()
    if var==4:
        print("run4")
        run4()
    if var==5:
        print("run5")
        run5()
    if var==6:
        print("run6")
        run6()
    if var==7:
        print("run7")
        run7()
    if var==8:
        print("run8")
        run8()
    if var==9:
        print("run9")
        run9()

print(x,y)

async def counter():
    a=1   
    while True:
        print(a)
        a=1


print("neu")