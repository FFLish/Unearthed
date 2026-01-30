# bridge_firebase.py - KORRIGIERTE VERSION
import os
import time
from datetime import datetime
import glob
import re
import firebase_admin
from firebase_admin import credentials, db
import threading

# Firebase
SERVICE_ACCOUNT = "firebase-service-key.json"
FIREBASE_URL = "https://fll-scorer-55c47-default-rtdb.europe-west1.firebasedatabase.app"

# Timer Konfiguration
MAX_TIMER_VALUE = 150  # 2:30 in Sekunden
MIN_TIMER_VALUE = -120  # -2:00 in Sekunden
INITIAL_TIMER_VALUE = 149  # Startet bei 2:29

# Globale Timer-Variablen
timer_active = False
timer_seconds = INITIAL_TIMER_VALUE
timer_thread = None
last_timer_update = 0

# Init Firebase
def init_firebase():
    if not os.path.exists(SERVICE_ACCOUNT):
        print("❌ Service Account fehlt")
        return False
    
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT)
        firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_URL})
        print("✅ Firebase ready")
        return True
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return False

# Firebase functions
def firebase_set(path, value):
    try:
        db.reference(path).set(value)
        return True
    except:
        return False

def firebase_delete(path):
    try:
        db.reference(path).delete()
        return True
    except:
        return False

# Helper: Setzt active und time separat
def set_active(value):
    """Setzt nur active"""
    firebase_set("2_30/activ/active", value)
    print(f"📊 Active auf {value} gesetzt")

def set_time(value):
    """Setzt nur time"""
    firebase_set("2_30/activ/time", value)
    print(f"⏰ Time auf {value} gesetzt")

# Helper: Format Sekunden in MM:SS oder -MM:SS
def format_timer(seconds):
    """Formatiert Sekunden in MM:SS Format mit optionalem Minuszeichen"""
    sign = "-" if seconds < 0 else ""
    abs_seconds = abs(int(seconds))
    minutes = abs_seconds // 60
    secs = abs_seconds % 60
    return f"{sign}{minutes:01d}:{secs:02d}"

# Timer-Funktionen
def start_timer():
    """Startet den Countdown-Timer - SCHNELL & GENAU"""
    global timer_active, timer_seconds, timer_thread, last_timer_update
    
    if timer_active:
        return
    
    timer_active = True
    timer_seconds = INITIAL_TIMER_VALUE  # Start bei 2:29
    last_timer_update = time.time()
    
    # Timer im Hintergrund laufen lassen
    timer_thread = threading.Thread(target=timer_worker, daemon=True)
    timer_thread.start()
    print(f"⏱️ Timer gestartet bei {format_timer(timer_seconds)}")
    
    # Sofort aktualisieren
    update_timer_display()

def stop_timer():
    """Stoppt den Countdown-Timer"""
    global timer_active
    timer_active = False
    print("⏱️ Timer gestoppt")

def reset_timer():
    """Setzt den Timer auf 2:30 zurück"""
    global timer_seconds
    timer_seconds = MAX_TIMER_VALUE  # 2:30
    update_timer_display()
    print(f"⏱️ Timer zurückgesetzt auf {format_timer(timer_seconds)}")

def timer_worker():
    """Hintergrund-Thread für den Timer - SCHNELL & GENAU"""
    global timer_active, timer_seconds, last_timer_update
    
    print("⏱️ Timer Worker gestartet - schnelle Version")
    
    while timer_active:
        current_time = time.time()
        elapsed = current_time - last_timer_update
        
        # Genau 1 Sekunde abwarten, nicht länger
        if elapsed >= 1.0:
            timer_seconds -= 1
            last_timer_update = current_time
            
            # Timer-Display sofort aktualisieren
            update_timer_display()
            
            # Prüfen ob Minimum erreicht
            if timer_seconds <= MIN_TIMER_VALUE:
                print(f"⏱️ Timer Minimum erreicht bei {format_timer(timer_seconds)}")
                stop_timer()
                # Aktiven Status auf False, time auf Minimum-Wert
                set_active(False)
                set_time(format_timer(MIN_TIMER_VALUE))
                break
        
        # Kurze Pause um CPU nicht zu belasten
        time.sleep(0.01)

def update_timer_display():
    """Aktualisiert die Timer-Anzeige in Firebase"""
    global timer_seconds
    
    # Timer-Format: 2:29, 2:28, ..., 0:00, -0:01, ..., -2:00
    timer_display = format_timer(timer_seconds)
    firebase_set("2_30/activ/time", timer_display)
    


# Global vars
current_session = None
current_run = None

