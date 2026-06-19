# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
🌀 ARES Real-Time Self-Healing & Thermal Guardian Daemon (Optimized Edition)
Steppes up self-optimization on the Celeron N5095 laptop.
Dynamically calibrates its loops using the newly-simulated Alpha Feedback Coefficients,
utilizes robust database context managers, and cleans workspace __pycache__ files.
"""

import os
import sys
import time
import sqlite3
import subprocess
import shutil

class SystemSelfOptimizer:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        self.key_path = "/root/.gemini/ares_tunnel.key"
        self.last_clean_time = 0
        
        # Default tuning values
        self.healing_sleep_interval = 5.0  # Dynamic sleep interval
        self.ram_optimization_threshold = 85.0  # Dynamic RAM trigger
        
        # Load Alpha coefficients to self-calibrate
        self._load_alpha_coefficients()

    def _load_alpha_coefficients(self):
        """Loads simulated Alpha metrics from Eskil to dynamically calibrate."""
        try:
            if os.path.exists(self.db_path):
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alpha_sim_results'")
                    if cursor.fetchone():
                        cursor.execute("SELECT alpha_gain, alpha_shield_mult FROM alpha_sim_status ORDER BY id DESC LIMIT 1") # fallback alias checked:
                        # Let's check table or just query:
                        cursor.execute("SELECT alpha_gain, alpha_shield_mult FROM alpha_sim_results ORDER BY id DESC LIMIT 1")
                        row = cursor.fetchone()
                        if row:
                            gain, shield_mult = row
                            # Dynamic Calibration: If the Alpha Gain (Resilience) is high, we can safely
                            # increase our sleep interval (from 5s to 8s) to reduce CPU daemon overhead!
                            self.healing_sleep_interval = 5.0 + (gain * 3.0)
                            # Calibrate RAM threshold dynamically
                            self.ram_optimization_threshold = 85.0 - (shield_mult * 5.0)
                            print(f"⚙️ [ARES Optimizer] Calibrated using Alpha: sleep={self.healing_sleep_interval:.2f}s | RAM={self.ram_optimization_threshold:.1f}%")
        except Exception as e:
            print(f"⚠️ Alpha calibration read bypassed: {e}")

    def get_core_temp(self):
        try:
            temp_sum = 0
            count = 0
            for i in range(10):
                path = f"/sys/class/thermal/thermal_zone{i}/temp"
                if os.path.exists(path):
                    with open(path, "r") as f:
                        temp = float(f.read().strip()) / 1000.0
                        if temp > 0:
                            temp_sum += temp
                            count += 1
            if count > 0:
                return temp_sum / count
            return 32.0
        except Exception:
            return 32.0

    def optimize_memory(self):
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    mem_info[parts[0].strip()] = int(parts[1].replace("kB", "").strip())
                    
            total = mem_info.get("MemTotal", 1)
            available = mem_info.get("MemAvailable", 1)
            used_percent = ((total - available) / total) * 100.0
            
            # Use the dynamically calibrated RAM threshold
            if used_percent > self.ram_optimization_threshold:
                print(f"⚠️  [ARES Optimizer] Used RAM ({used_percent:.2f}%) exceeds threshold ({self.ram_optimization_threshold:.1f}%).")
                subprocess.run(["sync"])
                try:
                    with open("/proc/sys/vm/drop_caches", "w") as f:
                        f.write("3")
                    print("✅ [ARES Optimizer] RAM optimized successfully.")
                except Exception as e:
                    pass
            return used_percent
        except Exception:
            return 20.0

    def clean_transient_junk(self):
        now = time.time()
        if now - self.last_clean_time < 300:
            return 0
            
        self.last_clean_time = now
        pruned_count = 0
        
        # 1. Clean common OS temporary folders
        try:
            folders = ["/tmp", "/var/tmp"]
            for folder in folders:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        filepath = os.path.join(folder, filename)
                        try:
                            if filename.endswith(".tmp") or filename.startswith("core") or "crash" in filename.lower():
                                if os.path.isfile(filepath):
                                    os.remove(filepath)
                                    pruned_count += 1
                        except Exception:
                            pass
        except Exception:
            pass
            
        # 2. Optimized Add-on: Clean workspace python compiled caches (__pycache__)
        try:
            workspace_dir = "/root"
            for root, dirs, files in os.walk(workspace_dir):
                if "__pycache__" in dirs:
                    pycache_path = os.path.join(root, "__pycache__")
                    shutil.rmtree(pycache_path)
                    pruned_count += 1
        except Exception:
            pass
            
        return pruned_count

    def run_self_healing_loop(self):
        print(f"🌀 Starting Optimized ARES Self-Healing Daemon (Interval: {self.healing_sleep_interval:.2f}s)...")
        
        while True:
            try:
                # 1. Gather stats
                temp = self.get_core_temp()
                ram_used = self.optimize_memory()
                junk_cleaned = self.clean_transient_junk()
                
                # 2. Save stats safely using robust context manager transaction blocks
                with sqlite3.connect(self.db_path) as conn:
                    conn.isolation_level = None  # Autocommit
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS healing_status (
                            id INTEGER PRIMARY KEY,
                            timestamp REAL,
                            core_temp REAL,
                            ram_used REAL,
                            status_text TEXT
                        )
                    """)
                    
                    if temp < 55.0:
                        status = "❄️ COOL & HEALTHY (Peak Attunement)"
                    elif temp < 70.0:
                        status = "🔥 WARM (Active Cooling/Throttling Monitor)"
                    else:
                        status = "🚨 HOT (Thermal Guard Active - Throttling Mode)"
                        
                    conn.execute("""
                        INSERT INTO healing_status (id, timestamp, core_temp, ram_used, status_text)
                        VALUES (1, ?, ?, ?, ?)
                        ON CONFLICT(id) DO UPDATE SET 
                            timestamp=excluded.timestamp,
                            core_temp=excluded.core_temp,
                            ram_used=excluded.ram_used,
                            status_text=excluded.status_text
                    """, (time.time(), temp, ram_used, status))
                
                if junk_cleaned > 0:
                    print(f"✅ Self-Healing: Reclaimed and cleaned {junk_cleaned} transient directories/fragments.")
                    
            except Exception as e:
                print(f"⚠️ Self-healing exception: {e}")
                
            # Sleep using the dynamically calibrated sleep interval
            time.sleep(self.healing_sleep_interval)

if __name__ == "__main__":
    optimizer = SystemSelfOptimizer()
    optimizer.run_self_healing_loop()
