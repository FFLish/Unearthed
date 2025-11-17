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
    watch = StopWatch()
    try:
        drb_m(100,600)
        drb_k(100,-60,200)
        drb_m(400,500)
        drb_k(300,-62,900)
        drb_m(20,1000)
        drb_k(87,85,500)
        rmkmove(800,900)
        drb_m(-65,500)
        rmkmove(800,-900);  lmkmove(200, 800)
        drb_m(-25, 1000)
        drb_k(-40,-62,900)
        drb_k(270,110,500)
        drb_m(480,900)
        drb_k(90,-85,500)


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("2","3","4","5","6","7","8","1"))

def run2():
    watch = StopWatch()
    try:
        print("hallo")
        drb_m(770, 400)
        drb_k(60, 30, 300)
        drb_m(140, 400)
        drb_k(70, 60, 300)
        drb_m(130, 400)
        rmkmove(280, 400)
        lmkmove(35, -500)
        rmkmove(250, -1000)
        drb_m(-130, 400)
        drb_t(100, 300)
        drb_m(800, 400)
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
    var = int(hub_menu("3","4","5","6","7","8","1","2"))

def run3():
    try: 
        drb_m(430,300)
        lmkmove(220,-800)
        wait(200)
        lmkmove(220,200)
        lmkmove(220,-800)
        wait(200)
        lmkmove(220,200)
        lmkmove(220,-800)
        wait(200)
        lmkmove(220,200)
        drb_m(-430,300)
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","1","2","3"))

def run4():
    watch = StopWatch()
    try:
        drb_m(50,500)
        drb_t(-65,500)
        drb_k(550,20,500)
        drb_m(330,500)
        rmkmove(330,500)
        drb_m(-150, 500)
        drb_k(700,-5,500)
        rmkmove(330,-500)
        drb_k(400,5,500)
        lmkmove(350, -500)
        drb_k(-400,20,500)
        drb_m(-450,500)
        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("5","6","7","8","1","2","3","4"))

def run5():
    watch = StopWatch()
    try:
        drb_k(230, -90, 400)
        drb_m(440, 400)
        drb_t(-90, 300)
        drb_m(230, 300)
        drb_t(-10,200)
        lmkmove(1200,900)
        drb_t(10,200)
        drb_m(10,300)
        drb_m(-100,300)
        drb_t(133, 300)
        rmkmove(560, 900)
        drb_m(320, 400)
        rmkmove(210, -600)
        drb_t(22, 300)
        drb_k(-100, 82, -300)
        drb_m(780, 600)

        drb_m(5, 500)
        

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("6","7","8","1","2","3","4","5"))

def run6():
    watch = StopWatch()
    try:
        drb_m(750, 500)
        drb_t(30, 500)
        drb_m(160, 400)
        drb_k(70, 60, 500)
        drb_m(150, 500)
        lmkmove(40,-400)
        rmkmove(200,500)
        rmkmove(190,-500)
        drb_m(-170,500)
        drb_t(100,500)
        drb_m(800,1000)  


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("7","8","1","2","3","4","5","6"))

def run7():
    watch = StopWatch()
    try:

        drb_m(780, 800)
        drb_t(-42, 500)
        drb_m(180, 300)
        lmkmove(100, 600)
        drb_m(-110, 500)
        drb_t(42, 300)
        drb_m(-130, 150)
        rmkmove(100, 700)#Landkarte hoch
        drb_m(-35, 150)
        wait(500)
        lmkmove(290, 800)#dreizack runter
        lmkmove(190, -900)
        drb_m(-600, 1000)
        drb.stop()
        lmk.brake()
        rmk.brake()



        drb_m(500, 900)
        rmkmove(120, 800)
        drb_m(-500, 900)
        drb.stop()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("8","1","2","3","4","5","6","7"))

def run8():
    watch = StopWatch()
    try:

        drb_m(500, 900)
        rmkmove(120, 800)
        drb_m(-500, 900)
        drb.stop()
       
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
    var = int(hub_menu("1","2","3","4","5","6","7","8"))
    
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
    