# Event handlers
def handle_start():
    global current_session
    
    current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    print(f"🚀 START {current_session}")
    
    # Altes 2_30 komplett löschen
    firebase_delete("2_30")
    
    # Timer zurücksetzen
    reset_timer()
    stop_timer()
    
    # 2_30 mit ID und allen Ordnern erstellen
    firebase_set("2_30", {
        "id": current_session,
        "runs": {
            "session_started": current_session
        },
        "missions": {
            "session_started": current_session
        },
        "activ": {
            "session_started": current_session,
            "active": False,        # Startwert: nicht aktiv
            "time": format_timer(MAX_TIMER_VALUE)  # Startwert: 2:30
        },
        "devices": {
            current_time: "Boseidon"  # Erster Eintrag im devices Ordner
        }
    })
    
    # Punkte auf 0 setzen
    firebase_set("2_30/points", 0)
    
    # Batterie initial setzen
    firebase_set("battery", 7.946)

def handle_restart():
    print("🔄 RESTART")
    
    # Bei Restart: Timer stoppen und zurücksetzen
    stop_timer()
    reset_timer()
    
    # active auf False, time auf 2:30
    set_active(False)
    set_time(format_timer(MAX_TIMER_VALUE))
    
    # Altes 2_30 löschen und neuen starten
    firebase_delete("2_30")
    
    handle_start()

def handle_battery(voltage):
    print(f"🔋 {voltage}V")
    try:
        v = float(voltage) if '.' in voltage else int(voltage)
        firebase_set("battery", v)
    except:
        pass

def handle_run(run_num, event_type, run_time=None):
    global current_run, timer_seconds
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if event_type == "start":
        current_run = run_num
        print(f"🏁 RUN {run_num} START")
        
        # WENN run-1 startet: active auf True, Timer starten
        if run_num == "1":
            set_active(True)
            start_timer()
        
        # Uhrzeit als Key, Event als Value
        firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_start")
        
    elif event_type == "stop!":
        print(f"✋ RUN {run_num} STOP")
        
        # WENN run-9 gestoppt wird: Timer stoppen, active auf False
        if run_num == "9":
            stop_timer()
            set_active(False)
        
        firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_stop")
        current_run = None
        
    elif event_type == "finish":
        # UNBEDINGT die Zeit mit übertragen
        if run_time:
            print(f"✅ RUN {run_num} DONE - {run_time}s")
            
            # WENN run-9 fertig: Timer stoppen, Zeit berechnen
            if run_num == "9":
                stop_timer()
                set_active(False)
                
                # Berechne verbleibende Zeit: 150 - run_time
                try:
                    finish_seconds = float(run_time)
                    remaining = 150 - finish_seconds
                    remaining_display = format_timer(int(round(remaining)))
                    set_time(remaining_display)
                    print(f"   Berechnung: 150 - {finish_seconds} = {remaining}s → {remaining_display}")
                except:
                    # Falls Berechnung fehlschlägt
                    set_time("0:00")
            
            # Uhrzeit als Key, Event + Zeit als Value
            firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_finish,{run_time}")
        else:
            print(f"✅ RUN {run_num} DONE")
            
            # WENN run-9 fertig OHNE Zeit: Timer anhalten, bei aktueller Zeit bleiben
            if run_num == "9":
                stop_timer()
                set_active(False)
                # Bei aktueller Zeit bleiben lassen
                current_display = format_timer(timer_seconds)
                set_time(current_display)
                print(f"   Timer angehalten bei: {current_display}")
            
            firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_finish")
        current_run = None

def handle_mission(code):
    print(f"🎯 MISSION: {code}")
    # Uhrzeit als Key, Mission-Code als Value
    timestamp = datetime.now().strftime("%H:%M:%S")
    firebase_set(f"2_30/missions/{timestamp}", code)
    
    # Punkte aus Mission-Code extrahieren (z.B. "A:10" = 10 Punkte)
    try:
        if code.startswith("A:"):
            points_str = code[2:]
            if points_str.isdigit():
                points = int(points_str)
                # Punkte in 2_30/points setzen
                firebase_set("2_30/points", points)
                print(f"   Punkte gesetzt auf: {points}")
    except:
        pass

def handle_230_event(event_type, run_time=None):
    """Behandelt 2_30 start und 2_30 finish Events"""
    
    if event_type == "finish":
        if run_time:
            print(f"🏆 2:30 FINISH - {run_time}s")
            
            # WICHTIG: Berechne verbleibende Zeit: 150 - run_time
            try:
                finish_seconds = float(run_time)
                remaining = 150 - finish_seconds
                remaining_display = format_timer(int(round(remaining)))
                
                print(f"   Berechnung: 150 - {finish_seconds} = {remaining}s")
                print(f"   Ergebnis in time: {remaining_display}")
                
                # Timer stoppen und verbleibende Zeit setzen
                stop_timer()
                set_active(False)
                set_time(remaining_display)
                
            except Exception as e:
                print(f"   Fehler bei Berechnung: {e}")
                # Falls Berechnung fehlschlägt, Timer stoppen
                stop_timer()
                set_active(False)
                set_time("0:00")
        else:
            print("🏆 2:30 FINISH")
            # Timer stoppen, aktiven Status auf False
            stop_timer()
            set_active(False)
    elif event_type == "start":
        print("🚀 2:30 START")
        # Aktiven Status auf True und Timer starten
        set_active(True)
        start_timer()

