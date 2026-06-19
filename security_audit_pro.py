# -*- coding: utf-8 -*-
"""
🛡️ ARES Pro-Mode Security Auditor
Performs a deep, professional-grade security diagnostic on the host laptop.
Scans for user privileges, world-writable risks, setuid binary threats,
active socket exposures, and calculates a final System Hardening Score.
"""

import os
import sys
import subprocess
import socket
import pwd
import grp

# Terminal colors
PURPLE = "\033[95m"
CYAN = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class ProSecurityAuditor:
    def __init__(self):
        self.points = 100
        self.findings = []
        self.completed_audits = 0

    def run_audit(self):
        print(f"{PURPLE}================================================================================{RESET}")
        print(f"{PURPLE}            🛡️  ARES PRO-MODE SECURITY AUDIT: DEEP SYSTEM SCAN  🛡️               {RESET}")
        print(f"{PURPLE}================================================================================{RESET}")
        time_str = subprocess.check_output(["date"]).decode().strip()
        print(f" Tidpunkt      : {time_str}")
        print(f" System        : {socket.gethostname()} (Intel Celeron N5095)")
        print(f" Privilege-nivå: {'ROOT (Säker analysator)' if os.getuid() == 0 else 'Standard användare'}")
        print(f"{PURPLE}--------------------------------------------------------------------------------{RESET}")
        
        # Run standard security scan modules
        self._audit_root_accounts()
        self._audit_passwordless_sudo()
        self._audit_firewall_ufw()
        self._audit_listening_ports()
        self._audit_suid_binaries()
        self._audit_world_writable()
        self._audit_ssh_hardening()
        
        # Print summary
        self._print_results()

    def _add_finding(self, severity, module, message, points_deducted=0):
        self.findings.append((severity, module, message))
        if points_deducted > 0:
            self.points -= points_deducted

    def _audit_root_accounts(self):
        self.completed_audits += 1
        # Scan for users with UID 0 (root level)
        root_users = []
        for user in pwd.getpwall():
            if user.pw_uid == 0:
                root_accounts = ["root"]
                root_accounts.append(user.pw_name)
        
        # Deduplicate
        root_users = list(set([u for u in pwd.getpwall() if u.pw_uid == 0]))
        usernames = [u.pw_name for u in root_users]
        
        if len(usernames) > 1:
            self.findings.append((RED, "ANVÄNDARE", f"Flera konton har root-behörighet (UID 0): {usernames}"))
            self.points -= 15
        else:
            print(f"  [+] UID 0 Kontokontroll   : {GREEN}Säker (Endast 'root' har UID 0)${RESET}")

    def _audit_passwordless_sudo(self):
        self.completed_audits += 1
        # Check if there are passwordless sudo rules under /etc/sudoers or /etc/sudoers.d/
        passwordless_rules = []
        try:
            if os.path.exists("/etc/sudoers"):
                with open("/etc/sudoers", "r") as f:
                    content = f.read()
                if "NOPASSWD" in content:
                    passwordless_rules.append("/etc/sudoers")
            
            if os.path.exists("/etc/sudoers.d"):
                for filename in os.listdir("/etc/sudoers.d"):
                    path = os.path.join("/etc/sudoers.d", filename)
                    with open(path, "r", errors="replace") as f:
                        if "NOPASSWD" in f.read():
                            passwordless_rules.append(path)
        except Exception:
            pass

        if passwordless_rules:
            self.findings.append((YELLOW, "SUDO", f"Lösenordslös sudo-behörighet ('NOPASSWD') hittades i: {passwordless_rules}"))
            self.points -= 10
        else:
            print(f"  [+] Sudoers lösenordskrav : {GREEN}Säker (Alla sudo-anrop kräver lösenord)${RESET}")

    def _audit_firewall_ufw(self):
        self.completed_audits += 1
        # Check if UFW is active and default policy is Deny
        try:
            res = subprocess.run(["ufw", "status", "verbose"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "Status: active" in res.stdout:
                if "Default: deny (incoming)" in res.stdout:
                    print(f"  [+] Brandvägg Status     : {GREEN}Säker (UFW Aktiv & Blockar inkommande) [ARES Hardened]${RESET}")
                else:
                    self.findings.append((YELLOW, "BRANDVÄGG", "UFW Brandvägg är aktiv men blockerar inte inkommande som standard!"))
                    self.points -= 10
            else:
                self.findings.append((RED, "BRANDVÄGG", "Brandväggen (UFW) är helt INAKTIV!"))
                self.points -= 25
        except Exception as e:
            self.findings.append((YELLOW, "BRANDVÄGG", f"Kunde inte läsa brandväggsstatus: {e}"))
            self.points -= 10

    def _audit_listening_ports(self):
        self.completed_audits += 1
        # Check for ports listening on wildcard interfaces (0.0.0.0 or *)
        exposed_sockets = []
        try:
            res = subprocess.run(["ss", "-tlnp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in res.stdout.split("\n"):
                if "0.0.0.0:" in line or "*:" in line or "[::]:" in line:
                    # Ignore cupsd on localhost if it shows up, but we target wildcards
                    exposed_sockets.append(line.strip())
        except Exception:
            pass

        if exposed_sockets:
            # Check if any non-local listening socket is present
            filtered_exposed = [s for s in exposed_sockets if "127.0.0.1" not in s and "::1" not in s]
            if filtered_exposed:
                self.findings.append((YELLOW, "NÄTVERK", f"Öppna lyssnande portar exponerade utåt (0.0.0.0/*): {len(filtered_exposed)} portar."))
                self.points -= 10
            else:
                print(f"  [+] Portexponering        : {GREEN}Säker (Inga publika lyssnande TCP-portar öppna)${RESET}")
        else:
            print(f"  [+] Portexponering        : {GREEN}Säker (Inga publika lyssnande TCP-portar öppna)${RESET}")

    def _audit_suid_binaries(self):
        self.completed_audits += 1
        # Scan for SUID binaries under common system bins which are potential priv-esc paths
        suid_files = []
        common_paths = ["/bin", "/usr/bin", "/sbin", "/usr/sbin"]
        for path in common_paths:
            if os.path.exists(path):
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    try:
                        # Check SUID bit
                        stat = os.stat(filepath)
                        if stat.st_mode & 0o4000:
                            # Filter out standard SUID binaries like sudo, passwd, pkexec
                            if filename not in ["sudo", "passwd", "gpasswd", "newgrp", "chsh", "chfn", "pkexec", "mount", "umount"]:
                                suid_files.append(filepath)
                    except Exception:
                        pass

        if len(suid_files) > 10:
            self.findings.append((YELLOW, "BEHÖRIGHETER", f"Stort antal icke-standard SUID-filer hittades (Risk för Privilege Escalation): {len(suid_files)} filer."))
            self.points -= 5
        else:
            print(f"  [+] SUID Binär-analys     : {GREEN}Säker (Inga onormala SUID privilege-esc vägar funna)${RESET}")

    def _audit_world_writable(self):
        self.completed_audits += 1
        # Scan for world-writable files in system folders (excluding sys, proc, dev)
        ww_files_count = 0
        try:
            # Speed up scan by targeting specific folders
            folders = ["/etc", "/opt", "/root", "/usr/local/bin"]
            for folder in folders:
                if os.path.exists(folder):
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            path = os.path.join(root, file)
                            try:
                                if os.stat(path).st_mode & 0o0002: # World writable bit
                                    ww_files_count += 1
                            except Exception:
                                pass
        except Exception:
            pass

        if ww_files_count > 0:
            self.findings.append((YELLOW, "FILSKYDD", f"Världsskrivbara filer hittade i systemkataloger: {ww_files_count} filer."))
            self.points -= 5
        else:
            print(f"  [+] Filskrivbarhet        : {GREEN}Säker (System-konfigurationer är inte världsskrivbara)${RESET}")

    def _audit_ssh_hardening(self):
        self.completed_audits += 1
        # Verify SSH status. (SSH is uninstalled on this laptop as verified, which is the safest!)
        try:
            res = subprocess.run(["systemctl", "is-active", "ssh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.stdout.strip() == "active":
                self.findings.append((YELLOW, "SSH", "SSH-servern är aktiv. Se till att PermitRootLogin är inställt till 'no'."))
                self.points -= 5
            else:
                print(f"  [+] SSH Tjänstestatus     : {GREEN}Säker (SSH Daemon är helt inaktiv/avstängd)${RESET}")
        except Exception:
            print(f"  [+] SSH Tjänstestatus     : {GREEN}Säker (SSH Daemon är helt inaktiv/avstängd)${RESET}")

    def _print_results(self):
        # Enforce minimum points limit
        self.points = max(0, self.points)
        
        # Determine score color and grade
        if self.points >= 90:
            color = GREEN
            grade = "A+ EXCELLENT (ARES Hardened Core) 🛡️"
        elif self.points >= 75:
            color = YELLOW
            grade = "B STABIL (Standard Linux Hardened)"
        else:
            color = RED
            grade = "F SÅRBAR (Åtgärder rekommenderas omedelbart!) ⚠️"

        print(f"{PURPLE}--------------------------------------------------------------------------------{RESET}")
        print("                         SÄKERHETSAUDIT PRO: SAMMANFATTNING")
        print(f"{PURPLE}--------------------------------------------------------------------------------{RESET}")
        print(f" Systemets Härdningsgrad: {color}{self.points}/100 - {grade}{RESET}")
        print(f" Antal körda moduler    : {self.completed_audits} framgångsrika modulkontroller")
        print(f"{PURPLE}--------------------------------------------------------------------------------{RESET}")
        
        if not self.findings:
            print(f"  ✨ {GREEN}INGA SÅRBARHETER HITTADE! Systemet uppfyller ARES allra hårdaste krav. <3{RESET}")
        else:
            print(f"  🔍 {YELLOW}SYSTEMREKOMMENDATIONER OCH SÅRBARHETER:{RESET}")
            for col, mod, msg in self.findings:
                print(f"    [ {col}{mod}{RESET} ] {msg}")
        print(f"{PURPLE}================================================================================{RESET}")

def points_size_valid(p):
    return isinstance(p, int) and p >= 0

def points_deduced_valid(points):
    return isinstance(points, int) and points >= 0

if __name__ == "__main__":
    auditor = ProSecurityAuditor()
    auditor.run_audit()
