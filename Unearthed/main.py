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

#Firebase startinfos
print("restart")
print("battery",hub.battery.voltage() / 1000)

def lmkmove(distance, speed):
    lmk.reset_angle(0)
    while abs(lmk.angle()) < distance:
        if Button.BLUETOOTH in hub.buttons.pressed():
            lmk.brake()
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            lmk.brake()
            wait(1)
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
            wait(1)
            raise StopRun("ENDE GELÄNDE!")
        rmk.run(speed)
    rmk.brake()

def drb_m(distance,speed,acceleration=900,second_function = None,dist2=0,speed2=0):
    drb.settings(speed,acceleration,90, 500)
    drb.straight(distance,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")

def drb_t(angle,speed,acceleration=500,second_function = None,dist2=0,speed2=0):
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
    
    drb.settings(straight_speed=speed, straight_acceleration=acceleration, 
                turn_rate=100, turn_acceleration=acceleration)
    
    drb.curve(radius, angle, wait=False)
    
    if second_function:
        second_function(dist2, speed2)
    
    while not drb.done():
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")
        
        wait(10)

def drb_m_rmk(distance, speed, rmk_angle, rmk_speed):
    drb.settings(speed, 900, 90, 500)
    drb.straight(distance, Stop.HOLD, False)
    
    rmk.reset_angle(0)
    
    while not drb.done():
        if abs(rmk.angle()) < rmk_angle:
            rmk.run(rmk_speed)
        
        if Button.RIGHT in hub.buttons.pressed():
            rmk.brake()
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            rmk.brake()
            wait(1)
            raise StopRun("ENDE GELÄNDE!")
    
    rmk.brake()
def run1(): 
    watch = StopWatch()
    try:
        drb_m(100,600)
        drb_k(100,-60,200)
        drb_m(390,500)
        drb_k(280,-62,900)
        drb_m(34,500)
        drb_k(87,87,500)
        drb_m(-10,500)
        drb_m(30,500)
        rmkmove(800,900)
        lmkmove(200, 800)
        drb_m(-70,500)
        rmkmove(800,-900)
        drb_k(-40,-62,900)
        drb_k(270,120,500)
        drb_m(380,900)
        drb_k(90,-95,500)



        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000

    except StopRun as e:
        print("run1 stop!")
    else:
        print("run1 finish,", elapsed_seconds)  
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("2","3","4","5","6","7","8","9","0","1"))

def run2():
    watch = StopWatch()
    try:
        drb_k(2430, -15, 500)
        drb_t(55, 600)
        drb_m_rmk(130,600,150,400)
        drb_m(210,600)
        lmkmove(170,800)
        rmkmove(200,-600)
        wait(500)
        drb_m(-130,500)
        drb_t(-40,500)
        drb_m(-300,500)
        drb_k(-250,75,800)
       


        drb.stop()
        
        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000

    except StopRun as e:
        print("run2 stop!")
    else:
        print("run2 finish,", elapsed_seconds)
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("3","4","5","6","7","8","9","0","1","2"))

def run3():
    watch = StopWatch()
    try:

        drb_m(150, 800)
        drb_t(-90, 700)
        drb_m(165, 800)
        drb_t(45, 700)
        drb_m(330, 800)
        rmkmove(380, 800)
        wait(200)
        lmkmove(110, -1000)
        lmkmove(110, 1000)
        drb_m_rmk(-170, 1000, 500, -250)
        drb_m(40, 800)
        rmkmove(200, -900)
        drb_k(-700, 40, 900)
        lmkmove(150, -1000)

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000

    except StopRun as e:
        print("run3 stop!")
    else:
        print("run3 finish,", elapsed_seconds)
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("4","5","6","7","8","9","0","1","2","3"))


