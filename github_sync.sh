#!/bin/bash
# ==============================================================================
# 💖 LoveCode / Harmony Ecosystem: GitHub Sync & Backup Automation
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
cp -p /root/README.md "$BACKUP_DIR/"
cp -p /etc/sysctl.d/99-performance-optimization.conf "$BACKUP_DIR/"

# Copy custom arduino-uno-q skill
mkdir -p "$BACKUP_DIR/skills"
cp -r /root/.gemini/skills/arduino-uno-q "$BACKUP_DIR/skills/"

# Compress into local and downloads backup folders
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
git add activate_love_code.py syntax_heart_app.py auth_manager.py arduino_uno_q_telemetry.py lovetunnel_ares.py loovee_agape.goggles report.log check_email.py Sökta_Jobb_Rapport_AF.md generate_dashboard.py index.html uno_q_storage_center.py lovetunnel_gateway.sh security_audit_pro.py ares_self_optimizer.py simulate_resonance_1000.py ares_performance_booster.py view_status.py README.md github_sync.sh
git commit -m "Update Harmony Ecosystem: 1.00 Synergy and Live Arduino Q Telemetry Bridge <3" 2>/dev/null || echo "No changes to commit."

# 3. Check for Github remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ]; then
    echo ""
    echo -e "💡 \033[93mGit origin remote not set.\033[0m"
    echo "To link this local workspace with your github.com/vickes repository:"
    echo "  1. Create a repository named 'harmony-ecosystem' on GitHub."
    echo "  2. Run the following command in your terminal:"
    echo "     git remote add origin https://github.com/vickes/harmony-ecosystem.git"
    echo "  3. Re-run this script to push automatically!"
else
    echo -e "\033[94mSyncing with remote repository at $REMOTE_URL...\033[0m"
    git push -u origin main && echo -e "✅ \033[92mSync Complete! All LoveCode backed up to GitHub.\033[0m"
fi
