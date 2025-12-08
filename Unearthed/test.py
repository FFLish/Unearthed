from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
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

# Motor und Sensor Initialisierung
lmg = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
rmg = Motor(Port.D)
lmk = Motor(Port.F)
rmk = Motor(Port.B)
radius = 31.2
drb = DriveBase(lmg, rmg, 62.4, 158)

# Verbesserte Menü-Funktion
def show_menu():
    """Zeigt das Hauptmenü mit besserer Reaktionszeit"""
    hub.display.off()
    wait(200)
    hub.display.on()
    
    try:
        selection = hub_menu(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        return selection + 1  # hub_menu gibt 0-9 zurück, wir wollen 1-10
    except:
        return 1  # Fallback auf Run 1 bei Fehlern

# Deine bestehenden Funktionen (lmkmove, rmkmove, drb_m, drb_t, drb_k) bleiben gleich
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

# Deine Run-Funktionen (run1 bis Run10) bleiben gleich, aber OHNE die hub_menu Aufrufe am Ende
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
    finally:
        drb.stop()
        lmk.brake()
        rmk.brake()

# run2 bis Run10 ähnlich anpassen - entferne die hub_menu Aufrufe am Ende jeder Funktion
# und ersetze sie durch ein einfaches return

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
    finally:
        drb.stop()
        lmk.brake()
        rmk.brake()

# Füge ähnliche finally-Blöcke für run3 bis Run10 hinzu...

# Hauptprogramm mit verbessertem Menü
while True:
    try:
        # Menü anzeigen
        hub.display.text("MENUE")
        wait(500)
        
        selection = show_menu()
        print("Auswahl:", selection)
        
        # Run basierend auf Auswahl ausführen
        run_functions = {
            1: run1,
            2: run2,
            3: run3,
            4: run4,
            5: run5,
            6: run6,
            7: run7,
            8: run8,
            9: Run9,
            10: Run10
        }
        
        if selection in run_functions:
            print(f"Starte Run {selection}")
            run_functions[selection]()
        else:
            print("Ungueltige Auswahl")
            
        # Kurze Pause vor naechstem Menü
        wait(1000)
        
    except StopRun as e:
        if getattr(e, 'stop_program', False):
            print("Programm gestoppt:", e.message)
            break
            
        print("Run abgebrochen:", e.message)
        drb.stop()
        lmk.brake()
        rmk.brake()
        wait(1000)
        
    except Exception as e:
        print("Fehler:", str(e))
        drb.stop()
        lmk.brake()
        rmk.brake()
        wait(1000)