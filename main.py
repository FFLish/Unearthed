from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
import umath as m
from pybricks.tools import multitask, run_task
from pybricks.hubs import PrimeHub

hub = PrimeHub()

hub.system.set_stop_button({Button.BLUETOOTH})
lmA = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
rmB = Motor(Port.D)
lmk = Motor(Port.F)
rmk = Motor(Port.B)
radius = 31.2
drb = DriveBase(lmA, rmB, 62.4, 158)
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
    
    print(f"Final heading: {hub.imu.heading()}")

def run1(): 
    watch = StopWatch()
    try:
        drb_m(710, 350)
        drb_t(-42, 400)
        drb_m(120, 150)
        lmkmove(100, 400)
        wait(100)
        drb_m(-130, 200)
        drb_t(-110, 200)
        drb_m(-120, 200)
        drb_t(30, 200)
        drb_k(-90, -15, 150,rmkmove(1600, 1200))
        drb_m(-50, 200)
        drb_k(-90, -12, 150)
        drb_m(50,200)
        lmkmove(300,500)
        drb_m(-150, 200)
        lmkmove(550,-500)
        rmkmove(130,-700)
        lmkmove(400,500)
        wait(500)
        drb_m(140,200)
        lmkmove(200,-500)
        rmkmove(300,-700)

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("2","3","4","5","6","7","8","9","1"))

def run2():
    watch = StopWatch()
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

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("3","4","5","6","7","8","9","1","2"))

def run3():

    watch = StopWatch()
    try:
        lmkmove(220,1000)
        lmkmove(-200,1200)

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","9","1","2","3"))

def run4():

    watch = StopWatch()
    try:
        
        drb_m(180, 300)
        drb_t(-90, 300)
        drb_m(800, 500)
        drb_t(-90, 300)
        drb_m(160, 500)
        drb_t(-20, 300)
        lmkmove(850, 1000)#kran
        
        drb_m(-250, 400)
        drb_k(-15, 200, 200)
        rmkmove(350, 500)
        drb_m(206, 400)
        rmkmove(300, -500) #Statur
        drb_m(-200, 400) 
        drb_t(130, 400)
        drb_m(150, 300)
        drb_m(-
        
        
        300, 300)
        drb_k(60, -80, 800)
        drb_m(550, 800)

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("5","6","7","8","9","1","2","3","4"))

def run5():
    
    watch = StopWatch()
    
    try:
        drb_m(200, 300)
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    global var
    var = int(hub_menu("6","7","8","9","1","2","3","4","5"))

def run6():

    watch = StopWatch()

    try:
        drb_m(710, 350)
        drb_t(-42, 400)
        drb_m(120, 150)
        lmkmove(100, 400)
        wait(100)
        drb_m(-130, 200)
        drb_t(-110, 200)
        drb_m(-120, 200)
        drb_t(30, 200)
        drb_k(-90, -15, 150,rmkmove(1600, 1200))
        #drb_m(50,200)
        #lmkmove(300,500)
        drb_m(-50, 200)
        drb_k(-90, -12, 150)
        drb_m(50,200)
        lmkmove(300,500)
        drb_m(-150, 200)
        lmkmove(550,-500)
        rmkmove(130,-700)
        lmkmove(400,500)
        wait(500)
        drb_m(140,200)
        lmkmove(200,-500)
        rmkmove(300,-700)
        drb.stop()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("7","8","9","1","2","3","4","5","6"))

def run7():

    watch = StopWatch()

    try:
        drb_m(500, 600)
        rmkmove(110, 400)
        drb_m(-500, 580)
        drb.stop()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("8","9","1","2","3","4","5","6","7"))

def run8():

    watch = StopWatch()

    try:
        drb_m(200, 300)
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("9","1","2","3","4","5","6","7","8"))

def run9():

    watch = StopWatch()
    
    try:
        drb_m(200, 300)
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9"))

var = int(hub_menu("1","2","3","4","5","6","7","8","9"))
print(var)

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
    elif var == 9:
        print("run9")
        run9()
    wait(100)