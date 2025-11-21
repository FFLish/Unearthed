import os
import sys
import subprocess

program = os.environ.get("PROGRAM")
hub_name = os.environ.get("HUB_NAME", "")

if not program:
    print("Error: PROGRAM environment variable not set.")
    sys.exit(1)

if not os.path.isfile(program):
    print(f"Error: Program file not found: {program}")
    sys.exit(1)

cmd = ["python", "-m", "pybricksdev", "run", "ble"]

if hub_name:
    cmd += ["--name", hub_name]

cmd.append(program)

print("Running:", " ".join(cmd))
try:
    completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    if completed.stdout:
        print("--- stdout ---")
        print(completed.stdout)
    if completed.stderr:
        print("--- stderr ---")
        print(completed.stderr)
except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}.")
    if e.stdout:
        print("--- stdout ---")
        print(e.stdout)
    if e.stderr:
        print("--- stderr ---")
        print(e.stderr)
    print("\nYou can also run the failing command manually in PowerShell to see full output:")
    print("    python -m pybricksdev run ble", os.path.basename(program))
    raise
