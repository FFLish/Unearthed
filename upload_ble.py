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

# Diagnostic info
print("Python executable:", sys.executable)
print("PATH:", os.environ.get("PATH", "(none)"))

# Run without raising so we can show stdout/stderr and return code
completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
print(f"Command exited with return code: {completed.returncode}")
if completed.stdout:
    print("--- stdout ---")
    print(completed.stdout)
if completed.stderr:
    print("--- stderr ---")
    print(completed.stderr)

if completed.returncode != 0:
    print("\nCommand failed. You can reproduce manually in PowerShell to see full interactive output:")
    print(f"    python -m pybricksdev run ble \"{program}\"")
    # Exit with the same return code. Use os._exit to avoid a SystemExit traceback
    # when this script is executed inside interactive/debug consoles.
    os._exit(completed.returncode)
