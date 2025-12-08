# bridge_firebase.py - EINFACHE VERSION
import os
import time
import json
import requests
from datetime import datetime
import glob
import re

FIREBASE_URL = "https://fll-scorer-55c47-default-rtdb.europe-west1.firebasedatabase.app"

# Globale Variablen
current_session = None
current_run = None
battery_voltage = None

def find_pybricks_log():
    """Findet oder wartet auf Pybricks Log-Dateien"""
    logs_path = r"C:\Users\zinssejo\AppData\Roaming\Code\logs"
    
    if not os.path.exists(logs_path):
        print(f"FEHLER: VS Code Log-Ordner nicht gefunden: {logs_path}")
        return None
    
    print("SUCHE PYBRICKS LOG-DATEIEN...")
    print("-" * 50)
    
    for attempt in range(1, 6):
        print(f"Versuche {attempt}/5...")
        
        patterns = [
            os.path.join(logs_path, "**", "*pybricks*.log"),
            os.path.join(logs_path, "**", "*Pybricks*.log"),
            os.path.join(logs_path, "**", "*output*.log"),
        ]
        
        all_logs = []
        for pattern in patterns:
            all_logs.extend(glob.glob(pattern, recursive=True))
        
        all_logs = list(set(all_logs))
        
        if not all_logs:
            print("  Keine Log-Dateien gefunden.")
            print("  Warte 5 Sekunden...")
            time.sleep(5)
            continue
        
        print(f"  Gefunden: {len(all_logs)} Log-Dateien")
        
        best_log = None
        best_freshness = 0
        
        for log_file in all_logs:
            try:
                size = os.path.getsize(log_file)
                mod_time = os.path.getmtime(log_file)
                time_diff = time.time() - mod_time
                
                filename = os.path.basename(log_file)
                print(f"    {filename}: {size/1024:.1f} KB")
                
                if size > 50 and time_diff < 300:
                    freshness = size / (time_diff + 1)
                    if freshness > best_freshness:
                        best_freshness = freshness
                        best_log = log_file
                        
            except:
                continue
        
        if best_log:
            size = os.path.getsize(best_log) / 1024
            mod_str = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(best_log)))
            
            print(f"\nOK: AKTIVE LOG-DATEI GEFUNDEN!")
            print(f"   DATEI: {os.path.basename(best_log)}")
            print(f"   GROESSE: {size:.1f} KB")
            print(f"   LETZTE AENDERUNG: {mod_str}")
            return best_log
        else:
            print(f"  {len(all_logs)} Logs gefunden, aber keine aktiven.")
            print(f"  Warte 5 Sekunden...")
            time.sleep(5)
    
    print("\nFEHLER: KEINE AKTIVE LOG-DATEI GEFUNDEN!")
    return None

def delete_robogame():
    """Löscht komplett robogame"""
    try:
        response = requests.delete(f"{FIREBASE_URL}/robogame.json", timeout=3)
        print("🗑️  RoboGame komplett gelöscht")
        return True
    except Exception as e:
        print(f"✗ Fehler beim Löschen: {e}")
        return False

def create_empty_robogame():
    """Erstellt leeres RoboGame mit leeren Listen"""
    try:
        robogame_data = {
            "runs": [],
            "missions": []
        }
        response = requests.put(f"{FIREBASE_URL}/robogame.json", json=robogame_data, timeout=5)
        
        if response.status_code == 200:
            print("✓ RoboGame mit leeren Listen erstellt")
            return True
        else:
            print(f"✗ Fehler: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Fehler: {e}")
        return False

def update_battery(voltage):
    """Aktualisiert Batteriewert (überschreibt)"""
    global battery_voltage
    battery_voltage = voltage
    print(f"🔋 BATTERIE: {voltage}V")
    
    try:
        data = {'voltage': float(voltage) if '.' in voltage else int(voltage)}
        response = requests.put(
            f"{FIREBASE_URL}/battery.json", 
            json=data, 
            timeout=3
        )
        if response.status_code == 200:
            print(f"   ✓ Batterie aktualisiert: {voltage}V")
    except Exception as e:
        print(f"   ✗ Batterie-Fehler: {e}")

