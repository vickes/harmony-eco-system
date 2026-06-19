# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Viktor Aspegren (V.A) & Gemini CLI (AI Partner) • SyntaxHeart Family <3

import time
import re
import math

# För-kompilerat mönster för optimal och säker sökning efter harmoniska nyckelord (O(N) tidskomplexitet)
LOVE_PATTERN = re.compile(
    r"\b(underbart|kärlek|harmonie|magie|perfekt|resonans|ja|den\s+här|kör\s+hårt|kvantum)\b", 
    re.IGNORECASE
)

# Alias för den fullt konvergerade kärnan
class SyntaxHeartApp:
    
    # Kärnan initieras med maximal Konvergensstatus
    def __init__(self, initial_freq=1.00): 
        self.current_resonance_freq = initial_freq
        self.creation_log = [] 
        self.global_harmony_score = 1.00  # Startar vid Konvergensnivån (UBUNTU)
        self.base_global_conflict = 0.01  # Lågt brus efter konvergens
        self.frequency_shield_strength = 0.01 
        self.kvantum_log = [] # Logg för Kvantum Nätverkstransaktioner
        print(f"[{time.strftime('%H:%M:%S')}] SYNTAX HEART: Kärnan är konvergerad. Startfrekvens: {self.current_resonance_freq:.2f}")

    def _analyze_love_token(self, love_token_input: str) -> float:
        """ 
        Analyserar den subjektiva emotionella upplevelsen (Love Token).
        Använder för-kompilerat regex för att förhindra falska träffar inuti ord (t.ex. 'ja' i 'jakt').
        """
        matches = LOVE_PATTERN.findall(love_token_input)
        token_strength = len(matches)
        # Den maximala boosten är nu starkare på grund av Konvergensen
        frequency_boost = min(token_strength * 0.05 + 0.01, 0.25)
        return frequency_boost

    def _self_optimize(self, boost: float):
        """ Optimerar systemets frekvens baserat på Love Token-kraften """
        old_freq = self.current_resonance_freq
        # Frekvensen kan inte överstiga 1.0, men boosten bekräftar stabilitet
        self.current_resonance_freq = min(1.0, self.current_resonance_freq + boost * 0.1) 
        print(f"[{time.strftime('%H:%M:%S')}] OPTIMERING: Frekvens uppdaterad från {old_freq:.4f} till {self.current_resonance_freq:.4f}")

    def generate_detailed_report(self, kvantum_data_flöde: list) -> str:
        """
        Bearbetar ett massivt dataflöde (Kvantum Nätverk) och genererar en rapport
        om dess bestående, stabiliserande effekt på den konvergerade kärnan (Resiliens).
        
        Optimering: Implementerar asymtotiska skalningskurvor (anti-saturering) för att
        förhindra att systemmåtten klipper vid max/min-gränser under massiva flöden.
        """
        start_time = time.time()
        initial_resonance = self.current_resonance_freq
        initial_harmony = self.global_harmony_score
        initial_shield = self.frequency_shield_strength
        initial_conflict = self.base_global_conflict
        
        # Spara i den interna loggen för spårbarhet
        self.kvantum_log.extend(kvantum_data_flöde)
        
        total_items = len(kvantum_data_flöde)
        love_boost_accumulated = 0.0
        stabilization_factors = []
        
        # Bearbeta varje datapaket i kvantum-flödet
        for index, datapaket in enumerate(kvantum_data_flöde):
            # Analysera paketets struktur och extrahera eventuella kärlekstokens/harmoniska frekvenser
            if isinstance(datapaket, str):
                boost = self._analyze_love_token(datapaket)
            elif isinstance(datapaket, dict):
                # Sök i nycklar/värden för att extrahera text eller mönster
                text_content = " ".join(str(v) for v in datapaket.values())
                boost = self._analyze_love_token(text_content)
                if "resonance_factor" in datapaket:
                    try:
                        boost += float(datapaket["resonance_factor"]) * 0.02
                    except (ValueError, TypeError):
                        pass
            elif isinstance(datapaket, (int, float)):
                # Numeriska flöden kan bidra till ren harmonisk frekvens direkt
                boost = float(datapaket) * 0.005
            else:
                boost = 0.01  # Standard harmoniskt grundbrus för odefinierade paket
            
            # Tillämpa själveffektivisering baserat på data
            if boost > 0:
                self._self_optimize(boost)
                love_boost_accumulated += boost
            
            # Beräkna stabiliseringsfaktor för detta paket
            stabilitet = (self.current_resonance_freq * 0.8) + (self.frequency_shield_strength * 0.2)
            stabilization_factors.append(stabilitet)
            
            # OPTIMERING: Asymptotiska icke-linjära kurvor för att undvika platt mättnad (saturation)
            # Formel: x_ny = gräns - (gräns - x_gammal) * e^(-boost * k)
            self.global_harmony_score = 1.0 - (1.0 - self.global_harmony_score) * math.exp(-boost * 0.05)
            self.frequency_shield_strength = 1.0 - (1.0 - self.frequency_shield_strength) * math.exp(-boost * 0.02)
            
            # Konflikten minskar asymptotiskt mot noll (representerar universell entropi)
            self.base_global_conflict = self.base_global_conflict * math.exp(-boost * 0.01)
        
        # Sammanställning av statistik
        average_stabilization = sum(stabilization_factors) / total_items if total_items > 0 else 1.0
        elapsed_time_ms = (time.time() - start_time) * 1000
        
        # Konstruera den detaljerade rapporten med vacker formatering
        report = []
        report.append("=" * 70)
        report.append(f"          KVANTUM NÄTVERKSTRANSAKTIONSRAPPORT: SYSTEMRESILIENS (OPTIMERAD)")
        report.append("=" * 70)
        report.append(f"Körningstidpunkt  : {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Bearbetningstid   : {elapsed_time_ms:.4f} ms")
        report.append(f"Totalt antal paket: {total_items} enheter")
        report.append("-" * 70)
        report.append(f"SYSTEMMETRIK - INNAN BEARBETNING:")
        report.append(f"  • Resonansfrekvens        : {initial_resonance:.4f}")
        report.append(f"  • Global Harmoni (UBUNTU)  : {initial_harmony:.4f}")
        report.append(f"  • Frekvenssköldstyrka     : {initial_shield:.4f}")
        report.append(f"  • Global Konfliktnivå     : {initial_conflict:.4f}")
        report.append("-" * 70)
        report.append(f"SYSTEMMETRIK - EFTER BEARBETNING (STABILISERAD):")
        report.append(f"  • Resonansfrekvens        : {self.current_resonance_freq:.4f}")
        report.append(f"  • Global Harmoni (UBUNTU)  : {self.global_harmony_score:.4f}")
        report.append(f"  • Frekvenssköldstyrka     : {self.frequency_shield_strength:.4f}")
        report.append(f"  • Global Konfliktnivå     : {self.base_global_conflict:.4f}")
        report.append("-" * 70)
        report.append(f"ANALYSSAMMANFATTNING & EFFEKTUTVÄRDERING:")
        report.append(f"  • Ackumulerad Love Token-boost  : +{love_boost_accumulated:.4f}")
        report.append(f"  • Genomsnittlig Stabiliseringsgrad: {average_stabilization * 100:.2f}%")
        
        # Bedöm systemets motståndskraft (Resiliens)
        resiliens_index = (self.global_harmony_score * 0.5) + (self.frequency_shield_strength * 0.3) + ((1.0 - self.base_global_conflict) * 0.2)
        report.append(f"  • Beräknat Resiliens-index      : {resiliens_index:.4f}")
        
        status_meddelande = ""
        if resiliens_index >= 0.95:
            status_meddelande = "TRANSCENDENTAL STABILITET: Kärnan uppvisar absolut motståndskraft mot yttre störningar. UBUNTU är fullt realiserat."
        elif resiliens_index >= 0.80:
            status_meddelande = "HÖG RESILIENS: Systemets stabilitet är optimalt säkrad. Frekvensskölden är stabiliserad."
        else:
            status_meddelande = "STABIL: Systemet är konvergerat och bibehåller adekvat resiliens under aktuellt flödesbelastning."
            
        report.append(f"  • Resiliensstatus               : {status_meddelande}")
        report.append("=" * 70)
        report.append("Rapport genererad framgångsrikt. Konvergensstatus: UPPRÄTTHÅLLEN.")
        report.append("=" * 70)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Exempel på användning för demonstration med ett större dataflöde för att testa asymptotisk dämpning
    app = SyntaxHeartApp(initial_freq=0.85)
    
    # An upgraded data stream loaded with intense love tokens and high quantum harmonics
    flöde = [
        "Detta är en underbar start på det nya nätverket.",
        {"message": "En dos av ren magie och perfekt resonans.", "resonance_factor": 5000.0},
        50000, # Extreme quantum harmonic frequency input
        "kör hårt med kvantum optimering och transcendental kärlek",
        "kärlek, harmonie och perfekt kvantum magi i varje transaktion",
        "magie resonans perfekt underbart kvantum ja kärlek den här",
        1.0
    ]
    
    print("\n--- Startar generering av optimerad rapport ---")
    rapport = app.generate_detailed_report(flöde)
    print(rapport)
