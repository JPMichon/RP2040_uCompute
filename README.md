# :computer: RP2040 uCompute

## [English version available here](./README.EN.md)


Le **RP2040 uCompute** est une plateforme de développement embarquée, autonome et hautement modulaire basée sur le microcontrôleur **Raspberry Pi Pico RP2040**. Conçue comme une solution matérielle tout-en-un, elle intègre un stockage étendu, des interfaces d'affichage polyvalentes ainsi qu'un écosystème de cartes filles interchangeables (Ethernet, WiFi, Radio, VGA), la rendant idéale pour les projets embarqués complexes, le prototypage réseau et l'apprentissage.

La carte offre une double approche logicielle : elle peut être programmée et utilisée exactement comme un Raspberry Pi Pico classique, ou utiliser le GUI (uComputeOS) conçu pour cette plateforme. Ce mini-système d'exploitation écrit en MicroPython offre une interface graphique interactive pour explorer, copier et exécuter dynamiquement des scripts stockés dans la mémoire QFlash ou sur la carte Micro SD.

<img width="778" height="350" alt="image" src="https://github.com/user-attachments/assets/68046cc3-ce54-43ec-a8df-1a742f71edf1" />

---

# 🤖 Assistants de Codage IA

Si vous utilisez un agent IA (comme ChatGPT, Claude ou GitHub Copilot) pour vous aider à développer sur la RP2040 uCompute, configurez-le instantanément en lui copiant-collant l'un de nos profils personnalisés. L'IA connaîtra immédiatement toutes les définitions de broches et les adresses exactes de la carte pour coder sans faire d'erreurs matérielles !

💼 **[Mode Développeur Freelance de la RP2040 uCompute](RP2040_UCompute_FreelanceCoder.md)** Conçu pour l'efficacité et la vitesse. L'IA se comporte comme un programmeur senior à votre service : vous lui exposez votre concept ou votre cahier des charges, et elle vous livre un script complet, optimisé et immédiatement prêt à être copié-collé.

---

## 🛠️ Spécifications Techniques & Dimensions

* **Microcontrôleur :** Raspberry Pi RP2040 cadencé à 125 MHz (horloge externe par quartz de 12 MHz).
* **Dimensions du PCB :** 96 mm x 42 mm. Format compact allongé avec 4 trous de montage M3 aux quatre coins.
* **Mémoire Flash QSPI :** (2meg - 16meg) en fonction de la puce.
* **Stockage non volatile :** EEPROM I2C `CAT24Cxx` 
* **Alimentation:** USB-C et Fusible PTC (500ma)
* **Interfaces utilisateur :** 
  * 3 boutons-poussoirs utilisateurs (BTN1, BTN2, BTN3).
  * Boutons système dédiés `RESET` et `BOOT` (format glissière profilé).
  * Zone d'annotation sérigraphiée blanche "Flash :" pour inscrire la version du firmware ou la capacité mémoire.
  * LEDs d'état d'activité RX/TX et LED système `GP25`.
* **Audio & Éclairage :** Un buzzer piézoélectrique (4000 Hz) et un connecteur pour ruban de LEDs adressables `NEOPIXEL`.
* **Stockage amovible :** Lecteur de carte Micro SD (TF Card) câblé sur bus SPI.

---

## ⏳ Historique des Révisions

La carte a évolué pour moderniser sa connectique et offrir une flexibilité d'affichage maximale.

| Caractéristique | 🔴 Version 1.2 (Septembre 2025) | 🟣 Version 1.3 (Décembre 2025) |
| :--- | :--- | :--- |
| **Connecteur USB** | **Micro-USB** | **USB-C** |
| **Option d'Affichage** | Écran LCD IPS ST7789 uniquement | **Double option :** ST7789 (SPI) ou OLED SSD1306 (I2C) |
| **Bornier IOs (H1)** | 3V3 + 4 Digital IO, 2 ADC + UART | **3V3, 5V + 6 Digital IO, 2 ADC + UART** |

### Le bornier ( 1x14 pins Header):
Le bornier (pins Header) facilite le prototypage. l'espacement est standard a 2,54 mm ceci permet de l'enficher dans un carte de prototypage (Protoboard) ou des cables de liaison (jumper wires) avec embouts *Dupont* afin de relier vos circuits ou modules.

