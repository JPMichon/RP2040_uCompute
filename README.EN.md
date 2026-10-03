# 🚀 RP2040 uCompute

## [Version française disponible ici](./README.md)<br>


The **RP2040 uCompute** is an autonomous, highly modular embedded development platform based on **the Raspberry Pi Pico** RP2040 microcontroller. Designed as an all-in-one hardware solution, it integrates expanded storage, versatile display interfaces, and an ecosystem of interchangeable daughterboards (Ethernet, WiFi, Radio, VGA), making it ideal for complex embedded projects, network prototyping, and learning.
The board offers a dual software approach: it can be programmed and used exactly like a classic Raspberry Pi Pico, or run the GUI (uComputeOS) designed for this platform. This mini-operating system written in MicroPython features an interactive graphical interface to explore, copy, and dynamically execute scripts stored in the QFlash memory or on the Micro SD card.

<img width="778" height="350" alt="image" src="https://github.com/user-attachments/assets/68046cc3-ce54-43ec-a8df-1a742f71edf1" />

---

## 🛠️ Technical Specifications & Dimensions

• **Microcontroller:** Raspberry Pi RP2040 clocked at 125 MHz (12 MHz external crystal oscillator).
• **PCB Dimensions:** 96 mm x 42 mm. Compact elongated form factor with 4 M3 mounting holes at the four corners.
• **QSPI Flash Memory:** Up to 16Mb depending on the memory module soldered on U2.
• **Non-volatile Storage:** CAT24Cxx I2C EEPROM.
• **Power & Safety:** Modern USB-C connector protected by a 500 mA resettable fuse and anti-backflow diodes (MBR120LSFT and 1N5819) to secure the dual power supply (USB + Neopixel).
• User Interfaces:
	• 3 user push-buttons (BTN1, BTN2, BTN3).
	• Dedicated system buttons RESET and BOOT (low-profile slide switch design).
	• White silkscreen annotation area labeled "Flash:" to write down the firmware version or memory capacity.
	• RX/TX activity status LEDs and GP25 system LED.
• **Audio & Lighting:** A piezoelectric buzzer (4000 Hz) and a connector for an addressable NEOPIXEL LED strip.
• **Removable Storage:** Micro SD card reader (TF Card) wired on the SPI bus.

---

## ⏳ Revision History & Pinout

| Feature | Version 1.2 (Sept 2025) | Version 1.3 (Dec 2025) |
| :--- | :--- | :--- |
| **USB** | Micro-USB | **USB-C** |
| **Display** | ST7789 LCD only | **ST7789 or SSD1306 OLED** |
| **Header IOs (H1)** | 3V3 + 4 Digital IO, 2 ADC + UART | **3V3, 5V + 6 Digital IO, 2 ADC + UART** |

### Header IOs (H1) :
The H1 Header facilitates prototyping. The standard 2.54 mm spacing allows it to be plugged into a prototyping board (Protoboard) or connected using jumper wires with Dupont connectors to link your circuits or modules.

### Header (H1) Pinouts
1. **5V** (Direct power from USB, ideal for power applications)
2. **3.3V** (Regulated via the AMS1117-3.3)
3. **GND** (Common ground)
4. **UART 0** : `GP0` (TX) & `GP1` (RX)
5. **2 Analog Inputs (ADC) :** `GP27` (ADC1) & `GP28` (ADC2)
6. **6 Digital Pins (GPIO): :** `GP16`, `GP17`, `GP18`, `GP19`, `GP22`, `GP24`

> [!CAUTION]
> **The RP2040 is not 5V tolerant.** 
>  According to the *Absolute Maximum Ratings* section of the official [RP2040 Datasheet](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf), the absolute maximum voltage on the I/O pins (`IOVDD`) is **3.63V**. Applying 5V directly will destroy the microcontroller.
<BR>

## 🔌 Alternative 5V Power Supply

