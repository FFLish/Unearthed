from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
import umath as m
from pybricks.tools import multitask, run_task

hub = PrimeHub()

# Définition des chiffres en matrices 5x5
digits = {
    "1": [
        [0,1,1,0,0],
        [1,1,1,0,0],
        [0,1,1,0,0],
        [0,1,1,0,0],
        [1,1,1,1,1],
    ],
    "2": [
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    "3": [
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,1,1,1,0],
        [0,0,0,0,1],
        [1,1,1,1,0],
    ],
    "4": [
        [1,0,0,1,0],
        [1,0,0,1,0],
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,0,1,0],
    ],
    "5": [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,0,1],
        [1,1,1,1,0],
    ],
    "6": [
        [0,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    "7": [
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,1,0,0],
        [0,1,0,0,0],
        [1,0,0,0,0],
    ],
    "8": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    "9": [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,1],
        [0,0,0,0,1],
        [0,1,1,1,0],
    ],
}
def show_digit(digit):
    # Affiche le chiffre personnalisé sur l'écran du hub
    d = str(digit)
    if d in digits:
        hub.display.image(digits[d])
    else:
        hub.display.number(digit)

lmA=Motor(Port.E, positive_direction=Direction.COUNTERCLOCKWISE)
rmB=Motor(Port.D)
lmk=Motor(Port.F)
rmk=Motor(Port.B)
radius = 2.8
drb = DriveBase(lmA, rmB, 56, 132)
strecke = (m.radians(lmA.angle())*radius+m.radians(rmB.angle())*radius)/2
alteStrecke = strecke
x = 0
y = 0
var = 0
drb.use_gyro(True)


def updatePosition():
    global alteStrecke, x, y
    strecke = (m.radians(lmA.angle())*radius+m.radians(rmB.angle())*radius)/2
    sdStrecke = strecke - alteStrecke
    richtung = m.radians(hub.imu.heading())
    deltaX = m.cos(richtung) * sdStrecke
    deltaY = m.sin(richtung) * sdStrecke
    x += deltaX
    y += deltaY
    #print("x:", x, "   y:", y)
    alteStrecke = strecke


def drive(xnewpos,ynewpos,speed,speed2=100):
    global x
    global y
    acceleration=10
    turnspeed = speed*3/4
    ankathete = xnewpos-x
    gegenkathete = ynewpos-y
    #zufahrenstrecke = m.sqrt(x*x+y*y)#(x**2+y**2)
    zufahrenstrecke = m.sqrt(ankathete**2+gegenkathete**2)
#    print(zufahrenstrecke)
    while zufahrenstrecke>0.7:
        if abs(speed2)/50>zufahrenstrecke:
            speed2 = zufahrenstrecke*50*speed2/abs(speed2)
        elif speed2<speed:
            speed2 = speed2+acceleration
        elif speed2>speed:
            speed2=speed-acceleration
        updatePosition()
        ankathete = xnewpos-x
        gegenkathete = ynewpos-y
        winkel = m.atan(gegenkathete/ankathete)
        print("x:", round(x, 2), " y:", round(y, 2), "winkel",winkel,"ankathete",ankathete,"gegenkathete",gegenkathete,"zufahrenstrecke ",zufahrenstrecke)
        zufahrenstrecke = m.sqrt(ankathete**2+gegenkathete**2)
        if ankathete/abs(ankathete)==-1:# and gegenkathete/abs(gegenkathete)==-1:
            lmA.run(speed2-(winkel+m.pi-m.radians(hub.imu.heading()))*-turnspeed)
            rmB.run(speed2+(winkel+m.pi-m.radians(hub.imu.heading()))*-turnspeed)
#            turndrive = (winkel+m.pi-m.radians(hub.imu.heading())*-turnspeed)*20
#            drivebase.drive(speed,turndrive)
            
        else:
            lmA.run(speed2-(winkel-m.radians(hub.imu.heading()))*-turnspeed)
            rmB.run(speed2+(winkel-m.radians(hub.imu.heading()))*-turnspeed)

#            turndrive = (winkel+m.pi-m.radians(hub.imu.heading())*-turnspeed)*-20
#            drivebase.drive(speed,turndrive)
#            while (!driveBase.done()):
#                updatePosition()

        print(speed-(winkel-m.radians(hub.imu.heading()))*-1000,speed+(winkel-m.radians(hub.imu.heading()))*-1000,winkel+m.pi-m.radians(hub.imu.heading())*-turnspeed, hub.imu.heading())
    lmA.brake()
    rmB.brake()

#drive(20,20,600)

