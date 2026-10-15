import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const

# --- Configuration Matérielle (uCompute / Pico Fun Board) ---
_SPI1_SCK  = 14
_SPI1_MOSI = 15
_SPI1_MISO = 12
csn = Pin(8, mode=Pin.OUT, value=1)
ce  = Pin(10, mode=Pin.OUT, value=0)

# Adresse du registre RPD (Received Power Detector)
_RPD_REG = const(0x09)

def init_scanner():
    """Initialise le module en mode écoute brute sans protocole bloquant"""
    spi = SPI(1, sck=Pin(_SPI1_SCK), mosi=Pin(_SPI1_MOSI), miso=Pin(_SPI1_MISO))
    # On utilise une taille de paquet par défaut
    nrf = NRF24L01(spi, csn, ce, channel=1, payload_size=32)
    
    # On désactive le CRC et l'Auto-Ack pour accélérer le balayage
    nrf.set_crc(0)
    nrf.auto_ack = 0
    
    # On ouvre un canal fictif pour pouvoir démarrer l'écoute
    nrf.open_rx_pipe(1, b"\x00\x00\x00\x00\x00")
    return nrf

def scan_spectrum(nrf, nb_echantillons=50):
    """Balaye les canaux et compte combien de fois un signal > -64dBm est détecté"""
    # Dictionnaire pour stocker le score d'occupation de chaque canal (0 à 125)
    # On se concentre souvent sur les canaux de 1 à 100 car au-delà on sort de la bande grand public
    canaux_a_tester = range(1, 101)
    resultats = {}

    for channel in canaux_a_tester:
        nrf.set_channel(channel)
        hits = 0
        
        # On effectue plusieurs mesures rapides sur le même canal pour capter les signaux intermittents
        for _ in range(nb_echantillons):
            nrf.start_listening()
            utime.sleep_us(130) # Temps nécessaire pour que la radio se cale sur la fréquence (Transition RX)
            
            # Lecture directe du registre RPD (bit 0) via la méthode de la bibliothèque
            # Si un signal > -64 dBm est présent, le bit passe à 1
            rpd_value = nrf.reg_read(_RPD_REG) & 0x01
            if rpd_value:
                hits += 1
                
            nrf.stop_listening()
        
        # Calcul du pourcentage d'occupation du canal
        pourcentage = int((hits / nb_echantillons) * 100)
        resultats[channel] = pourcentage

    return resultats

def afficher_graphique(spectre):
    """Affiche l'intégralité des canaux dans la console sans aucun filtre"""
    print("\n" * 2 + "=" * 45)
    print("      ANALYSE DU SPECTRE 2.4 GHz (RPD)      ")
    print("=" * 45)
    
    for channel, occupation in spectre.items():
        # Suppression du filtre 'if' : on affiche TOUT
        barre = "#" * (occupation // 4)
        print("CH {:03d} [{:3d}%] | {}".format(channel, occupation, barre))

# --- Boucle Principale ---
print("Démarrage du scanner de fréquences...")
nrf_module = init_scanner()

while True:
    # Réalise un balayage complet
    donnees_spectre = scan_spectrum(nrf_module, nb_echantillons=50)
    
    # Affiche le rendu visuel
    afficher_graphique(donnees_spectre)
    
    # Pause entre deux analyses globales
    utime.sleep(2)
