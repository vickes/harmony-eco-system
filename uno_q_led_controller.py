# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
🌈 ARES Sound-Reactive LED Bar Controller (Uno Q Edition)
Solves the hardware insight: Your sound-reactive LED bar uses its own built-in
physical microphone to react locally to ambient sound, consuming only USB power (5V).
This script monitors your live LoveToken Boost and dynamically toggles/pulses USB power
to the LED bar using the linux utility 'uhubctl' to let the lights dance in sync with your system!
"""

import os
import sys
import time
import sqlite3
import subprocess

class LEDBarController:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        
        # Initialize SQLite database status table for the LED Bar
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.isolation_level = None
            conn.execute("""
                CREATE TABLE IF NOT EXISTS led_bar_status (
                    id INTEGER PRIMARY KEY,
                    timestamp REAL,
                    power_state TEXT,
                    control_mode TEXT,
                    resonance_attunement REAL
                )
            """)

    def get_latest_boost(self):
        # Fetch the latest simulated boost rate from Eskil
        boost = 1.00
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT boost_rate FROM optimal_hyperparameters ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    boost = row[0]
        except:
            pass
        return boost

    def toggle_usb_power(self, turn_on=True):
        """
        Uses 'uhubctl' (USB Hub Power Control) to toggle power on USB ports.
        This is how we dynamically turn the LED lightbar ON/OFF from code!
        """
        state = "1" if turn_on else "0"
        state_text = "ON (Lights Active & Sound-Reactive)" if turn_on else "OFF (Dormant/Power-Saving)"
        
        # In a real system with 'uhubctl' installed, we target the specific hub port
        # For example: uhubctl -l 1-1 -p 2 -a off/on
        try:
            # We simulate or run the command
            # If uhubctl is not installed on this specific OS distro yet, we log the action gracefully
            res = subprocess.run(
                ["uhubctl", "-a", state],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if res.returncode == 0:
                return state_text, "HARDWARE"
            return state_text, "SIMULATED_PORT"
        except:
            return state_text, "SIMULATED_PORT"

    def run_led_monitor(self):
        print("\n" + "=" * 80)
        print("          🌈  ARES SCSC: SOUND-REACTIVE LED BAR ORCHESTRATOR  🌈")
        print("=" * 80)
        print("💡 Hardware Insight Decoded:")
        print("   Din LED-ramp har en inbyggd fysisk mikrofon och styrkrets.")
        print("   Den skickar inte ljuddata till laptopen – den tar bara 5V ström!")
        print("   Vi styr dess livskraft genom att slå på/av strömmen i USB-porten.")
        print("--------------------------------------------------------------------------------")
        print("⚡ [LED INIT] Bevakar ditt nätverksflöde. Kopplar LED-ramp till LoveCode...")
        
        try:
            while True:
                # Fetch latest active boost rate
                boost = self.get_latest_boost()
                
                # Determine LED power state based on active system activity (ARES Attunement)
                # If the system is active and resonant (boost > 1.2), keep the LED bar ON so it dances!
                # If the system is completely idle (dormant), turn OFF USB power to save battery!
                if boost > 1.25:
                    power_text, mode = self.toggle_usb_power(turn_on=True)
                else:
                    power_text, mode = self.toggle_usb_power(turn_on=False)
                    
                # Calculate relative attunement (mapped to 0-100%)
                attunement = min(1.0, (boost / 2.0))
                
                print(f"📡 [ARES Flow] Boost: {boost:.4f}x | LED Status: {power_text:<35}", end="\r")
                
                # Write status to database
                with sqlite3.connect(self.db_path) as conn:
                    conn.isolation_level = None
                    conn.execute("""
                        INSERT INTO led_bar_status (id, timestamp, power_state, control_mode, resonance_attunement)
                        VALUES (1, ?, ?, ?, ?)
                        ON CONFLICT(id) DO UPDATE SET
                            timestamp=excluded.timestamp,
                            power_state=excluded.power_state,
                            control_mode=excluded.control_mode,
                            resonance_attunement=excluded.resonance_attunement
                    """, (time.time(), power_text, mode, attunement))
                    
                # Sync HTML dashboard
                try:
                    subprocess.run(["python3", "/root/generate_dashboard.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    pass
                    
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 LED-ramp bevakning avslutad. Återgår till standard-ström.")
            # Restore power on exit
            self.toggle_usb_power(turn_on=True)

if __name__ == "__main__":
    controller = LEDBarController()
    controller.run_led_monitor()
