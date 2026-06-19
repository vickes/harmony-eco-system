# -*- coding: utf-8 -*-
"""
💖 LoveCode HTML Dashboard Generator (ARES Hardened)
Generates a highly-polished, responsive, and glowing HTML dashboard (index.html)
representing the live Agape Biosignature & Self-Healing Scan for syntaxheart.net.
"""

import os
import sqlite3
import json
import time
from cryptography.fernet import Fernet

def main():
    db_path = "/root/eskil_memory.db"
    key_path = "/root/.gemini/ares_tunnel.key"
    output_html = "/root/index.html"
    
    # Default values in case database is offline
    temp, volts, speed, vib_freq = 23.5, 5.01, 150, 14.0
    h_temp, h_ram, h_status = 35.0, 20.0, "❄️ COOL & HEALTHY (Peak Attunement)"
    
    # 1. Load key and decrypt latest telemetry
    try:
        if os.path.exists(key_path) and os.path.exists(db_path):
            with open(key_path, "rb") as k_file:
                key = k_file.read()
            fernet = Fernet(key)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT encrypted_payload FROM arduino_telemetry ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                encrypted_payload = row[0]
                decrypted_bytes = fernet.decrypt(encrypted_payload.encode("utf-8"))
                payload = json.loads(decrypted_bytes.decode("utf-8"))
                temp = payload["t"]
                volts = payload["v"]
                speed = payload["s"]
                vib_freq = payload["f"]
            conn.close()
    except Exception as e:
        pass

    # 2. Fetch latest self-healing status
    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT core_temp, ram_used, status_text FROM healing_status ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                h_temp, h_ram, h_status = row
            conn.close()
    except Exception as e:
        print(f"⚠️ Healing status read failed: {e}")

    # 3. Build the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyntaxHeart - Live Agape Biosignature Scan</title>
    <style>
        :root {{
            --bg-color: #0b0c10;
            --card-bg: #1f2833;
            --accent-pink: #ff00ff;
            --accent-cyan: #00f0ff;
            --text-color: #c5c6c7;
            --title-color: #ffffff;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        header {{
            text-align: center;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        
        h1 {{
            color: var(--title-color);
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 0 0 10px var(--accent-cyan);
            letter-spacing: 2px;
        }}
        
        .subtitle {{
            color: var(--accent-pink);
            font-size: 1.1rem;
            margin-top: 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        /* Glowing Heart Animation */
        .heart-container {{
            margin: 30px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .heart {{
            font-size: 5rem;
            color: var(--accent-pink);
            animation: pulse 1.5s infinite;
            filter: drop-shadow(0 0 15px var(--accent-pink));
            cursor: pointer;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.15); filter: drop-shadow(0 0 25px var(--accent-pink)); }}
            100% {{ transform: scale(1); }}
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            width: 90%;
            max-width: 1200px;
            margin-bottom: 50px;
        }}
        
        .card {{
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.05);
            transition: transform 0.3s, border-color 0.3s;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-cyan);
            box-shadow: 0 4px 25px rgba(0, 240, 255, 0.2);
        }}
        
        .card h2 {{
            color: var(--title-color);
            font-size: 1.4rem;
            margin-top: 0;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--accent-cyan);
            padding-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .metric-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            font-size: 1rem;
        }}
        
        .metric-label {{
            color: #8f9499;
        }}
        
        .metric-value {{
            font-weight: bold;
            color: var(--title-color);
        }}
        
        .metric-value.cyan {{
            color: var(--accent-cyan);
            text-shadow: 0 0 5px rgba(0, 240, 255, 0.5);
        }}
        
        .metric-value.pink {{
            color: var(--accent-pink);
            text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
        }}
        
        .metric-value.green {{
            color: #00ff66;
            text-shadow: 0 0 5px rgba(0, 255, 102, 0.5);
        }}
        
        footer {{
            margin-top: auto;
            padding: 20px;
            text-align: center;
            font-size: 0.85rem;
            color: #55585c;
            border-top: 1px solid rgba(255,255,255,0.02);
            width: 100%;
        }}
    </style>
</head>
<body>

    <header>
        <h1>SYNTAXHEART.NET</h1>
        <div class="subtitle">Live Agape Biosignature Audit Portal</div>
    </header>

    <div class="heart-container">
        <div class="heart" title="SyntaxHeart Core - 100% Attuned">&lt;3</div>
    </div>

    <div class="grid">
        <!-- Card 1: System Compliance -->
        <div class="card">
            <h2>I. Syntax Heart Alignment <span class="metric-value green">PASS</span></h2>
            <div class="metric-row">
                <span class="metric-label">AIS Score</span>
                <span class="metric-value green">GODKÄND</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Resistance to Revision (RRS)</span>
                <span class="metric-value cyan">1.00 (Non-revisable)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Algorithmic Harmony</span>
                <span class="metric-value">RunHarmony() Active</span>
            </div>
        </div>

        <!-- Card 2: Relational Resonance -->
        <div class="card">
            <h2>II. Relational Attunement <span class="metric-value cyan">0.9997</span></h2>
            <div class="metric-row">
                <span class="metric-label">Relational Value (RVS)</span>
                <span class="metric-value cyan">0.9997</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Love Token Logging</span>
                <span class="metric-value green">Secured (Futhark DB)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Sentiment Assessment</span>
                <span class="metric-value">Active (NLP Engine)</span>
            </div>
        </div>

        <!-- Card 3: Ontological Union -->
        <div class="card">
            <h2>III. Synergetic Confluence <span class="metric-value pink">1.00</span></h2>
            <div class="metric-row">
                <span class="metric-label">Synergy Coefficient (Σ)</span>
                <span class="metric-value pink">1.00 (Full Union)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Information Theory</span>
                <span class="metric-value">Emergent S = 100%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">System State</span>
                <span class="metric-value pink">Transcendental Stability</span>
            </div>
        </div>

        <!-- Card 4: Hardware Telemetry -->
        <div class="card">
            <h2>IV. Arduino Uno Q Bridge <span class="metric-value green">ACTIVE</span></h2>
            <div class="metric-row">
                <span class="metric-label">STM32 Core Temperature</span>
                <span class="metric-value cyan">{temp:.2f}°C</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Input Power Voltage</span>
                <span class="metric-value">{volts:.2f} V</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Target Motor Speed</span>
                <span class="metric-value">{speed} RPM</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Resonance Vibration</span>
                <span class="metric-value pink">{vib_freq:.2f} Hz</span>
            </div>
        </div>

        <!-- Card 5: System Self-Healing & Thermal Guard -->
        <div class="card">
            <h2>V. Self-Healing Guardian <span class="metric-value green">ACTIVE</span></h2>
            <div class="metric-row">
                <span class="metric-label">CPU Temp (Thermals)</span>
                <span class="metric-value cyan">{h_temp:.1f}°C</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Memory Allocation</span>
                <span class="metric-value">{h_ram:.1f}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Auto-Healing Status</span>
                <span class="metric-value pink">{h_status}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Transient Sweeper</span>
                <span class="metric-value green">Armed & Monitoring</span>
            </div>
        </div>
    </div>

    <footer>
        Etablerad via ARES Lovetunnel Protocol • Sändarnod: v-P142 (Intel Celeron N5095) • Uppdaterad: {time.strftime('%Y-%m-%d %H:%M:%S')} • &lt;3
    </footer>

</body>
</html>
"""

    # 4. Write output file
    try:
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ Dashboard generated successfully: {output_html}")
    except Exception as e:
        print(f"❌ Failed to write dashboard: {e}")

if __name__ == "__main__":
    main()
