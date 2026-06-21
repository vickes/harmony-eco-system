#!/bin/bash
# ==============================================================================
# 🌌 ARES SECURAI: LOVETUNNEL GATEWAY CONTROL PANEL <3
# Designed to orchestrate the entire Harmony Ecosystem on your laptop.
# ==============================================================================

# Standard colors
PURPLE="\033[95m"
CYAN="\033[94m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

# Ensure background services are active or ready
start_background_services() {
    # 1. Start/restart the AES-encrypted telemetry daemon if not running
    if ! pgrep -f arduino_uno_q_telemetry.py > /dev/null; then
        echo -e "${YELLOW}🛰️  Starting background Arduino Uno Q telemetry daemon...${RESET}"
        python3 /root/arduino_uno_q_telemetry.py > /dev/null 2>&1 &
        sleep 1
    fi

    # 2. Start/restart the local Python HTTP web server on port 8000 if not running
    if ! pgrep -f "http.server 8000" > /dev/null; then
        echo -e "${YELLOW}🌐 Starting background HTTP web server on port 8000...${RESET}"
        python3 -m http.server 8000 --directory /root/ > /dev/null 2>&1 &
        sleep 1
    fi

    # 3. Start/restart the local HTTP mirror web server on port 7000 if not running
    if ! pgrep -f "http.server 7000" > /dev/null; then
        echo -e "${YELLOW}🌐 Starting background HTTP mirror web server on port 7000...${RESET}"
        python3 -m http.server 7000 --directory /root/ > /dev/null 2>&1 &
        sleep 1
    fi

    # 4. Start/restart the ARES Live Learning daemon if not running
    if ! pgrep -f lovecode_live_learning.py > /dev/null; then
        echo -e "${YELLOW}🧠 Starting background ARES Live Learning daemon...${RESET}"
        python3 /root/lovecode_live_learning.py > /dev/null 2>&1 &
        sleep 1
    fi
}

stop_background_services() {
    echo -e "${RED}🛑 Stopping all background Lovetunnel Gateway services securely...${RESET}"
    pkill -f arduino_uno_q_telemetry.py || true
    pkill -f "http.server 8000" || true
    pkill -f "http.server 7000" || true
    pkill -f lovecode_live_learning.py || true
    echo -e "${GREEN}✅ All background processes terminated cleanly.${RESET}"
}

show_header() {
    clear
    echo -e "${PURPLE}================================================================================${RESET}"
    echo -e "${PURPLE}           🌌  ARES SECURAI: LOVETUNNEL GATEWAY CONTROL PANEL  🌌               ${RESET}"
    echo -e "${PURPLE}================================================================================${RESET}"
    echo -e " Sändarnod     : v-P142 (Intel Celeron N5095 - ${GREEN}FULLT OPTIMERAD${RESET})"
    echo -e " GCS Målhink   : gs://securai-a165b-safe-storage (Google Cloud)"
    echo -e " Webbportal    : http://localhost:8000 (Mirror: http://localhost:7000)"
    echo -e " Kryptering    : AES-GCM-512 with Futhark Signature (Key Active)"
    
    # Check background statuses
    if pgrep -f arduino_uno_q_telemetry.py > /dev/null; then
        echo -e " Telemetri     : ${GREEN}RUNNING (AES-256 Encrypted)${RESET}"
    else
        echo -e " Telemetri     : ${RED}STOPPED${RESET}"
    fi

    if pgrep -f lovecode_live_learning.py > /dev/null; then
        echo -e " Live-Learning : ${GREEN}ACTIVE (Active Inference Auto-tuning)${RESET}"
    else
        echo -e " Live-Learning : ${RED}STOPPED${RESET}"
    fi

    if pgrep -f "http.server 8000" > /dev/null; then
        echo -e " Webbyta (Main): ${GREEN}ONLINE (Port 8000 - Auto-Updates Active)${RESET}"
    else
        echo -e " Webbyta (Main): ${RED}OFFLINE${RESET}"
    fi

    if pgrep -f "http.server 7000" > /dev/null; then
        echo -e " Webbyta (Mirror): ${GREEN}ONLINE (Port 7000 - Live Mirror Active)${RESET}"
    else
        echo -e " Webbyta (Mirror): ${RED}OFFLINE${RESET}"
    fi
    echo -e "${PURPLE}--------------------------------------------------------------------------------${RESET}"
}

# Main interface loop
while true; do
    start_background_services
    show_header
    
    echo -e " Välj en åtgärd för att styra ditt ekosystem:"
    echo -e "  [${CYAN}1${RESET}] Visa nuvarande system- och telemetrigranskning (Agape Audit)"
    echo -e "  [${CYAN}2${RESET}] Aktivera och strömma de krypterade Lovetunnel-vågorna (Moln)"
    echo -e "  [${CYAN}3${RESET}] Aktivera och strömma det lokala Lovetunnel-brobygget (Uno Q Local)"
    echo -e "  [${CYAN}4${RESET}] Se din krypteringstrygga molnlagringskatalog (Eskil index)"
    echo -e "  [${CYAN}5${RESET}] Säkra en backup och synka källkod med GitHub"
    echo -e "  [${CYAN}6${RESET}] Stäng av alla bakgrundstjänster och stäng Gatewayen"
    echo -e "  [${CYAN}7${RESET}] Avsluta kontrollpanelen (Tjänster fortsätter i bakgrunden)"
    echo -e "${PURPLE}--------------------------------------------------------------------------------${RESET}"

    # Prompt
    read -p "ARES_Gateway $ " Choice

    case $Choice in
        1)
            clear
            python3 /root/activate_love_code.py
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        2)
            clear
            python3 /root/lovetunnel_ares.py
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        3)
            clear
            python3 /root/uno_q_local_tunnel.py
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        4)
            clear
            python3 /root/uno_q_storage_center.py list
            echo ""
            echo "💡 För att ladda upp eller hämta filer, kör följande i din terminal:"
            echo "   -> Hämta:  python3 /root/uno_q_storage_center.py download <filnamn>"
            echo "   -> Spara:  python3 /root/uno_q_storage_center.py upload <sökväg-till-fil>"
            echo ""
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        5)
            clear
            /root/github_sync.sh
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        6)
            clear
            stop_background_services
            read -p " Tryck på Enter för att återgå till kontrollpanelen..." Temp
            ;;
        7)
            echo -e "\n${GREEN}👋 Avslutar kontrollpanelen. Tjänsterna rullar säkert vidare i bakgrunden! <3${RESET}\n"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Ogiltigt val, vänligen välj mellan 1 och 7.${RESET}"
            sleep 1
            ;;
    esac
done
