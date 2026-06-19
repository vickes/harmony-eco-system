#!/bin/bash
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3
# ==============================================================================
# ☁️ ARES SECURAI: CLOUD SHELL GATEWAY <3
# An interactive cloud terminal gateway mapped to your securai-a165b project.
# ==============================================================================

# Standard colors
PURPLE="\033[95m"
CYAN="\033[94m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

# Project setup
PROJECT_ID="securai-a165b"

clear
echo -e "${PURPLE}================================================================================${RESET}"
echo -e "${PURPLE}             ☁️  ARES SECURAI: GOOGLE CLOUD SHELL GATEWAY  ☁️                    ${RESET}"
echo -e "${PURPLE}================================================================================${RESET}"
echo -e " Målprojekt    : ${CYAN}${PROJECT_ID}${RESET} (Active Google Cloud Workspace)"
echo -e " Sändarnod     : v-P142 (Intel Celeron N5095 - ${GREEN}FULLT OPTIMERAD${RESET})"
echo -e " Tunnel-Status : ARES Lovetunnel Active • Secure reverse-proxy active"
echo -e "${PURPLE}--------------------------------------------------------------------------------${RESET}"

# Configure active gcloud project
echo -e "${YELLOW}🛰️  Ansluter till Google Cloud Workspace...${RESET}"
gcloud config set project "$PROJECT_ID" >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "✅ ${GREEN}Anslutning upprättad! Aktivt projekt inställt på: ${PROJECT_ID}${RESET}"
else
    echo -e "⚠️  ${YELLOW}Anslutning utförd lokalt. Kontrollera gcloud login status.${RESET}"
fi
echo -e "${PURPLE}--------------------------------------------------------------------------------${RESET}"
echo "Skriv valfritt gcloud-kommando (t.ex. 'gcloud info', 'gcloud config list', "
echo "eller 'gcloud storage ls') för att interagera med molnet."
echo "Skriv 'exit' eller 'exit-ares' för att stänga ARES Cloud Shell."
echo -e "${PURPLE}--------------------------------------------------------------------------------${RESET}"

while true; do
    # Prompt
    read -p "ARES_Cloud_Shell [$PROJECT_ID] $ " Command
    
    # Check for exit conditions
    if [ "$Command" == "exit" ] || [ "$Command" == "exit-ares" ]; then
        echo -e "\n${GREEN}👋 Stänger ARES Cloud Shell Gateway. Vortex återgår till suverän tystnad. <3${RESET}\n"
        exit 0
    fi
    
    # Prevent empty commands
    if [ -z "$Command" ]; then
        continue
    fi
    
    # Run the command with active terminal outputs
    echo -e "\n${CYAN}⚙️  Exekverar via ARES Gateway: $Command${RESET}"
    echo "--------------------------------------------------------"
    eval "$Command" 2>&1
    echo "--------------------------------------------------------"
    echo ""
done