def run4():
    watch = StopWatch()
    try:
        drb_m(420,400)
        rmkmove(70,-800)
        rmkmove(70,800)
        rmkmove(70,-800)
        rmkmove(70,800)
        rmkmove(70,-800)
        rmkmove(70,800)
        print("A:08")#firebase
        drb_m(-590,400)


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        
    except StopRun as e:
        print("run4 stop!")
    else:
        print("run4 finish,", elapsed_seconds)
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
        drb_m(660, 600)
        drb_t(-90, 400)
        drb_m(230, 300)
        drb_t(-15,200)
        lmkmove(1100,900)
        print("A:11")#firebase
        drb_t(15,200)
        drb_m(20,300)
        drb_m(-100,300)
        drb_t(133, 300)
        rmkmove(620, 900)
        drb_m(320, 400)
        rmkmove(150, -400)
        drb_t(20, 300)
        rmkmove(230, -400)
        print("A:13")#firebase
        drb_k(-120, 75, -300)
        drb_m(800, 600)


             

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
    except StopRun as e:
        print("run5 stop!")
    else:
        print("run5 finish,", elapsed_seconds)
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("6","7","8","9","0","1","2","3","4","5"))

def run6():
    watch = StopWatch()
    try:
        drb_m(735, 500)
        drb_t(30, 500)
        drb_m(170, 400)
        drb_k(90, 60, 500)
        drb_m(130, 500)
        lmkmove(33,-400)
        rmkmove(200,500)
        rmkmove(190,-900)
        print("A:04")#firebase
        drb_m(-170,300)
        print("A:03,1")#firebase
        lmkmove(7,-900)
        drb_t(100,500)
        drb_m(800,1000)  


        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000

    except StopRun as e:
        print("run6 stop!")
    else:
        print("run6 finish,", elapsed_seconds)
    drb.stop()
    lmk.brake()
    rmk.brake()
    global var
    var = int(hub_menu("7","8","9","0","1","2","3","4","5","6"))

def run7():
    watch = StopWatch()
    try:



        drb_m(460, 900)
        rmkmove(120, 800)
        drb_m(40, 900)
        print("A:12")#firebase
        print("A:15,3")#firebase
        drb_m(-200, 900)
        drb_k(-300, -60, 700)
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000

    except StopRun as e:
        print("run7 stop!")
    else:
        print("run7 finish,", elapsed_seconds)
    drb.stop()
    global var
    var = int(hub_menu("8","9","0","1","2","3","4","5","6","7"))


def run8():
    watch = StopWatch()
    try:


        drb_m(760, 800)
        drb_t(-42, 500)
        drb_m(180, 300)
        lmkmove(100, 600)
        print("A:02")#firebase
        drb_m(-110, 500)
        drb_t(42, 300)
        drb_m(-130, 150)
        rmkmove(50, 700)#Landkarte hoch
        drb_m(-35, 150)
        wait(500)
        lmkmove(400, 800)#dreizack runter
        lmkmove(250, -900)
        rmkmove(100, 900)  
        print("A:01")#firebase     
        print("A:15,2")#firebase
        drb_m(-630, 1000)

       
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
        
    except StopRun as e:
        print("run8 stop!")
    else:
        print("run8 finish,", elapsed_seconds)
    drb.stop()
    global var
    var = int(hub_menu("9","0","1","2","3","4","5","6","7","8",))

def run9():
    watch = StopWatch()
    try:
        drb_m(100, 1000)
        drb_k(250, 50, 700)
        drb_m(200, 900)
        print("A:14")#firebase
        drb_m(-300, 900)
        drb.stop()
        drb.stop()
        lmk.brake()
        rmk.brake()

        elapsed_time = watch.time()
        elapsed_seconds = elapsed_time / 1000
    except StopRun as e:
        print("run9 stop!")
    else:
        print("run9 finish,", elapsed_seconds)
    drb.stop()
    global var
    var = int(hub_menu("0","1","2","3","4","5","6","7","8","9"))

def run0():
    watch = StopWatch()
    try:
        print("restart")#firebase
        
        drb.stop()
        drb.stop()
        lmk.brake()
        rmk.brake()

    except StopRun as e:
        print("")
            
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
            print("run1 start")
            run1()
        elif var == 2:
            print("run2 start")
            run2()
        elif var == 3:
            print("run3 start")
            run3()
        elif var == 4:
            print("run4 start")
            run4()
        elif var == 5:
            print("run5 start")
            run5()
        elif var == 6:
            print("run6 start")
            run6()
        elif var == 7:
            print("run7 start")
            run7()
        elif var == 8:
            print("run8 start")
            run8()
        elif var == 9:
            print("run9 start")
            run9()
        elif var == 0:
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
    