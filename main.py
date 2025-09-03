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



def drb_m(distance,speed,acceleration=900,second_function = None ,dist2=0,speed2=0):
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
        drb_m(800, 900)
        drb_t(-42, 400)
        drb_m(150, 400)
        lmkmove(100, 400)
        wait(100)
        drb_m(-110, 400)
        drb_t(42, 500)
        drb_m(-175, 200)
        wait(425)
        lmkmove(390, 650)
        lmkmove(390,-650)
        drb_m(-530, 1000)

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
        drb_m(600,500)
        rmkmove(500,-600)
        drb_m(-590,500)

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("3","4","5","6","7","8","9","1","2",))


def run3():
    try:
        drb_m(590,400)
        rmkmove(1000,500)
        drb_m(-590,400)
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","9","1","2","3"))


def run4():
    try:
        drb_m(620, 400)
        drb_t(30, 400)
        drb_m(170, 400)
        lmkmove(100, 500)
        drb_m(40, 500)
        rmkmove(180, 500)
        drb_m(40, 500)
        rmkmove(180, -500)
        drb_t(46, 400)
        drb_m(-144, 400)
        drb_t(70, 400)
        drb_m(613, 400)
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