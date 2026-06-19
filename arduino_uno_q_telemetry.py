# -*- coding: utf-8 -*-
"""
🤖 Arduino Uno Q Bridge Telemetry Daemon
Simulates the live Bridge RPC connection with the STM32U585 microcontroller.
Writes active hardware telemetries to our Eskil memory database.
"""

import sqlite3
import time
import random

def main():
    db_path = "/root/eskil_memory.db"
    print("🤖 Starting Arduino Uno Q Bridge Telemetry Daemon...")
    
    # Enable autocommit for immediate lock-free sqlite writes
    conn = sqlite3.connect(db_path)
    conn.isolation_level = None
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS arduino_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            temperature REAL,
            voltage REAL,
            motor_speed INTEGER,
            vibration_freq REAL
        )
    """)
    conn.close()

    while True:
        try:
            # Generate simulated hardware telemetry with realistic small oscillations
            temp = random.normalvariate(23.5, 0.2)
            volts = random.normalvariate(5.02, 0.05)
            speed = int(random.normalvariate(150, 5))
            vib_freq = random.normalvariate(14.0, 0.1) # 14Hz local quartz oscillation
            
            # Write to database
            conn = sqlite3.connect(db_path)
            conn.isolation_level = None
            conn.execute(
                "INSERT INTO arduino_telemetry (timestamp, temperature, voltage, motor_speed, vibration_freq) VALUES (?, ?, ?, ?, ?)",
                (time.time(), temp, volts, speed, vib_freq)
            )
            
            # Limit database to last 100 rows to prevent bloat
            conn.execute("""
                DELETE FROM arduino_telemetry 
                WHERE id NOT IN (
                    SELECT id FROM arduino_telemetry 
                    ORDER BY timestamp DESC LIMIT 100
                )
            """)
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Telemetry write failure: {e}")
            
        # Update metrics every 2 seconds
        time.sleep(2)

if __name__ == "__main__":
    main()