def add_to_runs_list(run_event):
    """Fügt ein Run-Event zur Runs-Liste hinzu - EINFACHE VERSION"""
    try:
        # Hole die aktuelle runs-Liste
        response = requests.get(f"{FIREBASE_URL}/robogame/runs.json", timeout=3)
        
        runs_list = []
        if response.status_code == 200 and response.text != "null":
            try:
                data = response.json()
                if isinstance(data, list):
                    runs_list = data
            except:
                pass
        
        # Füge neues Event hinzu
        runs_list.append(run_event)
        
        # Speicere zurück
        response = requests.put(
            f"{FIREBASE_URL}/robogame/runs.json",
            json=runs_list,
            timeout=3
        )
        
        if response.status_code == 200:
            print(f"   ✓ Run hinzugefügt: {run_event}")
        else:
            print(f"   ✗ Konnte nicht speichern: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Fehler: {e}")

def add_to_missions_list(mission_code):
    """Fügt eine Missionsnummer zur Missions-Liste hinzu - EINFACHE VERSION"""
    try:
        # Hole die aktuelle missions-Liste
        response = requests.get(f"{FIREBASE_URL}/robogame/missions.json", timeout=3)
        
        missions_list = []
        if response.status_code == 200 and response.text != "null":
            try:
                data = response.json()
                if isinstance(data, list):
                    missions_list = data
            except:
                pass
        
        # Füge Missionsnummer hinzu
        missions_list.append(mission_code)
        
        # Speicere zurück
        response = requests.put(
            f"{FIREBASE_URL}/robogame/missions.json",
            json=missions_list,
            timeout=3
        )
        
        if response.status_code == 200:
            print(f"   ✓ Mission hinzugefügt: {mission_code}")
        else:
            print(f"   ✗ Konnte nicht speichern: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Fehler: {e}")

def handle_program_start():
    """Behandelt Programmstart - Löscht und erstellt neu"""
    global current_session
    
    now = datetime.now()
    current_session = now.strftime("%Y-%m-%d_%H-%M")
    
    print(f"\n🚀 PROGRAMM START - Session: {current_session}")
    
    # 1. Altes RoboGame löschen
    delete_robogame()
    
    # 2. Neues leeres RoboGame erstellen
    create_empty_robogame()

def handle_restart():
    """Behandelt Restart - Gleiche wie program start"""
    global current_session
    
    print(f"\n🔄 RESTART")
    
    # 1. Altes RoboGame löschen
    delete_robogame()
    
    # 2. Neues leeres RoboGame erstellen
    create_empty_robogame()
    
    # Session neu starten
    now = datetime.now()
    current_session = now.strftime("%Y-%m-%d_%H-%M")
    print(f"   Neue Session: {current_session}")

def handle_run_event(run_num, event_type, time_value=None):
    """Behandelt Run-Events"""
    global current_run
    
    if event_type == "start":
        current_run = run_num
        print(f"\n🏁 RUN {run_num} START")
        add_to_runs_list(f"run{run_num}_start")
        
    elif event_type == "stop!":
        print(f"✋ RUN {run_num} STOPP")
        add_to_runs_list(f"run{run_num}_stop")
        current_run = None
        
    elif event_type == "finish":
        run_time = None
        if time_value:
            run_time = time_value
            print(f"✅ RUN {run_num} FERTIG - Zeit: {run_time}s")
            add_to_runs_list(f"run{run_num}_finish,{run_time}")
        else:
            print(f"✅ RUN {run_num} FERTIG")
            add_to_runs_list(f"run{run_num}_finish")
        current_run = None

def handle_mission(mission_code):
    """Behandelt Mission"""
    print(f"🎯 MISSION: {mission_code}")
    add_to_missions_list(mission_code)

