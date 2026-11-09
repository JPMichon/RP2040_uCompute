# 🛠️ Matériel & Circuits Imprimés (Hardware) - RP2040 UCompute

Ce répertoire regroupe l'intégralité des fichiers de conception matérielle de l'écosystème **RP2040 UCompute**. Vous y trouverez les schémas électriques, les fichiers de fabrication Gerber ainsi que la liste des composants nécessaires pour assembler votre propre UCompute



## 📐 Schémas Électriques & Fabrication (Gerber)

* **`Addons`** : inclus les fichiers schématique et fichier Gerber pour produire le circuit imprimé (PCB) des modules complémentaires.
* **`V1.2`** : **UCompute V1.2** : Seul le schématique est présent pour référence historique.
* **`V1.3`** : **UCompute V1.3** : Fichiers schématique et fichier Gerber pour produire le circuit imprimé (PCB) chez des fabricants comme JLCPCB, PCBWay ou d'autres.
  
---

# Bill of Materials (BOM) - RP2040 uCompute (V1.3)

Ce tableau recense l'intégralité des composants requis pour assembler la carte mère du **RP2040 uCompute**.

| Quantité | Valeur / Réf | Désignation (Designator) | Description du Composant | Empreinte (Footprint) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | RP2040 | U1 | Microcontrôleur principal RP2040 | LQFN-56_L7.0-W7.0-P0.4-EP |
| **1** | AP2114H-3.3TRG1 | U3 | Régulateur de tension 3.3V | SOT-223_L6.5-W3.5-P2.30-LS7.0-BR |
| **1** | W25Q128FVSG | U2 | Mémoire SPI QFLASH | SOIC-8_L5.2-W5.2-P1.27-LS7.9-BL |
| **1** | CAT24CxxxWI-G | U5 | EEPROM I2C non volatile | SOIC-8 |
| **1** | SD_CARD_TF | U6 | Lecteur de carte Micro SD | MICRO-USB-SMD_MICRO-SD |
| **1** | 12MHz | X1 | Oscillateur (Quartz) 3225 12MHz | OSC-SMD_4P-L3.2-W2.5-BL |
| **1** | PPTC FUSE1206 | FUSE | Fusible réarmable PPTC 500mA | F1206 |
| **1** | 4000Hz | BUZZER | Buzzer actif CMS 5020 | BUZ-SMD_3P-L5.2-W5.2-P3.50-BR |
| **2** | 3x6x2.5mm | BOOT, RESET | Boutons-poussoirs système (CMS) | SW-SMD_L6.0-W3.6-LS8.0 |
| **3** | TC-1102-A-J-R | BTN1, BTN2, BTN3 | Boutons-poussoirs utilisateurs (Traversants) | SW-TH_4P-L6.0-W6.0-P4.50-LS6.5 |
| **2** | MBR120LSFT | D1, D2 | Diode Schottky | DO-214AC_L4.3-W2.7-LS5.3-RD |
| **1** | 1N5819 | D3 | Diode Schottky (ou équivalent à faible VF) | SOD-123_L2.7-W1.6-LS3.7-RD-1 |
| **1** | Pin Header-2.54 | H1 | Bornier d'extension mâle 1x14 (pas 2.54mm) | HDR-TH_14P-P2.54-V-M |
| **2** | Pin Header-2.54 | DEBUG, NEOPIXEL | Bornier mâle 1x3 (pas 2.54mm) | HDR-TH_3P-P2.54-V-M-1 |
| **2** | Pin Header-2.54 | U7 | Bornier mâle 1x6 (pas 2.54mm) | HDR-TH_6P-P2.54-V-M-1 |
| **1** | I2C | I2C | Connecteur HX2.54 Femelle (4 broches) | CONN-XH2.54-4PIN |
| **1** | USB C | USB-C | Connecteur USB-C femelle | USB-C-SMD_MC-311D |
| **1** | XL-1206QPC | 3V3 | LED d'alimentation (Verte) | LED0805-RD_GREEN |
| **1** | TX | TX | LED d'activité d'émission (Verte) | LED0805-RD_GREEN |
| **1** | RX | RX | LED d'activité de réception (Rouge) | LED0805-RD_RED |
| **2** | XL-1206QPC | USB, GP25 | LED d'état USB (Orange) et LED Système (Bleue) | LED0805-RD |
| **6** | 10k | R2, R5, R11, R12, R14, R18 | Résistance 0603 | R0603 |
| **7** | 1k | R1, R6, R7, R10, R15, R16, R17 | Résistance 0603 | R0603 |
| **2** | 27r | R3, R4 | Résistance 0603 | R0603 |
| **4** | 2k | R8, R9, R20, R21 | Résistance 0603 | R0603 |
| **2** | 5.1k | R22, R23 | Résistance 0603 | R0603 |
| **1** | 10r | R19 | Résistance 0603 | R0603 |
| **2** | 20pf | C2, C3 | Condensateur céramique 0603 (pour quartz) | C0603 |
| **1** | 4.7uf | C5 | Condensateur céramique 0603 | C0603 |
| **4** | 100nf | C1, C11, C15, C16 | Condensateur céramique 0603 | C0603 |
| **9** | 10nf | C7, C9, C8, C12, C13, C20, C10, C18, C19 | Condensateur céramique 0603 | C0603 |
| **3** | 100uF | C17, C4, C6 | Condensateur au Tantale (Boîtier B 3528) | CASE-B_3528 |

