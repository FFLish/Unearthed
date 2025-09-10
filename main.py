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

# -----------------------
# RUN FUNCTIONS
# -----------------------

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
        drb_k(-90, -15, 150,rmkmove, 1600, 1200)
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
        drb_m(320,300)
        drb_t(90,400)
        drb_m(530,300)
        drb_t(45,300)
        drb_m(210,150)
        drb_t(-5,200)
        wait(500)
        lmkmove(150,700)
        rmkmove(250,300)
        wait(500)
        rmkmove(270,-300)
        drb_m(-30,200)
        drb_t(47,100)
        drb_m(-150,200)
        drb_m(50,200)
        drb_t(90,100)
        drb_m(270,200)
        drb_t(45,100)
        drb_m(200,200)
        drb_k(8,-110,200)
        drb_m(400,300)

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
    try:
        drb_m(430,300)
        lmkmove(220,-400)
        wait(200)
        lmkmove(220,200)
        lmkmove(220,-400)
        wait(200)
        lmkmove(220,200)
        lmkmove(220,-400)
        lmkmove(220,200)
        drb_m(-430,300)
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
        drb_m(185, 300)
        drb_t(-90, 300)
        drb_m(720, 500)
        drb_t(-90, 300)
        drb_m(170, 500)
        drb_t(-20, 300)
        lmkmove(850, 1000)    

        drb_m(-260, 400)
        drb_t(-210,300)
        rmkmove(650, -1000)
        drb_m(120, 400)
        rmkmove(260, 400) 
        drb_t(20, 400)

        drb_m(-150, 400) 
        rmkmove(450, 400)
        drb_t(130, 400)
        drb_m(150, 300)
        drb_t(85, 300)
        drb_m(-190, 100)
        drb_m(140,270)
        
        drb_t(90,300)
        drb_m(300,400)
        drb_t(-15, 400)
        drb_m(700, 1000)

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
        drb_m(800, 600)
        drb_t(-42, 300)
        drb_m(180, 200)
        lmkmove(100, 600)
        drb_m(-110, 500)
        drb_t(42, 300)
        drb_m(-160, 150)
        lmkmove(280, 700)
        wait(1200)
        lmkmove(180, -600)
        drb_m(-540, 600)
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
        #batterie= hub.battery.voltage
        #print(batterie)
        warn_threshold = 20  # Warnung ab 20%

# Werte für Batterie-Prozent-Berechnung
        max_voltage = 7.2
        min_voltage = 6.0

        while True:
    # Spannung abfragen
            voltage = hub.battery.voltage()
    
    # Batterieschätzung in Prozent
            battery_percent = max(0, min(100, (voltage - min_voltage) / (max_voltage - min_voltage) * 100))
            print(battery_percent)
            wait(1000)
        '''voltage = hub.battery.voltage()
        percent = int((voltage - 6000) / (8400 - 6000) * 100)
        percent = max(0, min(100, percent))
        hub.display.number(percent)
        print("Batterie :", percent, "%")

      
        #drb_m(100 0, 1000)  
        
        while True:

            voltage = hub.battery.voltage()
            percent = int((voltage - 6000) / (8400 - 6000) * 100)
            percent = max(0, min(100, percent))
            hub.display.number(percent)
            
        '''
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.CENTER in hub.buttons.pressed():
            wait(1000)
            raise SystemExit("ENDE GELÄNDE!")
                
            wait(100)

    except SystemExit:
        print("This was a stop!")
    finally:
        drb.stop()
        lmk.brake()
        rmk.brake()

    
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