The most common way to power the circuit is via the USB connector. However, it is possible to power the board with **5V** from **pin 1** of the Neopixel connector or via **pin 1** of the expansion header. Diode **D1** protects the USB port from reverse current, but it is always best to disconnect the external **5V** power supply if you connect the board to a computer.

> [!WARNING]
> The absolute Vin of the AP2114H-3.3TRG1 regulator is 6.5V, so **Max 5.5V**.
> 
<img width="571" height="271" alt="image" src="https://github.com/user-attachments/assets/c3ac5b20-0def-4023-9256-9ab2067576d6" />

---

## 📍 Port Mapping

Here is the exact software assignment of the RP2040 pins defined for the platform:

| Peripheral / Function | RP2040 Pin | Role & Configuration |
| :--- | :--- | :--- |
| **System LED** | `GP25` | Status indicator |
| **Buzzer** | `GP11` | Audio output (Piezo via PWM) |
| **NeoPixel Port** | `GP23` | WS2812 data output (8 LEDs by default) |
| **User Buttons** | `GP26` | Analog input (ADC0) with voltage divider |
| **UART 0** | `GP0` (TX) / `GP1` (RX) | Default serial link (9600 baud) |
| **I2C 0 (EEPROM / SSD1306)** | `GP20` (SDA) / `GP21` (SCL) | Shared I2C bus (EEPROM Address: `0x50`) |
| **ST7789 LCD Screen (SPI 0)** | `GP2` (SCK) / `GP3` (MOSI) <br> `GP4` (Reset) / `GP5` (DC) / `GP6` (BL) | Main screen and backlight control |
| **SPI 1 Bus (Shared)** | `GP14` (SCK) / `GP15` (MOSI) / `GP12` (MISO) | Data bus for SD card and expansion port |
| **Micro SD Card** | `GP13` (CS) / `GP7` (Detect) | SPI selection and hardware card detection |
| **Expansion Port (Addon)** | `GP8` (CS) / `GP10` (Reset) / `GP9` (INT) | Dedicated control pins for communication modules |
| **Side Header (H1)** | `GP16, 17, 18, 19, 22, 24, 27, 28` | General expansion pins (GPIO / ADC1 / ADC2) |

---

## 🔌 Extension Modules Ecosystem (Add-ons)

The dual-row rear socket and the front display connector form a standardized expansion port, allowing the hardware to be tailored to the target application.

### 1. Communication Modules (Rear Socket)
The mechanical and electrical footprint is compatible with several interchangeable technologies:

<img width="221" height="288" alt="image" src="https://github.com/user-attachments/assets/b017c095-deda-49ad-ae25-3661ce4e3009" /><br>
 **Ethernet Module (W5500):** Provides a stable wired network connectivity over SPI. (requires a special firmware)
  
 **WiFi Module (ESP-12F):** Adapter board embedding an ESP8266 module to add Wi-Fi connectivity.<br>
<img width="203" height="266" alt="image" src="https://github.com/user-attachments/assets/f0c80621-1b07-46e6-844b-4594e3d338f9" /><br>

**Radio Module (NRF24L01 - GT-24 Mini.MK1):** Adapter equipped with a 2x4-pin female connector for low-power, point-to-point radio communications (2.4 GHz).<br>
<img width="226" height="277" alt="image" src="https://github.com/user-attachments/assets/a6a0a83b-80ed-4dbc-bc28-06579f64b54c" />

---

### 2. Display & Video Module (Front Socket)
* **µCompute VGA8 Adaptor (REV 1.0):** Connects in place of the ST7789 LCD screen to generate and export an analog video signal to a standard monitor via a **VGA (DE-15)** port.
<img width="343" height="292" alt="image" src="https://github.com/user-attachments/assets/a070a613-6fbb-4731-9103-bb9ae0ae5e83" />

---

## 🎓 Accessibility & Compatibility with the Raspberry Pi Pico

