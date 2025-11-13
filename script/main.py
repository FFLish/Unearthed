from pybricks.tools import wait, StopWatch, hub_menu
from blocks import (
    hub,
    drb,
    lmk,
    rmk,
    drb_m,
    drb_t,
    drb_k,
    lmkmove,
    rmkmove
)

def run1(): 
    watch = StopWatch()
    try:
        drb_m(705, 350)
        drb_t(-45, 300)
        drb_m(100, 300)
        drb_t(-45, 300)
        drb_m(450, 300)
        drb_t(90, 300)
        drb_m(190, 150)
        rmkmove(375, -300)
        drb_m(50, 150)
        rmkmove(450, 300)
        drb_m(-130, 300)
        lmkmove(260, 200)
        drb_m(-100, 300)
        drb_t(-90, 300)
        drb_m(-200, 300)
        drb_t(45, 300)
        drb_m(-200, 200) #Aktuelle Angebote hochheben
        drb_m(100,300)
        drb_t(130,300)
        drb_m(100,300)
        drb_t(70,300)
        drb_m(200,300)
        drb_t(30,300)
        drb_m(500,400)

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
        print("hallo")
        drb_m(320,900)
        drb_t(90,700)
        drb_m(530,500)
        drb_t(45,300)
        drb_m(210,500)
        drb_t(-5,500)
        wait(500)
        lmkmove(150,700)
        rmkmove(250,600)
        wait(500)
        rmkmove(370,-300)
        drb_m(-30,700)
        drb_t(30,500)
        drb_m(-140,700)
        drb_t(90,500)
        drb_m(210,800)
        drb_t(65,500)
        drb_m(270,500)
        drb_k(110,-120,500)
        drb_m(400,600)

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
    var = int(hub_menu("4","5","6","7","8","9","1","2","3"))

def run4():
    watch = StopWatch()
    try:

        drb_m(5, 500)
        drb_t(-45, 400)
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
    global var
    var = int(hub_menu("6","7","8","9","1","2","3","4","5"))

def run6():
    watch = StopWatch()
    try:
        

        drb_m(800, 800)
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
    var = int(hub_menu("8","9","1","2","3","4","5","6","7"))

def run8():
    watch = StopWatch()
    try:
        drb_m(540, 1000)
        wait(500)
        drb_m(-270, 1000)


       
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


 '''     drb_m(-260, 400)
        drb_t(-210,300)
        rmkmove(650, -1000)
        drb_m(120, 400)
        rmkmove(260, 400) 
        drb_t(20, 400)

        drb_m(-150, 400) 
        rmkmove(450, 400)
        drb_t(140, 400)
        drb_m(150, 300)
        drb_t(90, 300)
        drb_m(-190, 100)
        drb_m(140,270)
        
        drb_t(90,300)
        drb_m(300,400)
        drb_t(-15, 400)
        drb_m(700, 1000)       
        drb_m(870, 500)
        drb_t(-90, 300)
        drb_m(170, 500)
        drb_t(-20, 300)
        lmkmove(850, 1000)    

'''       