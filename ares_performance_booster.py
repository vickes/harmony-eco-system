# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & SyntaxHeart Family

# -*- coding: utf-8 -*-
"""
🚀 ARES CPU Core & SSD Cache Optimizer Add-on
An advanced kernel-level tuning script designed to boost the performance
of the Intel Celeron N5095 processor and 1TB SATA SSD (sda).
Sets CPU Energy Performance Preference and tunes storage read-ahead caches.
"""

import os
import sys
import sqlite3
import time
import subprocess

class ARESPerformanceBooster:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        
    def tune_intel_cpu(self):
        print("⚡ [ARES Booster] Optimizing Intel Celeron N5095 CPU Core scaling...")
        epp_dir = "/sys/devices/system/cpu"
        cores_tuned = 0
        
        # Check and configure Energy Performance Preference (EPP)
        try:
            if os.path.exists(epp_dir):
                for dirname in os.listdir(epp_dir):
                    if dirname.startswith("cpu") and dirname[3:].isdigit():
                        epp_path = os.path.join(epp_dir, dirname, "cpufreq/energy_performance_preference")
                        if os.path.exists(epp_path):
                            # Set EPP to balance_performance (ideal for laptop snappiness vs thermal limits)
                            with open(epp_path, "w") as f:
                                f.write("balance_performance")
                            cores_tuned += 1
                if cores_tuned > 0:
                    print(f"✅ Successfully tuned {cores_tuned} Intel CPU cores to 'balance_performance'.")
                    return f"Tuned {cores_tuned} CPU Cores (balance_performance)"
            return "Intel CPU EPP not supported or managed by hardware"
        except Exception as e:
            return f"CPU tuning bypassed: {e}"

    def tune_ssd_cache(self):
        print("💾 [ARES Booster] Optimizing 1TB SSD (sda) read-ahead cache...")
        dev_path = "/dev/sda"
        try:
            if os.path.exists(dev_path):
                # Set read-ahead sector size to 4096 (accelerates sequential disk reads)
                res = subprocess.run(["blockdev", "--setra", "4096", dev_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if res.returncode == 0:
                    print("✅ Successfully optimized SSD read-ahead to 4096 sectors.")
                    return "SSD Read-Ahead set to 4096 (Optimized)"
            return "Target SSD /dev/sda not found"
        except Exception as e:
            return f"SSD tuning bypassed: {e}"

    def apply_all_boosts(self):
        print("\n" + "=" * 80)
        print("          ARES PERFORMANCE BOOSTER: HARDWARE KERNEL TUNING ADD-ON")
        print("=" * 80)
        
        cpu_status = self.tune_intel_cpu()
        ssd_status = self.tune_ssd_cache()
        
        # Log this performance optimization event in SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            conn.isolation_level = None
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_boosts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    cpu_status TEXT,
                    ssd_status TEXT,
                    active_status TEXT
                )
            """)
            conn.execute("""
                INSERT INTO performance_boosts (timestamp, cpu_status, ssd_status, active_status)
                VALUES (?, ?, ?, ?)
            """, (time.time(), cpu_status, ssd_status, "OPTIMIZED"))
            conn.close()
            print("📝 Performance tuning event logged in Eskil Database.")
        except Exception as e:
            print(f"⚠️ Failed to log tuning event: {e}")
            
        print("=" * 80)

if __name__ == "__main__":
    booster = ARESPerformanceBooster()
    booster.apply_all_boosts()