If you are new to programming or electronics, don't be intimidated! Although the **RP2040 uCompute** integrates many components on a single printed circuit board (VGA, Wi-Fi, MicroSD, etc.), **its core remains a standard Raspberry Pi Pico**. 

There are actually **very few fundamental differences** between this board and a classic Pi Pico:
* **Same chip:** The main microcontroller is the RP2040. Any code written for a standard Pico will work here.
* **Same basics:** The programming logic, pin usage (GPIO), and development environment remain identical.

### 📚 Resources for Beginners

Since the architecture is the same, you can fully use the official guides, tutorials, and documentation from the Raspberry Pi Foundation to learn how to program your **RP2040 uCompute**. 

To take your first steps, I highly recommend the official guide: <br>
👉 **[Getting started with the Raspberry Pi Pico (Raspberry Pi Projects)](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)**

This guide will teach you step-by-step how to:
1. Install and configure the **Thonny** development environment.
2. Connect your board to your computer and install the **MicroPython** firmware.
3. Write your first scripts to control inputs and outputs.

Once you understand the basics of blinking an LED or reading a button using this guide, the **RP2040 uCompute** ecosystem and its test scripts (`testcode/`) will allow you to go much further (graphical display, sound, games, and networking) without changing your workflow!


## 💾 Software Section: uComputeOS

The board runs **uComputeOS**, a mini embedded operating system written in MicroPython.

### Hardware dependencies to include (`lib/` folder):
* **LCD Screen Version:** `st7789py.py`, `framebuf2.py`, `vga1_8x8.py`, `vga2_bold_16x16.py`
* **OLED Screen Version:** `ssd1306.py`
* **Common Storage:** `sdcard.py`

### Major features of uComputeOS:
1. **Splash Screen:** Displays system information (`os.uname`), firmware version, as well as total and free Flash space calculated live.
2. **File Manager (FileManager):** Dynamically detects at boot if a Micro SD card is present. The user selects their root storage space (`FLASH` or `SD`).
3. **Navigation & Selection:** Visual interface navigable using the analog button (`Up`, `Down`, `Select`). A triangle-shaped cursor points to the selected script.
4. **Dynamic Execution (`EXEC`):** Allows opening any user `.py` file present on the storage medium and executing it on the fly. In case of a code error, uComputeOS captures the exception and displays a red error screen without crashing the board.
5. **Inter-Storage Copying (`CP>SD` / `CP>\`):** Integrates a block-based copy function (512 bytes) allowing scripts to be transferred from the internal Flash memory to the SD card (and vice versa) directly from the hardware interface.

### ⚙️ Automatic Execution at Boot (Configuration in `main.py`)

For the graphical interface (**uComputeOS**) to launch automatically upon powering up the board without requiring a computer, you must register it as the main script:

1. **Select the version** of the code corresponding to your hardware configuration (ST7789 LCD Screen Version or SSD1306 OLED Screen Version).
2. **Rename the chosen file** to **`main.py`**.
3. **Transfer it to the root** of the RP2040's internal Flash memory (and not in the `lib/` folder) using your IDE (such as Thonny).
4. **Ensure** that all required dependencies (`sdcard.py`, screen drivers, and fonts) are present in the `/lib` folder of the internal memory.

On the next reboot or power cycle, the MicroPython firmware will natively look for the `main.py` file and instantly boot the GUI on the screen.

---

## 📜 License

The hardware (design files, schematics, layouts) and software of this project are made available under the terms of the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

❌ **Commercial use of this project (reselling bare PCBs, kits, or assembled retroPico boards) is strictly prohibited without prior authorization from the author.**

Check the [LICENSE](LICENSE) file to read the full terms.

## ☕ Support the Project

If you appreciate my work and would like to buy me a coffee to support my future soldering and coding projects on a voluntary basis, you can leave me a tip on Ko-fi. It is entirely optional and greatly appreciated!
