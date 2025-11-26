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
class StopRun(Exception):
    def __init__(self, message: str = "", stop_program: bool = False):
        super().__init__(message)
        self.message = message
        self.stop_program = stop_program

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
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            lmk.brake()
            wait(1000)
            raise StopRun("ENDE GELÄNDE!")
        lmk.run(speed)
    lmk.brake()

def rmkmove(distance, speed):
    rmk.reset_angle(0)
    while abs(rmk.angle()) < distance:
        if Button.BLUETOOTH in hub.buttons.pressed():
            rmk.brake()
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            rmk.brake()
            wait(1000)
            raise StopRun("ENDE GELÄNDE!")
        rmk.run(speed)
    rmk.brake()

def drb_m(distance,speed,acceleration=900,second_function = None,dist2=0,speed2=0):
    print("start function")
    drb.settings(speed,acceleration,90, 500)
    print("finish settings")
    drb.straight(distance,Stop.HOLD,False)
    print("move done")
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")

def drb_t(angle,speed,acceleration=500,second_function = None,dist2=0,speed2=0):
    print(hub.imu.heading())
    drb.settings(400,400,speed,acceleration)
    drb.turn(angle,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")

def drb_k(radius, angle, speed, acceleration=500, second_function=None, dist2=0, speed2=0):
    print(f"Starting heading: {hub.imu.heading()}")
    
    drb.settings(straight_speed=speed, straight_acceleration=acceleration, 
                turn_rate=100, turn_acceleration=acceleration)
    
    drb.curve(radius, angle, wait=False)
    
    if second_function:
        second_function(dist2, speed2)
    
    while not drb.done():
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1000)
            raise StopRun("ENDE GELÄNDE!")
        
        wait(10)
def run1(): 
    watch = StopWatch()
    try:
        drb_m(100,600)
        drb_k(100,-60,200)
        drb_m(400,500)
        drb_k(300,-62,900)
        drb_k(87,83,500)
        rmkmove(800,900)
        lmkmove(200, 800)
        drb_m(-65,500)
        rmkmove(800,-900)
        drb_m(-25, 1000)
        drb_k(-40,-62,900)
        drb_k(270,120,500)
        drb_m(435,900)
        drb_k(90,-95,500)


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("2","3","4","5","6","7","8","9","0","1"))

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

    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("3","4","5","6","7","8","9","0","1","2"))

def run3():
    try:
        drb_m(590,400)
        rmkmove(1000,500)
        drb_m(-590,400)
    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","9","0","1","2","3"))


def run4():
    watch = StopWatch()
    try:
        drb_m(80,500)
        drb_t(-70,500)
        drb_k(650,27,500)
        drb_m(210,500)
        rmkmove(450,500)
        drb_m(-180, 500)
        drb_k(500,-6,500)
        rmkmove(360,-500)
        lmkmove(380, -500)
        drb_k(-400,20,600)
        drb_k(-1800,13,600)
        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
        

    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("5","6","7","8","9","0","1","2","3","4"))

def run5():
    watch = StopWatch()
    try:
        
        drb_m(220, 800)
        drb_t(-90, 500)
        drb_m(650, 600)
        drb_t(-90, 400)
        drb_m(230, 300)
        drb_t(-10,200)
        lmkmove(1100,900)
        drb_t(10,200)
        drb_m(20,300)
        drb_m(-100,300)
        drb_t(133, 300)
        rmkmove(620, 900)
        drb_m(320, 400)
        rmkmove(90, -400)
        drb_t(20, 300)
        rmkmove(290, -400)
        drb_k(-120, 75, -300)
        drb_m(800, 600)
        #zurückfaheren
        drb_m(-700, 900)
        drb_t(30, 600)
        drb_m(-850, 900)  
        drb_t(77, 600)
        drb_m(-240, 900)
        rmkmove(350, -900)

             

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("6","7","8","9","0","1","2","3","4","5"))

def run6():
    watch = StopWatch()
    try:
        drb_m(750, 500)
        drb_t(30, 500)
        drb_m(170, 400)
        drb_k(90, 60, 500)
        drb_m(130, 500)
        lmkmove(33,-400)
        rmkmove(200,500)
        rmkmove(190,-900)
        drb_m(-170,300)
        lmkmove(7,-900)
        drb_t(100,500)
        drb_m(800,1000)  


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")

    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("7","8","9","0","1","2","3","4","5","6"))

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
        lmkmove(400, 800)#dreizack runter
        lmkmove(250, -900)
        rmkmove(100, 900)       
        drb_m(-630, 1000)
        drb.stop()
        lmk.brake()
        rmk.brake()


        drb.stop()
        lmk.brake()
        rmk.brake()
    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("8","9","0","1","2","3","4","5","6","7"))


def run8():
    watch = StopWatch()
    try:

        drb_m(470, 900)
        rmkmove(120, 800)
        drb_m(30, 900)
        drb_m(-500, 900)
        drb.stop()
       
        drb.stop()
        lmk.brake()
        rmk.brake()
    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9","0"))

def run9():
    watch = StopWatch()
    try:
        drb_m(470, 900)
        rmkmove(120, 800)
        drb_m(30, 900)
        drb_m(-500, 900)
        drb.stop()
        drb.stop()
        lmk.brake()
        rmk.brake()
    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    global var
    var = int(hub_menu("0","1","2","3","4","5","6","7","8","9"))

def run0():
    watch = StopWatch()
    try:
        for _ in range(3):
            drb_m(800, 900)
            drb_t(90,500)
            drb_m(800, 900)
            drb_t(90,500)
            drb_m(500, 900)
            drb_t(90,500)
            drb_m(800, 900)
            drb_t(90,500)
            drb_m(-300, 900)

        drb.stop()
        drb.stop()
        lmk.brake()
        rmk.brake()
    except StopRun as e:
        if getattr(e, 'message', ''):
            print("This was a stop!", e.message)
        else:
            print("This was a stop!")
        if 'watch' in locals():
            try:
                elapsed_time = watch.time()
                elapsed_seconds = elapsed_time / 1000
                print("Verbrauchte Zeit:", elapsed_seconds, "Sekunden")
            except Exception:
                pass
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9","0"))
    
try:
    var = int(hub_menu("1","2","3","4","5","6","7","8","9","0"))
except Exception:
    var = 1

while True:
    try:
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
        elif var == 0:
            print("run0")
            run0()
    except StopRun as e:
        # If a caller explicitly requested stopping the whole program, exit.
        if getattr(e, 'stop_program', False):
            if getattr(e, 'message', ''):
                print("Stopping program:", e.message)
            else:
                print("Stopping program")
            break

        # Otherwise, only stop the current run and return to the menu.
        if getattr(e, 'message', ''):
            print("Run stopped:", e.message)
        else:
            print("Run stopped")
        drb.stop()
        lmk.brake()
        rmk.brake()
    wait(100)
    