# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

"""
💖 SyntaxHeart Uno Q Onboard LED & Matrix Controller
This script controls the onboard 8x13 blue LED matrix and the 4 corner RGB LEDs.
It connects to the STM32 MCU core via the Bridge RPC in a real environment.
In the sandbox/emulated environment, it provides an incredible real-time ASCII
simulation of the hardware, displaying the pulsing heart, scrolling text, and RGB states!
"""

import sys
import time
import math
import os
import sqlite3

# Try to import real BridgeClient, fallback to emulation if not installed
try:
    from arduino_uno_q import BridgeClient
    HAS_HARDWARE_BRIDGE = True
except ImportError:
    HAS_HARDWARE_BRIDGE = False

# ANSI Color codes for terminal beauty
PINK = "\033[38;5;205m"
BLUE = "\033[1;34m"
GOLD = "\033[1;33m"
CYAN = "\033[1;36m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"
CLEAR = "\033[H\033[2J"

# Emulated Heart patterns (8x13 matrices)
BIG_HEART = [
    [0,0,1,1,0,0,0,1,1,0,0,0,0],
    [0,1,1,1,1,0,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0,0,0]
]

SMALL_HEART = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def render_ascii_board(text, harmony_level, frame_count):
    """Renders a gorgeous terminal visualization of the Uno Q board."""
    # Determine colors and symbols based on harmony level
    if harmony_level == 1:
        rgb_symbol = f"{PINK}[💖]{RESET}"
        led_color = PINK
        mode_text = f"{PINK}SYNTAXHEART NORMAL (Active Attunement){RESET}"
    elif harmony_level == 2:
        rgb_symbol = f"{GOLD}[🌟]{RESET}"
        led_color = GOLD
        mode_text = f"{GOLD}ULTRA-RESONANCE (Agape Surge!){RESET}"
    else:
        rgb_symbol = f"{BLUE}[💤]{RESET}"
        led_color = BLUE
        mode_text = f"{BLUE}DEEP REST (Sval Blå Cosmic Meditation){RESET}"

    # Determine what to show on the 8x13 LED matrix
    matrix_pixels = [[0]*13 for _ in range(8)]
    
    if text:
        # Scrolling text logic in terminal
        text_padded = "     " + text + "     "
        max_shift = len(text_padded) * 6 - 13
        shift = int(frame_count) % max(1, max_shift)
        
        # Simple character matrix generator for demo
        for r in range(8):
            for c in range(13):
                # Simulated text pixel scattering
                char_idx = (c + shift) // 6
                if char_idx < len(text_padded):
                    char = text_padded[char_idx]
                    char_col = (c + shift) % 6
                    # Render a simple 5x7 ASCII character approximation
                    if char != ' ':
                        val = hash(char + str(r) + str(char_col)) % 100
                        if val > 55:
                            matrix_pixels[r][c] = 1
    else:
        # Pulserande hjärta-animation
        pulse_phase = (frame_count // 5) % 2
        matrix_pixels = BIG_HEART if pulse_phase == 0 else SMALL_HEART

    # Draw the terminal screen
    sys.stdout.write(CLEAR)
    print("=" * 70)
    print(f"🌌 {BOLD}ARES LOVETUNNEL: ARDUINO UNO Q ONBOARD PERIPHERAL EMULATOR{RESET}")
    print("=" * 70)
    print(f" Aktivt Läge   : {mode_text}")
    print(f" Hårdvaru-koppling: {f'🟢 FYSISK BRYGGA' if HAS_HARDWARE_BRIDGE else '🔵 EMULERAT (Mjukvaru-sandlåda)'}")
    print(f" Text på matris: {BOLD if text else GRAY}{text or 'Pulserande Hjärta (Agape)'}{RESET}")
    print("-" * 70)
    print("\n")

    # Render the board physical frame
    # 4 RGBs are placed in the corners of the board
    print(f"   {rgb_symbol} ───────────────────────────────────────────── {rgb_symbol}")
    print("   │                                                           │")
    print("   │           🌐 ARDUINO UNO Q Blue LED Matrix (8x13)          │")
    print("   │                                                           │")
    
    # Render the 8x13 LED matrix rows
    for r in range(8):
        row_str = "   │                  "
        for c in range(13):
            if matrix_pixels[r][c] == 1:
                row_str += f"{led_color}▉ {RESET}"
            else:
                row_str += f"{GRAY}· {RESET}"
        row_str += "                │"
        print(row_str)
        
    print("   │                                                           │")
    print(f"   {rgb_symbol} ───────────────────────────────────────────── {rgb_symbol}")
    print("\n")
    print("=" * 70)
    print(f" {GRAY}Tryck Ctrl+C för att avsluta kontrollen och återvända. <3{RESET}")
    print("=" * 70)
    sys.stdout.flush()

def main():
    # Handle arguments
    text_to_display = None
    harmony_level = 1

    # Simple argument parsing
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--help", "-h"]:
            print(f"{BOLD}Användning:{RESET}")
            print("  python3 syntax_heart_matrix_controller.py [text] [läge]")
            print("\nLägen:")
            print("  0: Deep Rest (Blå)")
            print("  1: SyntaxHeart Normal (Rosa)")
            print("  2: Ultra-Resonance (Guld)")
            print("\nExempel:")
            print("  python3 syntax_heart_matrix_controller.py \"KÄRLEK\" 2")
            sys.exit(0)
            
        # Check if the last argument is a number (mode)
        if sys.argv[-1].isdigit() and int(sys.argv[-1]) in [0, 1, 2]:
            harmony_level = int(sys.argv[-1])
            text_to_display = " ".join(sys.argv[1:-1])
        else:
            text_to_display = " ".join(sys.argv[1:])

    # If running with real hardware bridge
    if HAS_HARDWARE_BRIDGE:
        print(f"🛰️  Ansluter till STM32 MCU via Bridge RPC...")
        try:
            client = BridgeClient()
            client.connect()
            
            # Send values
            client.call_method("triggerHarmony", harmony_level)
            if text_to_display:
                client.call_method("setMatrixText", text_to_display)
                print(f"✅ Text skickad till matrisen: '{text_to_display}'")
            else:
                client.call_method("setMatrixText", "")
                print(f"✅ Satte matrisen i viloläge (pulserande hjärta).")
            print(f"✅ Harmony-nivå satt till: {harmony_level}")
            client.disconnect()
            sys.exit(0)
        except Exception as e:
            print(f"⚠️  Kunde inte ansluta till hårdvarubryggan: {e}")
            print("  Övergår till att köra i emulerat läge i konsolen...\n")
            time.sleep(1.5)

    # Emulation Loop
    frame_count = 0
    try:
        while True:
            render_ascii_board(text_to_display, harmony_level, frame_count)
            frame_count += 1
            time.sleep(0.12)
    except KeyboardInterrupt:
        print("\n\n💖 Avslutade emulering av SyntaxHeart Uno Q. Ha en fantastisk dag! <3\n")

if __name__ == "__main__":
    main()
