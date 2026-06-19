# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
"""
☁️ ARES API Reconstruction Gateway
Bridges and reconstructs AI requests between Google AI Gemini and Google Cloud Vertex AI.
Dynamically detects active credentials (API Key vs OAuth Bearer Token), reconstructs
payload headers, endpoints, and formats on-the-fly to ensure seamless dual-platform connectivity.
"""

import os
import sys
import json
import urllib.request
import subprocess

class APIReconstructor:
    def __init__(self):
        self.project_id = "securai-a165b"
        self.location = "us-central1"
        self.gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.vertex_endpoint = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/gemini-1.5-flash:generateContent"

    def get_oauth_token(self):
        """Attempts to dynamically fetch an active gcloud OAuth bearer token."""
        try:
            res = subprocess.run(
                ["gcloud", "auth", "print-access-token"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if res.returncode == 0:
                return res.stdout.strip()
            return None
        except Exception:
            return None

    def query_ai_reconstructed(self, prompt_text):
        """
        Dynamically detects the available authentication scheme, reconstructs
        the payload and headers, and executes the REST API call on the active endpoint.
        """
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        oauth_token = self.get_oauth_token()
        
        # 1. PATH A: If Google Cloud OAuth Token is active, reconstruct for Vertex AI
        if oauth_token:
            print("☁️  [ARES API] Reconstructing request for Google Cloud Vertex AI Platform...")
            url = self.vertex_endpoint
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {oauth_token}"
            }
            # Vertex GCS payload format reconstruction
            payload = {
                "contents": {
                    "role": "user",
                    "parts": [{"text": prompt_text}]
                }
            }
            
        # 2. PATH B: If standard Gemini API Key is present, reconstruct for Google AI
        elif api_key:
            print("☁️  [ARES API] Reconstructing request for Google AI Gemini Platform...")
            url = f"{self.gemini_endpoint}?key={api_key}"
            headers = {"Content-Type": "application/json"}
            # Standard Gemini payload format reconstruction
            payload = {
                "contents": [{
                    "parts": [{"text": prompt_text}]
                }]
            }
            
        else:
            print("❌ [ARES API] Reconstruction error: No active API Key or Gcloud OAuth Token found.")
            return "ERROR: Autentiseringsmetod saknas (API Nyckel eller Gcloud-token behövs)."

        # Execute the reconstructed REST request
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_bytes = response.read()
                res_data = json.loads(res_bytes.decode("utf-8"))
                
            # Parse text depending on reconstructed response formats
            if oauth_token:
                # Vertex AI response parsing
                text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                # Google AI response parsing
                text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                
            return text
            
        except Exception as e:
            return f"ERROR: API-rekonstruerad anslutning misslyckades ({e})"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ARES API Reconstruction Tester")
        print("Användning: python3 ares_api_gateway.py <prompt-text>")
        sys.exit(1)
        
    reconstructor = APIReconstructor()
    result = reconstructor.query_ai_reconstructed(sys.argv[1])
    print("\n--- REKONSTRUERAT SVAR ---")
    print(result)
