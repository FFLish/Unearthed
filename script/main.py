from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
import umath as m
from pybricks.tools import multitask, run_task
from pybricks.hubs import PrimeHub

hub = PrimeHub()

hub.system.set_stop_button({Button.BLUETOOTH})
lmg = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
rmg = Motor(Port.D)
lmk = Motor(Port.F)
rmk = Motor(Port.B)
radius = 31.2
drb = DriveBase(lmg, rmg, 62.4, 158)
drb.use_gyro(True)

def lmkmove(distance, speed):
    lmk.reset_angle(0)
    while abs(lmk.angle()) < distance:
        if Button.BLUETOOTH in hub.buttons.pressed():
            lmk.brake()
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            lmk.brake()
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
        lmk.run(speed)
    lmk.brake()

def rmkmove(distance, speed):
    rmk.reset_angle(0)
    while abs(rmk.angle()) < distance:
        if Button.BLUETOOTH in hub.buttons.pressed():
            rmk.brake()
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            rmk.brake()
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
        rmk.run(speed)
    rmk.brake()

def drb_m(distance, speed, acceleration=900, second_function=None, dist2=0, speed2=0):
    print("start function")
    drb.settings(speed, acceleration, 90, 500)
    print("finish settings")
    drb.straight(distance, Stop.HOLD, False)
    print("move done")
    if second_function:
        second_function(dist2, speed2)
    while not drb.done():
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
        wait(10)

def drb_t(angle, speed, acceleration=500, second_function=None, dist2=0, speed2=0):
    print(hub.imu.heading())
    drb.settings(400, 400, speed, acceleration)
    drb.turn(angle, Stop.HOLD, False)
    if second_function:
        second_function(dist2, speed2)
    while not drb.done():
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
        wait(10)

def drb_k(radius, angle, speed, acceleration=500, second_function=None, dist2=0, speed2=0):
    print(f"Starting heading: {hub.imu.heading()}")
    
    drb.settings(straight_speed=speed, straight_acceleration=acceleration, 
                turn_rate=100, turn_acceleration=acceleration)
    
    drb.curve(radius, angle, wait=False)
    
    if second_function:
        second_function(dist2, speed2)
    
    while not drb.done():
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
        wait(10)
def run1(): 
    try:
        drb_m(800, 500)
        drb_t(-42, 400)
        drb_m(150, 400)
        lmkmove(100, 400)
        wait(100)
        drb_m(-110, 400)
        drb_t(42, 400)
        drb_m(-175, 250)
        wait(450)
        lmkmove(390, 500)
        lmkmove(390,-500)
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
        drb_m(610, 400)
        drb_t(-49, 400)
        drb_m(270, 400)
        drb_t(-84, 400)
        drb_m(520, 400)
        drb_t(-48, 400)
        drb_m(420, 400)
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
    
try:
    var = int(hub_menu("1","2","3","4","5","6","7","8"))
except Exception:
    var = 1

while True:
    if var == 1:
        print("run1")
        run1() 
    elif var == 2:
        print("run2")
        run2()
    elif var == 3:
        print("run3")
        run3()
    elif var == 4:
        print("run4")
        run4()
    elif var == 5:
        print("run5")
        run5()
    elif var == 6:
        print("run6")
        run6()
    elif var == 7:
        print("run7")
        run7()
    elif var == 8:
        print("run8")
        run8()
    wait(100)
    