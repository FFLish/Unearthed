# bridge_firebase.py - CLEAN & FAST VERSION
import os
import time
from datetime import datetime
import glob
import re
import firebase_admin
from firebase_admin import credentials, db

# Firebase
SERVICE_ACCOUNT = "firebase-service-key.json"
FIREBASE_URL = "https://fll-scorer-55c47-default-rtdb.europe-west1.firebasedatabase.app"

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
    
    # 2_30 mit ID und allen Ordnern erstellen
    firebase_set("2_30", {
        "id": current_session,
        "runs": {
            "session_started": current_session
        },
        "missions": {
            "session_started": current_session
        },
        "devices": {
            current_time: "Boseidon"  # Erster Eintrag im devices Ordner
        }
    })

def handle_restart():
    print("🔄 RESTART")
    
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
    global current_run
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if event_type == "start":
        current_run = run_num
        print(f"🏁 RUN {run_num} START")
        # Uhrzeit als Key, Event als Value
        firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_start")
        
    elif event_type == "stop!":
        print(f"✋ RUN {run_num} STOP")
        firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_stop")
        current_run = None
        
    elif event_type == "finish":
        # UNBEDINGT die Zeit mit übertragen
        if run_time:
            print(f"✅ RUN {run_num} DONE - {run_time}s")
            # Uhrzeit als Key, Event + Zeit als Value
            firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_finish,{run_time}")
        else:
            print(f"✅ RUN {run_num} DONE")
            firebase_set(f"2_30/runs/{timestamp}", f"run{run_num}_finish")
        current_run = None

def handle_mission(code):
    print(f"🎯 MISSION: {code}")
    # Uhrzeit als Key, Mission-Code als Value
    timestamp = datetime.now().strftime("%H:%M:%S")
    firebase_set(f"2_30/missions/{timestamp}", code)

def handle_device_offline():
    """Setzt einen Offline-Eintrag im devices-Verzeichnis"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"📵 DEVICE OFFLINE - {timestamp}")
    firebase_set(f"2_30/devices/{timestamp}", "offline")

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

# Main
def main():
    print("="*50)
    print("SPIKE → FIREBASE BRIDGE (2:30 MODUS)")
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
    except Exception as e:
        print(f"Error: {e}")
        handle_device_offline()

if __name__ == "__main__":
    main()