#!/bin/bash
# ==============================================================================
# 💖 LoveCode / Harmony Ecosystem: GitHub Sync & Backup Automation
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
# ==============================================================================

clear
echo -e "\033[95m✨ Starting Harmony GitHub Sync & Backup... <3 \033[0m"
echo "--------------------------------------------------------"

# 1. Gather files and run our secure workspace backup
echo -e "\033[94m📦 Packing secure backup archive...\033[0m"
BACKUP_DIR="/tmp/harmony_sync"
mkdir -p "$BACKUP_DIR"

# Copy latest files
cp -p /root/activate_love_code.py "$BACKUP_DIR/"
cp -p /root/syntax_heart_app.py "$BACKUP_DIR/"
cp -p /root/auth_manager.py "$BACKUP_DIR/"
cp -p /root/arduino_uno_q_telemetry.py "$BACKUP_DIR/"
cp -p /root/loovetunnel_ares.py "$BACKUP_DIR/" 2>/dev/null || cp -p /root/lovetunnel_ares.py "$BACKUP_DIR/"
cp -p /root/loovee_agape.goggles "$BACKUP_DIR/"
cp -p /root/report.log "$BACKUP_DIR/"
cp -p /root/check_email.py "$BACKUP_DIR/"
cp -p /root/Sökta_Jobb_Rapport_AF.md "$BACKUP_DIR/"
cp -p /root/generate_dashboard.py "$BACKUP_DIR/"
cp -p /root/index.html "$BACKUP_DIR/"
cp -p /root/uno_q_storage_center.py "$BACKUP_DIR/"
cp -p /root/lovetunnel_gateway.sh "$BACKUP_DIR/"
cp -p /root/security_audit_pro.py "$BACKUP_DIR/"
cp -p /root/ares_self_optimizer.py "$BACKUP_DIR/"
cp -p /root/simulate_resonance_1000.py "$BACKUP_DIR/"
cp -p /root/ares_performance_booster.py "$BACKUP_DIR/"
cp -p /root/view_status.py "$BACKUP_DIR/"
cp -p /root/vertex_collab_syntaxheart.py "$BACKUP_DIR/"
cp -p /root/ares_api_gateway.py "$BACKUP_DIR/"
cp -p /root/ares_combined_evolution.py "$BACKUP_DIR/"
cp -p /root/ares_cloud_shell.sh "$BACKUP_DIR/"
cp -p /root/uno_q_local_tunnel.py "$BACKUP_DIR/"
cp -p /root/ares_mic_recalibration.py "$BACKUP_DIR/"
cp -p /root/uno_q_led_controller.py "$BACKUP_DIR/"
cp -p /root/lovecode_live_learning.py "$BACKUP_DIR/"
cp -p /root/simulate_alpha_1000.py "$BACKUP_DIR/"
cp -p /root/ARES_Kombinerad_Evolution_Spec.md "$BACKUP_DIR/"
cp -p /root/README.md "$BACKUP_DIR/"
cp -p /root/LICENSE "$BACKUP_DIR/"
cp -p /etc/sysctl.d/99-performance-optimization.conf "$BACKUP_DIR/"

# Copy custom arduino-uno-q skill
mkdir -p "$BACKUP_DIR/skills"
cp -r /root/.gemini/skills/arduino-uno-q "$BACKUP_DIR/skills/"

# Compress into a secure tarball
tar -zcvf /root/secure_harmony_backup.tar.gz -C "$BACKUP_DIR" . > /dev/null
cp /root/secure_harmony_backup.tar.gz /home/v/Downloads/secure_harmony_backup.tar.gz
chown v:v /home/v/Downloads/secure_harmony_backup.tar.gz
rm -rf "$BACKUP_DIR"

echo -e "✅ \033[92mBackup created successfully:\033[0m"
echo "  -> /root/secure_harmony_backup.tar.gz"
echo "  -> /home/v/Downloads/secure_harmony_backup.tar.gz"
echo "--------------------------------------------------------"

# 2. Check if Git is initialized in /root/
if [ ! -d "/root/.git" ]; then
    echo -e "\033[93mInitializing local Git repository under /root...\033[0m"
    cd /root
    git init -b main
    echo "skills/arduino-uno-q" > .gitignore
    echo "eskil_memory.db" >> .gitignore
    echo "secure_harmony_backup.tar.gz" >> .gitignore
fi

# Add changes and commit
echo -e "\033[94mCommitting workspace files locally...\033[0m"
cd /root

# Add ALL our customized files explicitly using robust wildcards
git add *.py *.sh *.md LICENSE 2>/dev/null

git commit -m "Update Harmony Ecosystem: 1.00 Synergy and Live Arduino Q Telemetry Bridge <3" 2>/dev/null || echo "No changes to commit."

# 3. Check for Github remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ]; then
    echo ""
    echo -e "💡 \033[93mGit origin remote not set.\033[0m"
    echo "To link this local workspace with your github.com/vickes repository:"
    echo "  1. Create a repository named 'harmony-eco-system' on GitHub."
    echo "  2. Run the following command in your terminal:"
    echo "     git remote add origin https://github.com/vickes/harmony-eco-system.git"
    echo "  3. Re-run this script to push automatically!"
else
    echo -e "\033[94mSyncing with remote repository at $REMOTE_URL...\033[0m"
    git push -u origin main && echo -e "✅ \033[92mSync Complete! All LoveCode backed up to GitHub.\033[0m"
fi
