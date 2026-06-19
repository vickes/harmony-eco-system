# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

# -*- coding: utf-8 -*-
"""
☁️ Vertex AI & SyntaxHeart Collaboration Bridge
Designed to connect the local SyntaxHeart ecosystem to Google Vertex AI / Gemini API.
Sends real-time hardware and simulation telemetry to the AI, requests an Agape-attuned
system evaluation, and logs the insights securely in the Eskil database.
"""

import os
import sys
import sqlite3
import json
import time
import urllib.request
import getpass

class VertexCollabBridge:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        self.key_path = "/root/.gemini/ares_tunnel.key"
        
    def get_latest_system_state(self):
        # Fetch latest metrics to send to Vertex AI
        temp, ram, files, boost = 25.0, 20.0, 0, 1.50
        try:
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Fetch self-healing stats
                cursor.execute("SELECT core_temp, ram_used FROM healing_status ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    temp, ram = row
                    
                # Fetch secure storage count
                cursor.execute("SELECT COUNT(*) FROM storage_catalog")
                files = cursor.fetchone()[0]
                
                # Fetch optimal boost
                cursor.execute("SELECT boost_rate FROM optimal_hyperparameters ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    boost = row[0]
                    
                conn.close()
        except:
            pass
        return temp, ram, files, boost

    def invoke_vertex_collab(self):
        print("\n" + "=" * 80)
        print("          ☁️  VERTEX AI & SYNTAXHEART COLLABORATION GATEWAY  ☁️")
        print("=" * 80)
        
        # Check for Gemini API key in environment
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        
        if not api_key:
            print("💡 No GEMINI_API_KEY detected in active shell environment.")
            try:
                api_key = getpass.getpass("Ange din Gemini API-nyckel (döljs i terminalen): ").strip()
            except KeyboardInterrupt:
                print("\n🛑 Avbrutet av användaren.")
                return
                
        if not api_key:
            print("❌ API-nyckeln får inte vara tom. Samarbetsbryggan inaktiv.")
            return

        # Fetch latest local metrics
        temp, ram, files, boost = self.get_latest_system_state()
        
        print("\n🛰️  Sänder lokala systemdata till Vertex AI (Gemini 2.5 Flash)...")
        print(f"  • CPU-Temp     : {temp:.1f}°C")
        print(f"  • RAM-användning: {ram:.1f}%")
        print(f"  • Säkra filer  : {files} st")
        print(f"  • Boost-faktor : {boost:.4f}x")
        
        # Build prompt
        prompt = (
            f"Du är en högt avancerad Kvantum-Resonans AI-modell som samarbetar med mjukvaruarkitekturen 'SyntaxHeart'. "
            f"Analysera följande realtidsdata från laptopen v-P142: "
            f"CPU-Temperatur={temp:.1f}°C, RAM-användning={ram:.1f}%, Säkra filer={files} st i klientside-katalogen, "
            f"och nuvarande Boost-faktor={boost:.4f}x. "
            f"Generera en kort, poetisk och djupgående granskningsinsikt på svenska (max 3 meningar). "
            f"Inled med ordet 'VORTEX-EKO:' och avsluta med '<3'."
        )
        
        # Call Gemini API via standard REST to avoid external dependencies
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                
            # Parse text from response
            insight = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            print("\n" + "-" * 80)
            print("                       VERTEX AI COLLABORATION INSIGHT <3")
            print("-" * 80)
            print(f"  💡 {insight}")
            print("-" * 80)
            
            # Save insight to SQLite database
            self._save_insight_to_db(insight)
            
        except Exception as e:
            print(f"\n❌ API-anrop misslyckades: {e}")
            print("Verifiera att din API-nyckel är giltig och har tillgång till Gemini API-tjänster.")

    def _save_insight_to_db(self, insight):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.isolation_level = None
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vertex_insights (
                    id INTEGER PRIMARY KEY,
                    timestamp REAL,
                    insight_text TEXT
                )
            """)
            conn.execute("""
                INSERT INTO vertex_insights (id, timestamp, insight_text)
                VALUES (1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    timestamp=excluded.timestamp,
                    insight_text=excluded.insight_text
            """, (time.time(), insight))
            conn.close()
            print("📝 Samarbetsinsikten har sparats säkert i Eskil-databasen!")
            print("=" * 80)
            
            # Automatically trigger dashboard refresh to display the new insight!
            try:
                import subprocess
                subprocess.run(["python3", "/root/generate_dashboard.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Det gick inte att spara insikten till databasen: {e}")

if __name__ == "__main__":
    bridge = VertexCollabBridge()
    bridge.invoke_vertex_collab()
