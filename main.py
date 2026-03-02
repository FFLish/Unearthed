from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
import math as m
from pybricks.tools import multitask, run_task
from pybricks.hubs import PrimeHub

hub = PrimeHub()

hub.system.set_stop_button({Button.BLUETOOTH})


session_watch = None  # StopWatch für die gesamte Session
session_start_time = None  # Startzeit in Millisekunden

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

def drb_m(distance,speed,acceleration=900):
    drb.settings(speed,acceleration,90, 500)
    drb.straight(distance,Stop.HOLD,True)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")

def drb_t(angle,speed,acceleration=500):
    drb.settings(400,400,speed,acceleration)
    drb.turn(angle,Stop.HOLD,True)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise StopRun("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1)
            raise StopRun("ENDE GELÄNDE!")

def drb_k(radius, angle, speed, acceleration=500):

    drb.settings(straight_speed=speed, straight_acceleration=acceleration, turn_rate=100, turn_acceleration=acceleration)
    drb.curve(radius, angle, wait=False)
    
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(100,600)
        drb_k(100,-60,200)
        drb_m(390,500)
        drb_k(280,-62,900)
        drb_m(34,500)
        drb_k(87,87,500)
        drb_m(40,500)
        rmkmove(780,900)#Lore klauen
        lmkmove(200, 800)#Flagge aufstellen
        print("A:03")#firebase
        drb_m(-70,500)
        rmkmove(800,-900)
        drb_k(-40,-62,900)
        drb_k(270,120,500)
        drb_m(380,900)
        drb_k(130,-95,500)
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(90,500)
        drb_k(800, -35, 500)
        drb_m(112,500)
        drb_t(82, 600)
        drb_m_rmk(150,700,140,250)
        drb_m(210,600)
        lmkmove(170,900)#Schmiede 
        rmkmove(140,-300)#Schweres Heben
        print("A:06")#firebase
        print("A:07")#firebase
        wait(500)
        drb_m(-160,500)
        drb_t(-40,500)#Landkarte Hoch
        print("A:05")#firebase
        drb_m_rmk(-300,500,100,-80)
        drb_k(-250,95,800)
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(150, 810)
        drb_t(-90, 700)
        drb_m(165, 800)
        drb_t(45, 700)
        drb_m(330, 800)
        rmkmove(400, 900)#Aktuelle Angebote hochheben
        print("A:09")#firebase
        drb_m(-10, 500)
        wait(200)
        lmkmove(110, -500)
        lmkmove(120, 500)
        drb_m_rmk(-170, 1000, 500, -250)
        print("A:04")#firebase
        drb_m(40, 800)
        rmkmove(200, -900)
        drb_k(-700, 40, 900)
        
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(420,400)
        rmkmove(70,-800)#Mehr runter damit er beim hochgehen nicht immer dagegenhaut
        rmkmove(50,800)
        wait(300)
        rmkmove(50,-800)
        rmkmove(50,800)
        wait(100)
        rmkmove(50,-800)
        rmkmove(40,-800)
        print("A:08")#firebase
        drb_k(-1000, -20, 800)

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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(210, 800)
        drb_t(-90, 500)
        drb_m(655, 600)
        drb_t(-90, 400)
        drb_m(110, 300)
        drb_t(-15,200)
        lmkmove(1100,900)#Anglerartefakt
        print("A:11")#firebase
        drb_t(15,200)
        drb_m(20,300)
        drb_m(-100,300)
        drb_t(129, 300)
        rmkmove(620, 900)
        drb_m(318, 400)
        rmkmove(150, -400)
        drb_t(35, 300)
        rmkmove(220, -400)#Statue rekpnstruieren
        print("A:13")#firebase
        drb_k(-100, 85, -300)
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_k(3300, 15, 700)
        drb_t(165, 700)
        drb_m(-125, 700)
        drb_m(58, 700)#hier am wettbewerb ändern
        drb_t(-90, 500)
        drb_m(140, 500)
        drb_m(50, 200)
        lmkmove(55,-400)
        rmkmove(250,800)#vorsichtige Bergungsaktion^
        wait(200)
        print("A:04")#firebase
        drb_m_rmk(-170,300, 100, 400)#Lore rüberschieben
        print("A:03,1")#firebas
        lmkmove(7,-900)
        drb_t(100,500)
        drb_m(760,1000)

        '''
        drb_m(734, 500)
        drb_t(30, 500)
        drb_m(170, 400)
        drb_k(90, 60, 500)
        drb_m(130, 300)
        lmkmove(45,-400)
        rmkmove(220,800)#vorsichtige Bergungsaktion^
        wait(200)
        print("A:04")#firebase
        drb_m_rmk(-170,300, 100, 400)#Lore rüberschieben
        print("A:03,1")#firebas
        lmkmove(7,-900)
        drb_t(100,500)
        drb_m(760,1000)  '''


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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(500, 700)
        wait(350)
        rmkmove(150, -800)#Bergungsaktion und dritte Flage abstellen
        print("A:12")#firebase
        print("A:15,3")#firebase
        drb_m(-200, 800)
        drb_k(-350, -45, 900)
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
        lmg.reset_angle(0)
        rmg.reset_angle(0)
        drb_m(770, 800)
        drb_t(-42, 500)
        drb_m(180, 300) #Landkarten enthüllen
        print("A:2,1")
        print("A:2,2")
        lmkmove(100, 600)#Mutterboden hochheben
        print("A:2,3")
        drb_m(-110, 500)
        drb_t(42, 300)
        drb_m(-55, 350)
        rmkmove(100, -700)#Flagge abwerfen
        print("A:15,2")
        drb_m(-115, 150)
        wait(500)
        lmkmove(430, 800)#Pinsel Gefangen
        print("A:1")#firebase
        lmkmove(400, -600)  
        drb_k(-1400, -20, 800)
       
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
        drb_k(110, 90, 600)
        drb_m(140, 1000) 
        drb_k(110, -75, 600) 
        drb_m(60, 900)#alles rein
        rmkmove(600, -500)
        wait(500)
        print("A:14")#firebase
        drb_m(-250, 900)
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
        
        # BERECHNE GESAMTZEIT DER 2:30 SESSION
        global session_watch, session_start_time
        if session_watch is not None:
            total_session_time = session_watch.time()  # Zeit in Millisekunden
            total_session_seconds = total_session_time // 1000  # Zeit in Sekunden
            
            # Hier wird die Gesamtzeit mit ausgegeben
            print("2_30 finish,", total_session_seconds)
        else:
            print("2_30 finish")  
            
        # Session beenden
        session_watch = None
        session_start_time = None
        
    drb.stop()
    global var
    var = int(hub_menu("0","1","2","3","4","5","6","7","8","9"))

def run0():
    try:
        drb_k(900, -50, 500)
        drb_m(100, 500)
        drb_t(-40, 500)
        drb_m(255, 500)
        drb_t(90, 500)
        drb_m(200, 1000)
        rmkmove(320, -310)#ayyana klauen
        wait(500)
        drb_m(-80, 1000)
        rmkmove(170, 200)
        rmkmove(150, 150)
        drb_m(-80, 1000)
        wait(500)
        drb_t(180, 100)
        drb_m(-20, 500)
        lmkmove(200, -800)  #Flagge aufstellen - Ändern!
        drb_m(50, 500)
        drb_t(-90, 100)
        drb_m(275, 500)
        drb_t(55,100)
        drb_m(750, 500)
        print("restart")#firebase
        print("battery",hub.battery.voltage() / 1000)
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
            print("2_30 start")
            print("run1 start")
            session_watch = StopWatch()  
            session_start_time = session_watch.time()         
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
            print("battery",hub.battery.voltage() / 1000)
            run9()
        elif var == 0:
            run0()
    except StopRun as e:
        if getattr(e, 'stop_program', False):
            if getattr(e, 'message', ''):
                print("Stopping program:", e.message)
            else:
                print("Stopping program")
            
            if session_watch is not None:
                total_time = session_watch.time()
                print("2_30 stop!,", total_time / 1000)
                session_watch = None
            
            break
        if getattr(e, 'message', ''):
            print("Run stopped:", e.message)
        else:
            print("Run stopped")
            
        if session_watch is not None:
            total_time = session_watch.time()
            print("run stop!,", total_time / 1000)
            
        drb.stop()
        lmk.brake()
        rmk.brake()
    wait(100)