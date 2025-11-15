try:
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
except OSError:
    # Running on host (modulefinder/pybricksdev compile) where hardware isn't available.
    # Provide lightweight stubs so the file can be imported for compilation and so
    # calls like `Button.BLUETOOTH in hub.buttons.pressed()` behave sensibly.
    class _Dummy:
        def __getattr__(self, name):
            def _method(*a, **k):
                return None
            return _method

    class _DummyMotor(_Dummy):
        def __init__(self, *a, **k):
            self._angle = 0
        def reset_angle(self, a=0):
            self._angle = a
        def angle(self):
            return self._angle
        def run(self, speed):
            pass
        def brake(self):
            pass

    class _DummyDriveBase:
        def __init__(self, *a, **k):
            pass
        def use_gyro(self, v):
            pass
        def settings(self, *a, **k):
            pass
        def straight(self, *a, **k):
            pass
        def turn(self, *a, **k):
            pass
        def curve(self, *a, **k):
            pass
        def done(self):
            return True
        def stop(self):
            pass

    class _DummyButtons:
        def pressed(self):
            # No buttons pressed on host
            return []

    class _DummyBattery:
        def voltage(self):
            # Return a reasonable default voltage (Volts or millivolts depending on usage)
            try:
                return 7.0
            except Exception:
                return 7000

    class _DummyIMU:
        def heading(self):
            return 0

    class _DummyDisplay:
        def number(self, v):
            print(f"[display] {v}")

    class _DummyHub:
        def __init__(self):
            self.system = _Dummy()
            self.buttons = _DummyButtons()
            self.battery = _DummyBattery()
            self.imu = _DummyIMU()
            self.display = _DummyDisplay()

    class _ButtonConsts:
        BLUETOOTH = 'BLUETOOTH'
        CENTER = 'CENTER'

    class _StopConsts:
        HOLD = 'HOLD'

    class _DirectionConsts:
        COUNTERCLOCKWISE = 'CCW'

    class _PortConsts:
        C = 'C'
        D = 'D'
        F = 'F'
        B = 'B'

    Button = _ButtonConsts()
    Stop = _StopConsts()
    Direction = _DirectionConsts()
    Port = _PortConsts()

    hub = _DummyHub()
    lmg = _DummyMotor()
    rmg = _DummyMotor()
    lmk = _DummyMotor()
    rmk = _DummyMotor()
    radius = 31.2
    drb = _DummyDriveBase()

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