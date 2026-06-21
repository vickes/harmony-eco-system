# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

# -*- coding: utf-8 -*-
"""
🤖 Arduino Uno Q Bridge Telemetry Daemon
Simulates the live Bridge RPC connection with the STM32U585 microcontroller.
Writes AES-encrypted hardware telemetries to our Eskil memory database.
"""

import sqlite3
import time
import random
import json
import os
from cryptography.fernet import Fernet

def main():
    db_path = "/root/eskil_memory.db"
    key_path = "/root/.gemini/ares_tunnel.key"
    
    print("🤖 Starting Encrypted Arduino Uno Q Bridge Telemetry Daemon...")
    
    # Load the cryptographic key
    if not os.path.exists(key_path):
        print(f"❌ Error: Key missing at {key_path}. Please generate it first.")
        return
        
    with open(key_path, "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    
    # Initialize the database with the encrypted payload column
    try:
        conn = sqlite3.connect(db_path)
        conn.isolation_level = None  # Autocommit mode
        conn.execute("DROP TABLE IF EXISTS arduino_telemetry")  # Migrate table to encrypted format
        conn.execute("CREATE TABLE arduino_telemetry (id INTEGER PRIMARY KEY, timestamp REAL, encrypted_payload TEXT)")
        conn.close()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return

    try:
        while True:
            # Gather physical values
            temp = 23.0 + random.uniform(0, 1)
            volts = 5.0 + random.uniform(-0.1, 0.1)
            speed = int(140 + random.uniform(0, 15))
            vib_freq = 30.0 + random.uniform(0, 8)
            
            # Pack into a JSON payload
            payload = {
                "t": temp,
                "v": volts,
                "s": speed,
                "f": vib_freq
            }
            json_str = json.dumps(payload)
            
            # Encrypt using Fernet AES-128/256
            encrypted_payload = fernet.encrypt(json_str.encode("utf-8")).decode("utf-8")
            
            # Write to the SQLite database
            conn = sqlite3.connect(db_path)
            conn.isolation_level = None
            conn.execute("INSERT INTO arduino_telemetry (timestamp, encrypted_payload) VALUES (?, ?)", 
                         (time.time(), encrypted_payload))
            
            # Prune old logs to keep it clean (keep last 100 rows)
            conn.execute("""
                DELETE FROM arduino_telemetry 
                WHERE id NOT IN (SELECT id FROM arduino_telemetry ORDER BY id DESC LIMIT 100)
            """)
            conn.close()
            
            # Automatically trigger dashboard generation to keep index.html perfectly live-updated
            try:
                import subprocess
                subprocess.run(["python3", "/root/generate_dashboard.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"⚠️ Dashboard generation failed: {e}")
            
            # Wait 2 seconds for next wave
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🤖 Daemon stopped manually.")

if __name__ == "__main__":
    main()