def heading():
    if hub.imu.heading()>0:
        heading = abs(hub.imu.heading())%360
    else:
        heading = 360-(abs(hub.imu.heading())%360)
    return heading

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
'''rmkmove(450,500)
rmkmove(450,-500)'''
#wait(10000000)
def move(speed,acceleration, endbedingung, distance = 0,speed2=0,brake1 = True):
    weiterfahren = True
    lmA.reset_angle(0)
    rmB.reset_angle(0)
    gyrostart=hub.imu.heading()
    gyroende=hub.imu.heading()
    while weiterfahren:
        togo = distance-abs(lmA.angle())
        if abs(speed2)/5>togo and endbedingung == "distance":
            speed2 = togo*5*speed2/abs(speed2)
            print(speed2)
        elif speed2<speed:
            speed2 = speed2+acceleration
        elif speed2>speed:
            speed2 = speed2-acceleration           
        aditional = (rmB.angle())-(lmA.angle())
        gyro=gyrostart-hub.imu.heading()
        gyroextra=gyroende-hub.imu.heading()
        lmA.run(speed2*1+aditional*0+(gyro*3-gyroextra*1))    
        rmB.run(speed2*1-aditional*0-(gyro*3-gyroextra*1))
        print(gyro,gyroextra,aditional,speed2,rmB.angle(),lmA.angle(),speed2*1-aditional*0.5+(gyro*3-gyroextra*0),speed2*1-aditional*0.5-(gyro*3-gyroextra*0))
        gyroende=hub.imu.heading()
        if endbedingung == 2:
            weiterfahren = ls2.reflection() > 9
        elif endbedingung == 1:
            weiterfahren = distance > abs(lmA.angle())
    if brake1== True:
        lmA.hold()
        rmB.hold()

