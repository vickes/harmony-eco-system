# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
🎙️ ARES Voice Trigger Daemon
Zero-dependency, high-efficiency real-time audio stream analyser.
Streams raw PCM bytes from ALSA default input, calculates RMS volume spikes,
and automatically triggers your Vocal & Visual Partner Portal!
"""

import os
import sys
import time
import math
import struct
import subprocess

class VoiceTriggerDaemon:
    def __init__(self):
        self.threshold = 4000  # Voice spike RMS threshold (adjust based on room noise)
        self.portal_path = "/root/utilities/ares_partner_portal.py"
        self.last_trigger_time = 0

    def run_voice_loop(self):
        print("\n" + "=" * 80)
        print("          🎙️  ARES VOICE TRIGGER DAEMON: REAL-TIME ALSA MONITOR  🎙️")
        print("=" * 80)
        print(f"📡 Threshold: {self.threshold} RMS | Target: {self.portal_path}")
        print("⚡ [VOICE INIT] Streaming raw S16_LE 8000Hz mono PCM from microphone...")
        
        # Start arecord as a subprocess streaming raw PCM to stdout
        cmd = ["arecord", "-D", "plughw:0,0", "-f", "S16_LE", "-r", "8000", "-c", "1", "-t", "raw"]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"❌ Failed to start arecord: {e}")
            sys.exit(1)

        # Buffer parameters: read 100ms of audio (800 samples = 1600 bytes) at each tick
        chunk_size = 1600
        
        try:
            while True:
                data = proc.stdout.read(chunk_size)
                if not data:
                    break
                    
                # Calculate RMS (Root Mean Square) volume level
                count = len(data) // 2
                shorts = struct.unpack(f"<{count}h", data)
                
                sum_squares = 0.0
                for sample in shorts:
                    n = sample / 32768.0  # Normalize S16 to float (-1.0 to 1.0)
                    sum_squares += n * n
                    
                rms = math.sqrt(sum_squares / count) if count > 0 else 0.0
                rms_scaled = int(rms * 32768)
                
                # Check for voice trigger threshold
                now = time.time()
                if rms_scaled > self.threshold and (now - self.last_trigger_time > 10):
                    self.last_trigger_time = now
                    print(f"\n🎙️  [VOICE TRIGGERED] Sound spike detected: {rms_scaled} RMS! Activating Partner Portal...")
                    
                    # Temporarily stop our own arecord process so the camera capture and speaking can run safely
                    # (Prevent ALSA lock collisions)
                    proc.terminate()
                    proc.wait()
                    
                    # Execute Partner Portal
                    subprocess.run(["python3", self.portal_path])
                    
                    # Restart the arecord stream
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    print("\n⚡ [VOICE RE-INIT] Microphone streaming resumed. Monitoring...")
                    
        except KeyboardInterrupt:
            print("\n🛑 Voice trigger daemon stopped manually.")
        finally:
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    daemon = VoiceTriggerDaemon()
    daemon.run_voice_loop()