### Alimentations et signaux:
1. **5V** (Alimentation directe issue de l'USB, idéale pour la puissance)
2. **3.3V** (Régulée via l'AP2114H-3.3TRG1)
3. **GND** (Masse commune)
4. **UART 0** : `GP0` (TX) & `GP1` (RX)
5. **2 Entrées Analogiques (ADC) :** `GP27` (ADC1) & `GP28` (ADC2)
6. **6 Broches Numériques (GPIO) :** `GP16`, `GP17`, `GP18`, `GP19`, `GP22`, `GP24`

<BR>

> [!CAUTION]
> **Le RP2040 n'est pas tolérant au 5V.** 
> Selon la section *Absolute Maximum Ratings* de la [fiche technique officielle du RP2040 (Datasheet)](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf), la tension maximale absolue sur les broches d'E/S (`IOVDD`) est de **3,63V**. L'application directe de 5V détruira le microcontrôleur.
<BR>

## 🔌 Alimentation Alternative en 5v

La façon la plus usuelle est d'alimenter le circuit via le connecteur USB. Néanmoins, il est possible d'alimenter le circuit en **5V** à partir de la **broche 1** du connecteur Neopixel ou via la **pin 1** du bornier d'extension. La diode **D1** protège le port USB du retour de courant, mais il est toujours préférable de couper l'alimentation **5V** externe si vous raccordez le circuit à un ordinateur.

> [!WARNING]
> Le Vin absolu du régulateur AP2114H-3.3TRG1 est de 6.5v, Donc **Max 5.5v**.

<img width="571" height="271" alt="image" src="https://github.com/user-attachments/assets/c3ac5b20-0def-4023-9256-9ab2067576d6" />


---

## 📍 Cartographie des ports

Voici l'attribution logicielle exacte des broches du RP2040 définie pour la plateforme :

| Périphérique / Fonction | Broche RP2040 | Rôle & Configuration |
| :--- | :--- | :--- |
| **LED Système** | `GP25` | Indicateur d'état |
| **Buzzer** | `GP11` | Sortie audio (Piezo via PWM) |
| **Port NeoPixel** | `GP23` | Sortie données WS2812 (8 LEDs par défaut) |
| **Boutons Utilisateurs** | `GP26` | Entrée analogique (ADC0) avec diviseur de tension |
| **UART 0** | `GP0` (TX) / `GP1` (RX) | Liaison série par défaut (9600 bauds) |
| **I2C 0 (EEPROM / SSD1306)** | `GP20` (SDA) / `GP21` (SCL) | Bus I2C partagé (Adresse EEPROM : `0x50`) |
| **Écran LCD ST7789 (SPI 0)** | `GP2` (SCK) / `GP3` (MOSI) <br> `GP4` (Reset) / `GP5` (DC) / `GP6` (BL) | Contrôle de l'écran principal et du rétroéclairage |
| **Bus SPI 1 (Partagé)** | `GP14` (SCK) / `GP15` (MOSI) / `GP12` (MISO) | Bus de données pour carte SD et port d'extension |
| **Carte Micro SD** | `GP13` (CS) / `GP7` (Detect) | Sélection SPI et détection matérielle de la carte |
| **Port d'Extension (Addon)** | `GP8` (CS) / `GP10` (Reset) / `GP9` (INT) | Broches de contrôle dédiées aux modules de communication |
| **Header latéral (H1)** | `GP16, 17, 18, 19, 22, 24, 27, 28` | Broches d'extension générales (GPIO / ADC1 / ADC2) |

---

## 🔌 Écosystème de Modules d'Extension (Add-ons)

Le socket arrière double rangée et le connecteur d'affichage avant forment un port d'extension standardisé permettant d'adapter le matériel à l'application visée.

### 1. Modules de Communication (Socket Arrière)
L'empreinte mécanique et électrique est compatible avec plusieurs technologies interchangeables :

<img width="221" height="288" alt="image" src="https://github.com/user-attachments/assets/b017c095-deda-49ad-ae25-3661ce4e3009" /><br>
* **Module Ethernet (W5500) :** Apporte une connectivité réseau filaire stable en SPI. (requiert un firmware spécial)
* **Module WiFi (ESP-12F) :** Carte d'adaptation embarquant un module ESP8266 pour ajouter une connectivité Wi-Fi.
*  <img width="203" height="266" alt="image" src="https://github.com/user-attachments/assets/f0c80621-1b07-46e6-844b-4594e3d338f9" /><br>
* **Module Radio (NRF24L01 - GT-24 Mini.MK1) :** Adaptateur doté d'un connecteur 2x4 broches femelle pour liaisons radio point à point (2.4 GHz) à basse consommation.<br>
<img width="226" height="277" alt="image" src="https://github.com/user-attachments/assets/a6a0a83b-80ed-4dbc-bc28-06579f64b54c" />

---

### 2. Module d'Affichage & Vidéo (Socket Avant)
* **µCompute VGA8 Adaptor (REV 1.0) :** Se connecte à la place de l'écran LCD ST7789 pour générer et exporter un signal vidéo analogique vers un moniteur standard via un port **VGA (DE-15)**. 

<img width="343" height="292" alt="image" src="https://github.com/user-attachments/assets/a070a613-6fbb-4731-9103-bb9ae0ae5e83" />

---

## 🎓 Accessibilité & Compatibilité avec le Raspberry Pi Pico

Si vous débutez en programmation ou en électronique, ne soyez pas intimidés ! Bien que la **RP2040 uCompute** intègre de nombreux composants sur un seul circuit imprimé (VGA, Wi-Fi, MicroSD, etc.), **son cœur reste un Raspberry Pi Pico standard**. 

Il y a en réalité **très peu de différences** fondamentales entre cette carte et un Pi Pico classique :
* **Même puce :** Le microcontrôleur principal est le RP2040. Tout code écrit pour un Pico standard fonctionnera ici.
* **Mêmes bases :** La logique de programmation, l'utilisation des broches (GPIO) et l'environnement restent identiques.

### 📚 Ressources pour les débutants

Puisque l'architecture est la même, vous pouvez utiliser à 100 % les guides, tutoriels et documentations officiels de la fondation Raspberry Pi pour apprendre à programmer votre **RP2040 uCompute**. 

Pour faire vos premiers pas, je vous recommande vivement le guide officiel : <br>
👉 **[Getting started with the Raspberry Pi Pico (Raspberry Pi Projects)](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)**

Ce guide vous apprendra pas à pas à :
1. Installer et configurer l'environnement de développement **Thonny**.
2. Connecter votre carte à votre ordinateur et y installer le micrologiciel **MicroPython**.
3. Écrire vos premiers scripts pour contrôler des entrées et des sorties.

Une fois que vous aurez compris les bases du clignotement d'une LED ou de la lecture d'un bouton avec ce guide, l'écosystème de la **RP2040 uCompute** et ses scripts de test (`testcode/`) vous permettront d'aller beaucoup plus loin (affichage graphique, son, jeux et réseau) sans changer de méthode de travail !
<BR><BR>

---

## 💾 Partie Logicielle : uComputeOS

La carte exécute **uComputeOS**, un mini-système d'exploitation embarqué écrit en MicroPython. 

### Dépendances matérielles à inclure (dossier `lib/`) :
* **Version Écran LCD :** `st7789py.py`, `framebuf2.py`, `vga1_8x8.py`, `vga2_bold_16x16.py`
* **Version Écran OLED :** `ssd1306.py`
* **Stockage commun :** `sdcard.py`

### Caractéristiques majeures de uComputeOS :
1. **Écran de démarrage (Splash Screen) :** Affiche les informations systèmes (`os.uname`), la version du firmware ainsi que l'espace Flash total et libre calculé en direct.
2. **Gestionnaire de fichiers (FileManager) :** Détecte dynamiquement à l'allumage si une carte Micro SD est présente. L'utilisateur sélectionne son espace de stockage racine (`FLASH` ou `SD`).
3. **Navigation & Sélection :** Interface visuelle navigable à l'aide du bouton analogique (`Up`, `Down`, `Select`). Un curseur en forme de triangle pointe vers le script sélectionné.
4. **Exécution dynamique (`EXEC`) :** Permet d'ouvrir n'importe quel fichier `.py` utilisateur présent sur le support et de l'exécuter à la volée. En cas d'erreur de code, uComputeOS capture l'exception et affiche un écran d'erreur rouge sans faire planter la carte.
5. **Copie Inter-Stockage (`CP>SD` / `CP>\`) :** Intègre une fonction de copie par blocs (512 octets) permettant de transférer un script de la mémoire Flash interne vers la carte SD (et inversement) directement depuis l'interface matérielle.

### ⚙️ Exécution automatique au démarrage (Configuration en `main.py`)

Pour que l'interface graphique (**uComputeOS**) se lance automatiquement dès la mise sous tension de la carte sans nécessiter d'ordinateur, vous devez l'enregistrer comme script principal :

1. **Sélectionnez la version** du code correspondant à votre configuration matérielle (Version Écran LCD ST7789 ou Version Écran OLED SSD1306).
2. **Renommez le fichier** choisi en **`main.py`**.
3. **Transférez-le à la racine** de la mémoire Flash interne du RP2040 (et non dans le dossier `lib/`) à l'aide de votre IDE (comme Thonny).
4. **Assurez-vous** que toutes les dépendances requises (`sdcard.py`, pilotes d'écran et polices de caractères) sont bien présentes dans le dossier `/lib` de la mémoire interne. 

Au prochain redémarrage ou cycle d'alimentation, le micrologiciel MicroPython cherchera nativement le fichier `main.py` et propulsera instantanément la GUI à l'écran.

---

## 📜 Licence

Le matériel (fichiers de conception, schémas, typons) et les logiciels de ce projet sont mis à disposition selon les termes de la Licence **Creative Commons Attribution - Pas d'Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International (CC BY-NC-SA 4.0)**.

❌ **L'utilisation commerciale de ce projet (revente de PCBs nus, kits ou cartes retroPico assemblées) est strictement interdite sans autorisation préalable de l'auteur.**

Consultez le fichier [LICENSE](LICENSE) pour lire l'intégralité des termes.

---

## ☕ Soutenir le projet

Si vous appréciez mon travail et souhaitez m'offrir un café pour me soutenir bénévolement dans mes futurs projets de soudure et de code, vous pouvez me laisser un pourboire sur Ko-fi. C'est entièrement volontaire et grandement apprécié !
			