#move(1000,5,1,2000)
#wait(10000)
def turn(speed, angle):
    acceleration = 5
    speed2=100
    stopdis = 10
    while abs(heading()-angle)>1:
        updatePosition()
        if heading()-angle>180:
            if abs(speed2)/stopdis>360-(heading()+angle)%360:
                speed2 = (360-(heading()+angle)%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(speed2)
            rmB.run(-speed2)
        elif (heading()-angle)/(abs(heading()-angle))==-1:
            if abs(speed2)/stopdis>angle-heading():
                speed2 = ((abs(heading()-angle))%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(speed2)
            rmB.run(-speed2)
            print(heading()-angle)
        else:
            if abs(speed2)/stopdis>abs(angle-heading())%360:
                speed2 = (abs(angle-heading())%360)*stopdis
            elif speed2<speed:
                speed2 = speed2+acceleration
            lmA.run(-speed2)
            rmB.run(speed2)
    lmA.brake()
    rmB.brake()




def drivedis(speed,distance,speed2):
    global x
    global y
    acceleration=10
    turnspeed = 10
    winkel = 0
    ankathete = m.cos(hub.imu.heading())*distance
    gegenkathete = m.sin(hub.imu.heading())*distance
    drive(ankathete+x,gegenkathete+y,speed,speed2)


#drb.settings(200,700,150,700)

#drb.straight(100,Stop.HOLD,True)
def drb_m(distance,speed,acceleration=900,second_function = None,dist2=0,speed2=0):
    drb.settings(speed,acceleration,800,500)#max straight_speed=97(argument.1)
    drb.straight(distance,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise CompleteExit("ENDE GELÄNDE!")

def drb_t(angle,speed,acceleration=500,second_function = None,dist2=0,speed2=0):
    #drb.use_gyro(True)
    print(hub.imu.heading())
    drb.settings(400,400,speed,acceleration)
    drb.turn(angle,Stop.HOLD,False)
    if second_function:
        second_function(dist2,speed2)
    while not drb.done():
        if Button.RIGHT in hub.buttons.pressed():
            raise SystemExit("ENDE")
        if Button.BLUETOOTH in hub.buttons.pressed():
            raise CompleteExit("ENDE GELÄNDE!")

#drb.use_gyro(True)
'''print(drb.heading_control.pid()) #before: 21242, 0, 5310, 34, 63

drb.heading_control.pid(21242,0,5310,3) #before: 21242, 0, 5310, 34, 63
print(drb.heading_control.pid()) #before: 21242, 0, 5310, 34, 63
'''
'''rmkmove(600,300)
rmkmove(600,-300)'''
#START PROGRAMM
#1 Hochschieben
#drb.turn(-90)
#drb_t(90,800,500,lmkmove,500,50)
def run1():
    try:
        drb_m(500,500)
        drb_t(360,500)

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("4","5","6","7","8","9","10","1","2","3"))

'''def run4():
    try:
        drb_m(250,300,500)
        drb_t(-90,200,200)
        drb_m(-465,300,500)
        drb_t(-45,200,200)
        drb_m(-170,300,500)
        rmkmove(200,400)
        drb_m(170,300,500)
        drb_t(30,200,200)
        drb_m(700,900,1500)
        drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("5","6","7","8","9",10,"1","2","3","4"))
def run5():
    try:
        drb_m(570,400,500)
        drb_t(90,200,200)
        drb_m(200,200,500)
        drb_m(-200,500,500)
        drb_t(-70,300,200)
        drb_m(-700,900,1500)
        drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("6","7","8","9",10,"1","2","3","4","5"))
def run6():
    try:
       lmkmove(100,100)
       wait(500)
       drb_m(100,500)
       drb_m(500,900,900,lmkmove,100,-900)
       drb_m(-200,900)
       lmkmove(100,500)
       drb_m(200,900)
       drb_m(50,500)
       drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("7","8","9",10,"1","2","3","4","5","6"))
def run7():
    try:
       drb_m(-500,900)
       drb_t(-10,500)
       drb_m(-1000,900)
       drb_t(30,500)
       drb_m(-500,900)
       drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("8","9",10,"1","2","3","4","5","6","7"))

def run8():
    try:
      drb_m(200,300)
      drb_t(-90,300)
      drb_m(225,300)
      drb_t(135,200)
      drb_m(90,200)
      lmkmove(400,-500)#schiff umsetzen
      drb_m(-50,300)
      drb_t(135,-200)
      drb_m(-400,400)
      drb_t(44,-200)
      drb_m(-140,300)#Wal
      drb_m(190,300)
      drb_t(-50,200)
      drb_m(650,300)
      drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("9",10,"1","2","3","4","5","6","7","8"))


def run9():
    try:
      drb_m(-250,500) 
      drb_m(-70,100)#Korallen rausschieben       
      drb_m(280,500)        
      drb_t(-45,500)
      drb_m(-535,300)#gegen Krakenturm fahren
      drb_m(250,500)
      drb_t(-45,500)
      drb_m(-375,500)#fahren
      drb_t(67,500)  
      drb_m(-387,500)
      drb_t(-44,500)  
      drb_m(-165,500)#gegen Leuchfisch fahren 
      #drb_t(-10,500) 
      drb_m(100,500)
      drb_t(-43,500)
      drb_m(240,500)
      drb_t(108,500) 
      drb_m(-280,500) 
      drb_m(90,500)        
      lmkmove(270,300)#DRehen 
      lmkmove(50,-300)#Drehen zurück  
      drb_m(130,400) 
      drb_t(-45,400)
      rmkmove(1250,1000)#Gabelstabler runter
      drb_m(-180,400)
      drb_t(10,400)
      rmkmove(1250,-1000)#Gabelstabler hoch
      drb_t(-10,400)
      drb_m(150,400)
      drb_t(84 ,400)            
      drb_m(140,400)#ende 
      drb.stop()
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu(10,"1","2","3","4","5","6","7","8","9"))

def run10():
    try:
        drb_m(-50000,900,1500)
    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9",10))
def run11():
    try:

    except SystemExit:
        print("This was a stop!")
    drb.stop()
    global var
    var = int(hub_menu("1","2","3","4","5","6","7","8","9",10,11))'''

''' MAIN PROGRAM STARTS HERE'''
var = int(hub_menu("1","2","3","4","5","6","7","8","9",10,11))
print(var)
#if Button.CENTER in hub.buttons.pressed():
#while True
#    var = int(hub_menu("1","2","3","4","5","6","7","8","9"))
while True:
    #var = int(hub_menu("1","2","3","4","5","6","7","8","9"))
    #if hub.buttons.pressed() == [hub.BUTTON_CENTER]:
    #if hub.buttons.pressed():
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
    if var==10:
        print("run10")
        run10()
    if var==11:
        print("run11")
        run11()
#2Start (großer Aufsatz)



#3Krebse auf dem Boden
'''driveb_st(900,150)'''
#drb.use_gyro(True)
#driveb_st(300,200)
'''driveb_st(-600,300)
lmkmove(60,-80)
driveb_st(110,60,False)
lmkmove(150,-80)
wait(10000)
driveb_st(-800,300,True)'''
#driveb_st(-300,300)
#wait(1000)
#driveb_st(300,300)
#drb.settings(97,100,800,500)
#drb.turn(90,Stop.HOLD,True)
#drb.straight(100,Stop.HOLD,True)
#drb.straight(-100,Stop.HOLD,True)
#updatePosition()


#wait(300000000)
#drive(50,1,400)



#drive(0,0,400)
#turn(0)
print(x,y)
#while True:
#    print(hub.imu.heading())
#drivedis(500,20,50)
#drive(20,-20,600)
#drive(0,0,600)
#turn(0)

#main(10,30,300)
async def counter():
    a=1   
    while True:
        print(a)
        a=1

#async def run(xnewpos,ynewpos,speed):
#    await multitask(updatePosition(),counter())

#run_task(run(1,1,1))


#run_task(runn())
#main(10,10,500)#neu
#updatePosition()
#main(10,10,500)
#main(xnewpos,ynewpos,speed)
#Agml
#Bgmr
#Ckml
#Dkmr