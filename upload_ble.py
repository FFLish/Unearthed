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
subprocess.run(cmd, check=True)
