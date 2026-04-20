#!/usr/bin/env python3
"""Test the clap trigger with simulated audio input"""

import numpy as np
import time
import subprocess
import os
import json
import sys

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

WORKSPACE_PATH = config["workspace_path"]
if os.name == 'nt':
    SCRIPT_PATH = os.path.join(WORKSPACE_PATH, "scripts", "launch-session.ps1")
else:
    SCRIPT_PATH = os.path.join(WORKSPACE_PATH, "scripts", "launch-session.sh")

THRESHOLD = 0.15
MIN_GAP = 0.1
MAX_GAP = 1.2

print("[TEST] Simulating clap trigger...")
print(f"[TEST] Will execute: {SCRIPT_PATH}")
print("[TEST] Simulating first clap in 1 second...")

time.sleep(1)
first_clap = time.time()
print(f"[TEST] First clap detected at {first_clap:.3f}")

print("[TEST] Simulating second clap in 0.5 seconds...")
time.sleep(0.5)
second_clap = time.time()
gap = second_clap - first_clap

print(f"[TEST] Second clap detected at {second_clap:.3f}")
print(f"[TEST] Gap between claps: {gap:.3f}s")

if MIN_GAP <= gap <= MAX_GAP:
    print("[TEST] ✓ Valid gap detected! Firing launch script...")
    if os.name == 'nt':
        subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", SCRIPT_PATH])
    else:
        os.chmod(SCRIPT_PATH, 0o755)
        subprocess.Popen(["bash", SCRIPT_PATH])
    print("[TEST] Launch script executed!")
else:
    print(f"[TEST] ✗ Invalid gap {gap:.3f}s (needs {MIN_GAP}-{MAX_GAP}s)")
    sys.exit(1)
