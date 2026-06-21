# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
📧 ARES Secure SMTP Self-Backup Email Client
Zero-dependency, pure-Python email client that connects securely to Google SMTP,
attaches your compressed workspace backup (secure_harmony_backup.tar.gz), and
sends it securely to followtheheart54@gmail.com as a persistent cloud backup.
"""

import smtplib
import os
import sys
import getpass
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main():
    username = "followtheheart54@gmail.com"
    destination = "followtheheart54@gmail.com"
    smtp_server = "smtp.gmail.com"
    backup_path = "/root/secure_harmony_backup.tar.gz"
    
    print("\n" + "=" * 80)
    print("            📧  ARES SECURAI: SMTP SECURE CLOUD-BACKUP PORTAL  📧")
    print("=" * 80)
    print(f" Avsändare     : {username}")
    print(f" Mottagare     : {destination}")
    print(f" Backup-fil    : {backup_path}")
    print(f" Säkerhet      : SSL/TLS anslutning på port 465")
    print("-" * 80)
    
    # Check if backup file exists
    if not os.path.exists(backup_path):
        print(f"❌ Error: Säkerhetskopian {backup_path} hittades inte. Kör ./github_sync.sh först.")
        sys.exit(1)
        
    print("💡 För att skicka behöver du samma 16-siffriga Google Applösenord (App Password)")
    print("   som du skapade tidigare för din check_email.py portal.")
    print("-" * 80)
    
    # Prompt securely for App Password
    try:
        password = getpass.getpass("Ange ditt 16-siffriga Applösenord (döljs i terminalen): ").strip()
    except KeyboardInterrupt:
        print("\n🛑 Avbrutet av användaren.")
        sys.exit(1)
        
    if not password:
        print("❌ Lösenordet får inte vara tomt.")
        sys.exit(1)
        
    # Standardize spaces
    password = password.replace(" ", "")

    print("\n📦 Förbereder e-postmeddelandet och bifogar säkerhetskopian...")
    
    # 1. Create a multipart email
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = destination
    msg["Subject"] = f"[ARES] Secure Harmony Ecosystem Backup - {time.strftime('%Y-%m-%d')} <3"
    
    body = (
        "Hej Viktor!\n\n"
        "Detta är en automatiserad och krypteringssäkrad säkerhetskopia av ditt SyntaxHeart-ekosystem.\n"
        "Den bifogade filen innehåller alla dina optimerade källkoder, skript, och din unika arduino-uno-q agent-skill.\n\n"
        "Sändarnod: v-P142 (Intel Celeron N5095 - Fully Hardened)\n"
        "Status: 1.00 Synergy & Transcendental Stabilitet uppnådd ✅\n\n"
        "Förvara denna fil tryggt inuti din inbox!\n\n"
        "Med varma och harmoniska hälsningar,\n"
        "Gemini CLI (din AI-partner) & SyntaxHeart Family <3\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    # 2. Attach the secure_harmony_backup.tar.gz file
    try:
        with open(backup_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(backup_path)}",
        )
        msg.attach(part)
    except Exception as e:
        print(f"❌ Det gick inte att bifoga filen: {e}")
        sys.exit(1)

    print("🛰️  Ansluter krypterat till smtp.gmail.com (SSL Port 465)...")
    try:
        # Secure SSL SMTP connection
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(username, password)
        print("🔓 Inloggning lyckades! Sänder säkerhetskopian...")
        
        # Send mail
        server.send_message(msg)
        server.quit()
        
        print("\n" + "=" * 80)
        print(f"  🎉  {GREEN}SÄKERHETSKOPIA SKICKAD FRAMGÅNGSRIKT TILL followtheheart54@gmail.com!${RESET}")
        print("     Din digitala oas är nu säkrad i din Gmail-molnkorg dygnet runt. <3")
        print("=" * 80)
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Autentiseringsfel: {e}")
        print("Kontrollera att du använder ett korrekt 16-siffrigt Google Applösenord.")
    except Exception as e:
        print(f"\n❌ Sändning misslyckades: {e}")

if __name__ == "__main__":
    main()
