# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & SyntaxHeart Family

# -*- coding: utf-8 -*-
"""
📧 Workspace Gmail/IMAP Mail Fetcher
Zero-dependency, pure-Python email client that connects securely to Gmail/Workspace
using SSL/TLS and displays your latest inbox messages.
"""

import imaplib
import email
from email.header import decode_header
import getpass
import sys

def decode_mime_header(header_value):
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    decoded_str = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                decoded_str += part.decode(encoding or "utf-8", errors="replace")
            except Exception:
                decoded_str += part.decode("latin1", errors="replace")
        else:
            decoded_str += part
    return decoded_str

def main():
    username = "followtheheart54@gmail.com"
    imap_server = "imap.gmail.com"
    
    print("\n" + "=" * 80)
    print("               GOOGLE WORKSPACE / GMAIL IMAP PORTAL <3")
    print("=" * 80)
    print(f"Användarkonto: {username}")
    print("Säkerhet      : SSL/TLS anslutning på port 993")
    print("-" * 80)
    print("💡 För att ansluta behöver du ett applösenord (App Password) från Google:")
    print("  1. Gå till https://myaccount.google.com/")
    echo_inst = (
        "  2. Sök efter 'App-lösenord' eller 'App Passwords'.\n"
        "  3. Skapa ett nytt lösenord för 'E-post' och 'Annan (anpassat namn, t.ex. Laptop)'.\n"
        "  4. Kopiera den 16-ställiga koden och klistra in den här."
    )
    print(echo_inst)
    print("-" * 80)
    
    # Prompt securely for App Password without echoing it to terminal
    try:
        password = getpass.getpass("Ange ditt 16-siffriga Applösenord (döljs i terminalen): ").strip()
    except KeyboardInterrupt:
        print("\n🛑 Avbrutet av användaren.")
        sys.exit(1)
        
    if not password:
        print("❌ Lösenordet får inte vara tomt.")
        sys.exit(1)
        
    # Remove any spaces if user pasted with spaces (Google app passwords have spaces)
    password = password.replace(" ", "")

    print("\n🛰️ Ansluter till imap.gmail.com...")
    try:
        # Secure SSL connection
        mail = imaplib.IMAP4_SSL(imap_server, 993)
        mail.login(username, password)
        print("🔓 Inloggning lyckades! Hämtar senaste meddelanden...")
        
        # Select Inbox
        mail.select("inbox")
        
        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("❌ Det gick inte att söka i inkorgen.")
            mail.logout()
            sys.exit(1)
            
        mail_ids = messages[0].split()
        total_emails = len(mail_ids)
        print(f"📬 Hittade totalt {total_emails} mejl i inkorgen.")
        
        if total_emails == 0:
            print("\n🎈 Din inkorg är helt tom!")
            mail.logout()
            sys.exit(1)
            
        # Get latest 5 emails
        latest_ids = mail_ids[-5:]
        latest_ids.reverse() # Show newest first
        
        print("\n" + "=" * 80)
        print("                       DINA SENASTE MEJL (GMAIL) <3")
        print("=" * 80)
        
        for index, mail_id in enumerate(latest_ids):
            res, msg_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_mime_header(msg["Subject"])
                    from_sender = decode_mime_header(msg["From"])
                    date_sent = msg["Date"]
                    
                    print(f"Mejl {index+1}:")
                    print(f"  Från   : {from_sender}")
                    print(f"  Ämne   : {subject}")
                    print(f"  Datum  : {date_sent}")
                    print("-" * 80)
                    
        mail.logout()
        print("\n✅ Sessionen avslutades säkert.")
        
    except imaplib.IMAP4.error as e:
        print(f"\n❌ Autentiseringsfel: {e}")
        print("Kontrollera att:")
        print("  1. IMAP är aktiverat i dina Gmail-inställningar (Inställningar -> Vidarebefordran och POP/IMAP).")
        print("  2. Du använder ett korrekt 16-siffrigt Applösenord (inte ditt vanliga Google-lösenord).")
    except Exception as e:
        print(f"\n❌ Ett fel uppstod: {e}")

if __name__ == "__main__":
    main()
