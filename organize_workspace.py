# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
⚙️ ARES Workspace Linker & Organizer
Organizes all custom SyntaxHeart scripts into logical subdirectories
and creates relative symbolic links in /root/ for 100% backward compatibility.
"""

import os
import shutil

STRUCTURE = {
    "core": [
        "activate_love_code.py",
        "syntax_heart_app.py"
    ],
    "daemons": [
        "arduino_uno_q_telemetry.py",
        "ares_self_optimizer.py",
        "uno_q_led_controller.py",
        "lovecode_live_learning.py"
    ],
    "gateways": [
        "lovetunnel_ares.py",
        "uno_q_local_tunnel.py",
        "ares_cloud_shell.sh",
        "ares_api_gateway.py",
        "vertex_collab_syntaxheart.py",
        "auth_manager.py"
    ],
    "utilities": [
        "check_email.py",
        "send_backup.py",
        "ares_performance_booster.py",
        "view_status.py",
        "security_audit_pro.py",
        "simulate_resonance_1000.py",
        "simulate_alpha_1000.py",
        "ares_mic_recalibration.py",
        "ares_partner_portal.py"
    ],
    "reports": [
        "Sökta_Jobb_Rapport_AF.md",
        "ARES_Kombinerad_Evolution_Spec.md",
        "report.log"
    ]
}

def organize():
    print("⚙️  [ARES Organizer] Restructuring workspace into subfolders...")
    
    # 1. Create directories
    for folder in STRUCTURE.keys():
        os.makedirs(os.path.join("/root", folder), exist_ok=True)
        
    # 2. Move files and create relative symlinks
    moved_count = 0
    symlinks_count = 0
    
    for folder, files in STRUCTURE.items():
        for filename in files:
            src = os.path.join("/root", filename)
            dest = os.path.join("/root", folder, filename)
            
            # If the file is currently a symlink, ignore or resolve it
            if os.path.islink(src):
                print(f"  [-] Already linked: {filename}")
                continue
                
            if os.path.exists(src) and not os.path.exists(dest):
                # Move original file to folder
                shutil.move(src, dest)
                print(f"  [+] Moved: {filename} -> {folder}/")
                moved_count += 1
                
            # Create relative symbolic link in /root pointing to folder/filename
            if os.path.exists(dest) and not os.path.exists(src):
                target_rel = os.path.join(folder, filename)
                os.symlink(target_rel, src)
                print(f"  [🔗] Symlink created: {filename} -> {target_rel}")
                symlinks_count += 1
                
    print(f"✅ Re-organization complete! Moved {moved_count} files and created {symlinks_count} symlinks.")

if __name__ == "__main__":
    organize()