def handle_device_offline():
    """Setzt einen Offline-Eintrag im devices-Verzeichnis"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"📵 DEVICE OFFLINE - {timestamp}")
    firebase_set(f"2_30/devices/{timestamp}", "offline")
    # Timer stoppen, aktiven Status auf False
    stop_timer()
    set_active(False)

# Log file
def find_log():
    logs_path = r"C:\Users\zinssejo\AppData\Roaming\Code\logs"
    
    if not os.path.exists(logs_path):
        return None
    
    for attempt in range(5):
        patterns = [os.path.join(logs_path, "**", "*pybricks*.log")]
        all_logs = []
        for pattern in patterns:
            all_logs.extend(glob.glob(pattern, recursive=True))
        
        all_logs = list(set(all_logs))
        
        if not all_logs:
            time.sleep(2)
            continue
        
        # Find latest
        best_log = None
        latest_time = 0
        
        for log in all_logs:
            try:
                mod_time = os.path.getmtime(log)
                if mod_time > latest_time and os.path.getsize(log) > 50:
                    latest_time = mod_time
                    best_log = log
            except:
                continue
        
        if best_log:
            print(f"📄 Log: {os.path.basename(best_log)}")
            return best_log
        
        time.sleep(2)
    
    return None

# Monitor
class Monitor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_size = 0
        self.last_valid_size = 0
        self.empty_counter = 0
        self.max_empty_checks = 3  # Wie oft auf Leerheit prüfen, bevor als offline markiert
    
    def run(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)
                self.last_size = f.tell()
                self.last_valid_size = self.last_size
                
                print("\n📡 Monitoring...")
                print("=" * 40)
                
                while True:
                    if not os.path.exists(self.filepath):
                        print("❌ Log file disappeared")
                        handle_device_offline()
                        return False
                    
                    current_size = os.path.getsize(self.filepath)
                    
                    # Prüfe, ob Datei leer geworden ist (0 Bytes)
                    if current_size == 0 and self.last_valid_size > 0:
                        self.empty_counter += 1
                        print(f"⚠️ Log file empty ({self.empty_counter}/{self.max_empty_checks})")
                        
                        if self.empty_counter >= self.max_empty_checks:
                            print("❌ Log file persistently empty - marking as offline")
                            handle_device_offline()
                            return False
                    elif current_size > 0:
                        self.empty_counter = 0  # Zurücksetzen, wenn Datei wieder Inhalt hat
                        self.last_valid_size = current_size
                    
                    if current_size > self.last_size:
                        f.seek(self.last_size)
                        new_data = f.read(current_size - self.last_size)
                        self.last_size = current_size
                        
                        if new_data:
                            self.process(new_data)
                    
                    time.sleep(0.05)
                    
        except Exception as e:
            print(f"Monitor error: {e}")
            handle_device_offline()
            return False
    
    def process(self, new_data):
        for line in new_data.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # Remove timestamp
            if len(line) > 12 and line[2] == ':' and line[5] == ':':
                line = line[12:].strip()
            
            # RESTART
            if line.lower().startswith("restart"):
                handle_restart()
            
            # PROGRAM START
            elif line.startswith("program start"):
                handle_start()
            
            # BATTERY
            elif line.startswith("battery"):
                match = re.search(r'(\d+\.?\d*)', line)
                if match:
                    handle_battery(match.group(1))
            
            # RUN
            elif line.startswith("run"):
                time_match = re.search(r'finish,(\d+\.?\d+)', line)
                time_value = time_match.group(1) if time_match else None
                
                if "start" in line:
                    run_num = line.replace("run", "").replace("start", "").strip()
                    handle_run(run_num, "start")
                    
                elif "stop!" in line:
                    run_num = line.replace("run", "").replace("stop!", "").strip()
                    handle_run(run_num, "stop!")
                    
                elif "finish" in line:
                    clean_line = re.sub(r',\d+\.?\d+', '', line)
                    run_num = clean_line.replace("run", "").replace("finish", "").strip()
                    handle_run(run_num, "finish", time_value)
            
            # MISSION
            elif line.startswith("A:"):
                code = line[2:].strip()
                handle_mission(code)
            
            # 2_30 EVENTS
            elif line.startswith("2_30"):
                time_match = re.search(r'finish,(\d+\.?\d+)', line)
                time_value = time_match.group(1) if time_match else None
                
                if "start" in line:
                    handle_230_event("start")
                    
                elif "finish" in line:
                    handle_230_event("finish", time_value)

# Main
def main():
    print("="*50)
    print("SPIKE → FIREBASE BRIDGE (SCHNELLE & KORREKTE VERSION)")
    print("="*50)
    
    if not init_firebase():
        return
    
    log_file = find_log()
    if not log_file:
        print("No log file found")
        return
    
    monitor = Monitor(log_file)
    
    print("\n✅ READY - Start SPIKE program")
    print("="*50)
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopped")
        # Beim manuellen Stopp: Timer stoppen, active auf False
        stop_timer()
        set_active(False)
    except Exception as e:
        print(f"Error: {e}")
        handle_device_offline()

if __name__ == "__main__":
    main()