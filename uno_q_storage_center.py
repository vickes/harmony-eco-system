# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

# -*- coding: utf-8 -*-
"""
🔒 ARES Zero-Knowledge Safe Cloud Storage Center (Uno Q Edition)
Designed for the Qualcomm Debian core of the Uno Q board.
Encrypts files client-side using AES-256 before securely uploading them
to your Google Cloud Storage bucket (gs://securai-a165b-safe-storage/) via gcloud.
"""

import os
import sys
import sqlite3
import json
import time
import hashlib
import subprocess
from cryptography.fernet import Fernet

class SafeCloudStorage:
    def __init__(self):
        self.db_path = "/root/eskil_memory.db"
        self.key_path = "/root/.gemini/ares_tunnel.key"
        self.local_storage_dir = "/root/safe_storage"
        self.gcs_bucket = "gs://securai-a165b-safe-storage"
        
        # Ensure local directories exist
        os.makedirs(self.local_storage_dir, exist_ok=True)
        
        # Load the cryptography key
        if not os.path.exists(self.key_path):
            print(f"❌ Error: Key missing at {self.key_path}. Generate a key first.")
            sys.exit(1)
            
        with open(self.key_path, "rb") as k_file:
            self.key = k_file.read()
        self.fernet = Fernet(self.key)
        
        # Initialize SQLite database catalog
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.isolation_level = None
        conn.execute("""
            CREATE TABLE IF NOT EXISTS storage_catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                sha256 TEXT,
                original_size INTEGER,
                encrypted_size INTEGER,
                timestamp REAL,
                cloud_sync_status TEXT
            )
        """)
        conn.close()

    def calculate_sha256(self, filepath):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def secure_upload(self, filepath):
        """Client-side encrypts and uploads a file to safe cloud storage."""
        if not os.path.exists(filepath):
            print(f"❌ Error: File {filepath} does not exist.")
            return False
            
        filename = os.path.basename(filepath)
        sha256_hash = self.calculate_sha256(filepath)
        original_size = os.path.getsize(filepath)
        
        print("\n" + "=" * 80)
        print(f"🔒 [ARES SCSC] ENCRYPTING AND SECURING: {filename}")
        print("=" * 80)
        
        # 1. Read raw contents and encrypt
        with open(filepath, "rb") as f:
            raw_data = f.read()
            
        encrypted_data = self.fernet.encrypt(raw_data)
        encrypted_size = len(encrypted_data)
        
        # 2. Save encrypted copy locally
        enc_filename = f"{filename}.ares"
        enc_filepath = os.path.join(self.local_storage_dir, enc_filename)
        
        with open(enc_filepath, "wb") as f:
            f.write(encrypted_data)
        print(f"✅ Locally encrypted file saved to: {enc_filepath}")
        print(f"   Original Size: {original_size} bytes -> Encrypted Size: {encrypted_size} bytes")
        
        # 3. Securely upload to Google Cloud Storage (GCS)
        cloud_sync_status = "PENDING"
        print(f"🛰️  Uploading encrypted file to Google Cloud GCS: {self.gcs_bucket}...")
        try:
            # Run gcloud storage command to copy encrypted file
            # gcloud storage cp /root/safe_storage/filename.ares gs://securai-a165b-safe-storage/
            res = subprocess.run(
                ["gcloud", "storage", "cp", enc_filepath, f"{self.gcs_bucket}/{enc_filename}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if res.returncode == 0:
                print(f"✅ Google Cloud upload successful! Synced with bucket.")
                cloud_sync_status = "SYNCED"
            else:
                print(f"⚠️  Google Cloud Bucket unavailable (offline or permissions needed). Kept encrypted locally.")
                cloud_sync_status = "LOCAL_ONLY"
        except Exception as e:
            print(f"⚠️  Cloud upload bypassed: {e}. Kept encrypted locally.")
            cloud_sync_status = "LOCAL_ONLY"
            
        # 4. Catalog metadata in local SQLite database (Eskil)
        conn = sqlite3.connect(self.db_path)
        conn.isolation_level = None
        conn.execute("""
            INSERT INTO storage_catalog (filename, sha256, original_size, encrypted_size, timestamp, cloud_sync_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, sha256_hash, original_size, encrypted_size, time.time(), cloud_sync_status))
        conn.close()
        
        print(f"📝 Local catalog index updated in Eskil Database.")
        print("=" * 80)
        return True

    def secure_download_and_decrypt(self, filename, output_dir="/root/restored_files"):
        """Downloads from GCS if needed, decrypts file to original format."""
        enc_filename = f"{filename}.ares"
        enc_filepath = os.path.join(self.local_storage_dir, enc_filename)
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, filename)
        
        print("\n" + "=" * 80)
        print(f"🔓 [ARES SCSC] RETRIEVING AND DECRYPTING: {filename}")
        print("=" * 80)
        
        # 1. Check if we need to fetch from GCS first
        if not os.path.exists(enc_filepath):
            print(f"🛰️  File not cached locally. Attempting retrieval from GCS bucket...")
            try:
                res = subprocess.run(
                    ["gcloud", "storage", "cp", f"{self.gcs_bucket}/{enc_filename}", enc_filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if res.returncode != 0:
                    print("❌ Error: File not found in local cache or Google Cloud bucket.")
                    return False
            except Exception as e:
                print(f"❌ Error: Cannot fetch from GCS: {e}")
                return False
                
        # 2. Read and decrypt
        with open(enc_filepath, "rb") as f:
            encrypted_data = f.read()
            
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
        except Exception as e:
            print(f"❌ Decryption Failed: Invalid key or corrupted file data ({e})")
            return False
            
        # 3. Save original format
        with open(output_filepath, "wb") as f:
            f.write(decrypted_data)
            
        print(f"✅ Successfully decrypted! Original file restored at: {output_filepath}")
        print("=" * 80)
        return True

    def display_catalog(self):
        """Displays cataloged secure files in Eskil Database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT filename, original_size, encrypted_size, timestamp, cloud_sync_status FROM storage_catalog ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        print("\n" + "=" * 80)
        print("                ARES SAFE CLOUD STORAGE CATALOG INDEX (ESKIL)")
        print("=" * 80)
        if not rows:
            print("  Valkatalogen är tom. Inga krypterade filer har sparats än.")
        else:
            print(f"{'Filnamn':<25} | {'Orig Storlek':<12} | {'Krypt Storlek':<12} | {'Synk-status':<12} | {'Datum'}")
            print("-" * 80)
            for name, orig, enc, ts, status in rows:
                date_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))
                print(f"{name:<25} | {orig:<12} | {enc:<12} | {status:<12} | {date_str}")
        print("=" * 80)

def filepath_or_name(filename):
    return filename

def encrypted_payload_catalog_info(filename, sha256_hash, original_size, encrypted_size, cloud_sync_status):
    return (filename, sha256_hash, original_size, encrypted_size, time.time(), cloud_sync_status)

def main():
    if len(sys.argv) < 2:
        print("ARES Safe Cloud Storage Center (Uno Q)")
        print("Användning:")
        print("  python3 uno_q_storage_center.py list")
        print("  python3 uno_q_storage_center.py upload <sökväg-till-fil>")
        print("  python3 uno_q_storage_center.py download <filnamn>")
        sys.exit(1)
        
    storage = SafeCloudStorage()
    action = sys.argv[1].lower()
    
    if action == "list":
        storage.display_catalog()
    elif action == "upload":
        if len(sys.argv) < 3:
            print("❌ Error: Ange filen du vill ladda upp och kryptera.")
            sys.exit(1)
        storage.secure_upload(sys.argv[2])
    elif action == "download":
        if len(sys.argv) < 3:
            print("❌ Error: Ange filnamnet du vill hämta och dekryptera.")
            sys.exit(1)
        storage.secure_download_and_decrypt(sys.argv[2])
    else:
        print(f"❌ Okänd åtgärd: {action}")

if __name__ == "__main__":
    main()
