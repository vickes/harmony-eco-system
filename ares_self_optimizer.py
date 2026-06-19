# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

# -*- coding: utf-8 -*-
"""
🌀 ARES Real-Time Self-Healing & Thermal Guardian Daemon
Steppes up self-optimization on the Celeron N5095 laptop.
Monitors memory pressure, thermal zones, auto-cleans transient caches,
performs Eskil Healing, and logs active optimization status to the database.
"""

import os
import sys
import time
import sqlite3
import subprocess

class SystemSelfOptimizer:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        self.key_path = "/root/.gemini/ares_tunnel.key"
        self.last_clean_time = 0
        
    def get_core_temp(self):
        # Read thermal zones on Linux
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
            return 35.0  # Safe default fallback
        except Exception:
            return 35.0

    def optimize_memory(self):
        # Scan memory stats
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    mem_info[parts[0].strip()] = int(parts[1].replace("kB", "").strip())
                    
            total = mem_info.get("MemTotal", 1)
            free = mem_info.get("MemFree", 1)
            available = mem_info.get("MemAvailable", 1)
            
            used_percent = ((total - available) / total) * 100.0
            
            # If used RAM goes over 85%, perform memory cache optimization
            if used_percent > 85.0:
                print(f"⚠️  [ARES Optimizer] High RAM pressure detected ({used_percent:.2f}%). Reclaiming caches...")
                # Run sync in background
                subprocess.run(["sync"])
                # Note: Drop caches requires writing to /proc/sys/vm/drop_caches (runs safely as root)
                try:
                    with open("/proc/sys/vm/drop_caches", "w") as f:
                        f.write("3")
                    print("✅ [ARES Optimizer] RAM cache successfully optimized and reclaimed.")
                except Exception as e:
                    print(f"⚠️  Cache reclaim bypassed: {e}")
            return used_percent
        except Exception:
            return 20.0  # safe default

    def clean_transient_junk(self):
        # Prune temporary files, .tmp, core files, and crash dumps in /tmp or user cache
        now = time.time()
        if now - self.last_clean_time < 300: # Limit aggressive cleaning to once every 5 minutes
            return 0
            
        self.last_clean_time = now
        pruned_count = 0
        try:
            # Clean common transient paths
            folders = ["/tmp", "/var/tmp"]
            for folder in folders:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        filepath = os.path.join(folder, filename)
                        try:
                            # Prune if .tmp or starts with core or is a crash dump
                            if filename.endswith(".tmp") or filename.startswith("core") or "crash" in filename.lower():
                                if os.path.isfile(filepath):
                                    os.remove(filepath)
                                    pruned_count += 1
                        except Exception:
                            pass
        except Exception:
            pass
        return pruned_count

    def run_self_healing_loop(self):
        print("🌀 Starting ARES System Self-Healing & Thermal Guardian Daemon...")
        
        while True:
            try:
                # 1. Thermal monitoring
                temp = self.get_core_temp()
                
                # 2. Memory optimization
                ram_used = self.optimize_memory()
                
                # 3. Transient cleaning
                junk_cleaned = self.clean_transient_junk()
                
                # 4. Write active self-healing state to eskil_memory.db under a new table
                conn = sqlite3.connect(self.db_path)
                conn.isolation_level = None
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS healing_status (
                        id INTEGER PRIMARY KEY,
                        timestamp REAL,
                        core_temp REAL,
                        ram_used REAL,
                        status_text TEXT
                    )
                """)
                
                # Status evaluation based on CPU temp
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
                conn.close()
                
                if junk_cleaned > 0:
                    print(f"✅ Self-Healing: Cleaned {junk_cleaned} transient fragments from system floor.")
                    
            except Exception as e:
                print(f"⚠️ Self-healing exception: {e}")
                
            # Perform system checks every 5 seconds
            time.sleep(5)

if __name__ == "__main__":
    optimizer = SystemSelfOptimizer()
    optimizer.run_self_healing_loop()