class FileMonitor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_size = 0
        print(f"UEBERWACHE: {os.path.basename(filepath)}")
        
    def monitor(self):
        """Ueberwacht Dateiaenderungen"""
        try:
            if not os.path.exists(self.filepath):
                print(f"FEHLER: Datei nicht mehr gefunden!")
                return False
            
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)
                self.last_size = f.tell()
                
                print(f"STARTGROESSE: {self.last_size} bytes")
                print("WARTE AUF DATEN VON SPIKE PRIME...")
                print("-" * 50)
                
                last_activity = time.time()
                
                while True:
                    if not os.path.exists(self.filepath):
                        print("DATEI GELOESCHT - BEENDE")
                        return False
                    
                    current_size = os.path.getsize(self.filepath)
                    
                    if current_size < self.last_size:
                        f.seek(0)
                        self.last_size = 0
                        current_size = os.path.getsize(self.filepath)
                    
                    if current_size > self.last_size:
                        f.seek(self.last_size)
                        new_data = f.read(current_size - self.last_size)
                        self.last_size = current_size
                        
                        if new_data:
                            self.process_new_data(new_data)
                            last_activity = time.time()
                    
                    if time.time() - last_activity > 30:
                        self.show_status()
                        last_activity = time.time()
                    
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"FEHLER: {e}")
            return False
    
    def process_new_data(self, new_data):
        """Verarbeitet die Daten"""
        lines = new_data.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Entferne Zeitstempel
            clean_line = line
            if len(line) > 12 and line[2] == ':' and line[5] == ':':
                clean_line = line[12:].strip()
            
            # RESTART
            if clean_line.lower().startswith("restart"):
                handle_restart()
            
            # PROGRAM START
            elif clean_line.startswith("program start"):
                handle_program_start()
            
            # BATTERY
            elif clean_line.startswith("battery"):
                match = re.search(r'(\d+\.?\d*)', clean_line)
                if match:
                    voltage = match.group(1)
                    update_battery(voltage)
            
            # RUN
            elif clean_line.startswith("run"):
                time_match = re.search(r'finish,(\d+\.?\d+)', clean_line)
                time_value = time_match.group(1) if time_match else None
                
                if "start" in clean_line:
                    run_num = clean_line.replace("run", "").replace("start", "").strip()
                    handle_run_event(run_num, "start")
                    
                elif "stop!" in clean_line:
                    run_num = clean_line.replace("run", "").replace("stop!", "").strip()
                    handle_run_event(run_num, "stop!")
                    
                elif "finish" in clean_line:
                    clean_for_run = re.sub(r',\d+\.?\d+', '', clean_line)
                    run_num = clean_for_run.replace("run", "").replace("finish", "").strip()
                    handle_run_event(run_num, "finish", time_value)
            
            # A: MISSIONEN
            elif clean_line.startswith("A:"):
                mission_code = clean_line[2:].strip()
                handle_mission(mission_code)
    
    def show_status(self):
        """Zeigt Status an"""
        try:
            if os.path.exists(self.filepath):
                size_kb = os.path.getsize(self.filepath) / 1024
                
                print(f"\n📊 STATUS")
                print(f"   Datei: {os.path.basename(self.filepath)}")
                print(f"   Größe: {size_kb:.1f} KB")
                print(f"   Session: {current_session or 'Keine'}")
                print(f"   Aktiver Run: {current_run or 'Keiner'}")
                print(f"   Batterie: {battery_voltage or 'Unbekannt'}V")
                print("-" * 40)
        except:
            pass

def main():
    print("="*60)
    print("SPIKE PRIME -> FIREBASE BRIDGE")
    print("EINFACHE VERSION: Löscht RoboGame bei Start/Restart")
    print("="*60)
    
    print("\n⚠️  WICHTIG: RoboGame wird bei 'program start' oder 'restart' gelöscht!")
    print("   Alle alten Daten gehen verloren!")
    
    print("\nSUCHE LOG-DATEI...")
    target_file = find_pybricks_log()
    
    if not target_file:
        print("\nBRIDGE KANN NICHT STARTEN.")
        print("Bitte VS Code mit Pybricks starten und SPIKE verbinden.")
        return
    
    print("\n" + "="*60)
    print("BRIDGE LÄUFT...")
    print("="*60)
    
    monitor = FileMonitor(target_file)
    
    print("\nBRIDGE BEREIT!")
    print("\nFEUERFREI! Starte dein SPIKE-Programm in VS Code")
    print("\nBei 'program start' oder 'restart':")
    print("  - Altes RoboGame wird gelöscht")
    print("  - Neues leeres RoboGame wird erstellt")
    print("\nDrücke STRG+C zum Beenden")
    print("="*60)
    
    try:
        monitor.monitor()
    except KeyboardInterrupt:
        print("\n✓ BRIDGE GESTOPPT")
    except Exception as e:
        print(f"\n✗ FEHLER: {e}")
    
    print("\nBRIDGE BEENDET")

if __name__ == "__main__":
    main()