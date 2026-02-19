# BTF-LIGHTING SP803E — WLED ESP32 Controller Installation & Configuration
**Revision:** 2026-02-18  
**Source:** SP803E instruction manual (manuals.plus/device.report), WLED official docs (kno.wled.ge)

---

## Specifications Summary

| Parameter | Value |
|-----------|-------|
| MCU | ESP32 (dual-core, 240 MHz) |
| Input Voltage | 5V – 24V DC |
| Working Current | 30mA – 150mA (controller only) |
| SPI Output | IO16, max 2048 pixels (RGB or RGBW IC strips) |
| PWM Channels | IO25, IO26, IO27 (3 independent channels) |
| PWM Max Current | 6A per channel, 12A total |
| MIC Input | IO36, onboard analog microphone |
| Connectivity | 2.4GHz WiFi (802.11 b/g/n) |
| Interface | USB Type-C (for firmware flash and data-only cable) |
| Dimensions | 118mm × 45mm × 15mm |
| Button | Short press = on/off; Long press 1s = color cycle; Long press 10s = factory reset |
| Indicator | Green LED, solid = powered/connected |

---

## Compatible Strip Types

### SPI Addressable (connect to IO16 SPI output)
- WS2811, WS2812, WS2812B
- WS2815 (dual-signal, 12V)
- **WS2814 RGBW** ← your indoor and outdoor RGBW strips
- SK6812 RGBW
- FCOB with addressable IC (not your passive FCOB strips — see PWM below)

### PWM Dimming (connect to IO25/26/27)
- 2-pin single-color LED strips ← **your FCOB warm white strips**
- 3-pin CCT dual-white
- 4-pin RGB (non-addressable)

---

## Terminal / Connector Layout

Looking at the SP803E board:

```
┌─────────────────────────────────────┐
│  [KEY]  [LED]  [MIC]                │
│                                     │
│  Power Input: VCC+ and GND−         │
│  (also accepts 5.5/2.1mm DC barrel) │
│                                     │
│  SPI Output:  DATA  GND             │
│  PWM1-3:      PWM1  PWM2  PWM3  GND │
│                                     │
│               [USB-C]               │
└─────────────────────────────────────┘
```

> The screw terminal block has labeled positions. Match your strip's DATA (or DIN), VCC, and GND accordingly. For addressable strips, only DATA and GND go to the controller's SPI terminals — VCC comes directly from the PSU bus, not through the controller.

---

## Wiring Diagram — Your Specific Configuration

### SPI Channel: WS2814 RGBW Strips

```
LRS-200-12 PSU
  +12V ──────────────────────────────→ WS2814 V+ (pin 1 of JST-SM)
  GND  ──────────→ SP803E GND
                   SP803E SPI GND  → WS2814 GND (pin 3 of JST-SM)
                   SP803E IO16 DATA → WS2814 DATA IN (pin 2 of JST-SM)
```

**Important:** Power (12V+) to the WS2814 strip comes directly from the PSU, NOT through the SP803E. Only DATA and GND go through the SP803E. The SP803E cannot handle strip current (up to 17A) — it only passes control signals.

For long WS2814 runs, also connect the strip's DATA RETURN/BACKUP wire. WS2814 has a dual-signal architecture — see LED strip doc for details.

### PWM Channels: FCOB Warm White Strips

```
LRS-200-12 PSU
  +12V ──────────→ FCOB strip V+ (directly, heavy wire)
  GND  ──────────→ FCOB strip GND AND SP803E GND
                   SP803E IO25  →  FCOB strip Signal/DIM input
                   (IO26, IO27 for additional FCOB zones if needed)
```

The FCOB strips are constant-current (not addressable). The SP803E's PWM output acts as a dimmer signal. The strip must be connected with its signal wire to the PWM output and power directly from the PSU. Check your specific FCOB strip's wiring label — some use a 2-wire connection (V+ and V−), with the PWM signal substituting for V− (varies by wiring approach). Consult the specific strip's label.

### HC-SR501 PIR to SP803E

The ESP32 on the SP803E has accessible GPIO. Connect PIR OUT to a GPIO not used by SPI/PWM — GPIO4 or GPIO13 are commonly available:

```
HC-SR501 VCC → 3.3V or 5V (from a small LDO or the USB 5V rail on the SP803E)
HC-SR501 GND → SP803E GND
HC-SR501 OUT → SP803E GPIO (IO4 recommended)
```

> Note: HC-SR501 VCC can be 5–12V. The OUT pin outputs 3.3V logic, compatible with the ESP32. You can power the PIR from a 5V USB charger sharing GND with the SP803E, or from a small 5V regulator off the 12V PSU.

---

## Initial Setup — First Time

### Step 1: Flash / Verify Firmware
The SP803E ships with WLED pre-installed. Verify by powering it up and checking for the WLED-AP WiFi network. If the firmware is absent or corrupt:
- Visit https://install.wled.me in Chrome or Edge (Web Serial required — not Safari, not Firefox)
- Connect SP803E via USB-C using a **data cable** (not charge-only)
- Select your device and flash the latest stable WLED release

### Step 2: Connect to WLED-AP
1. Power on the SP803E (12V to VCC/GND).
2. On your phone or computer, connect to WiFi network: **WLED-AP**
3. Password: **wled1234**
4. Browser should auto-redirect to `4.3.2.1` (or go there manually).

### Step 3: Connect to Home WiFi
1. In WLED interface → ☰ menu → **WiFi Settings**
2. Enter your 2.4GHz network name (SSID) and password
3. **Must be 2.4GHz — SP803E does not support 5GHz.**
4. Save & Connect.
5. The controller reboots and joins your home network.
6. Find its new IP via your router's device list, or use the WLED app's discover function.

### Step 4: Configure LED Settings (Critical)

Navigate to **Config → LED Preferences** in WLED:

| Setting | Indoor WS2814 | Outdoor WS2814 | FCOB Indoor | FCOB Outdoor |
|---------|-------------|--------------|-------------|--------------|
| LED Type | WS2814 | WS2814 | PWM White | PWM White |
| Color Order | RGBW | RGBW | — | — |
| Length (pixels) | 84×5m = 420 | 420 | — | — |
| Max Brightness | 200/255 (~78%) | 200/255 | — | — |
| Max Current (mA) | set to strip budget | set to strip budget | — | — |

> **Set maximum current in WLED.** WLED has a built-in current limiter — enter the PSU's rated output current in mA (17000 mA for the LRS-200-12) and WLED will automatically cap brightness to stay within that budget. This is your primary over-current protection at the software level.

---

## WLED App Setup

- **iOS:** Search "WLED" or "WLED Native" on App Store
- **Android:** Download from https://github.com/Aircoookie/WLED-App/releases

In the app: tap **+** → Discover Lights → select your SP803E → control.

---

## Multi-Controller Sync (if you add a second SP803E for outdoor)

WLED supports sync between controllers via UDP:
1. **Config → Sync Interfaces → WLED Broadcast**
2. Set one unit as **Sync Master**, others as **Sync Receivers**
3. Both must be on the same WiFi subnet
4. Effects and brightness changes on master propagate to receivers in near real-time

---

## Music / Microphone Mode

The SP803E has an onboard analog microphone. To enable:
1. In WLED → **Config → Usermods**
2. Enable **AudioReactive** usermod (must be compiled into firmware — check current WLED release)
3. Set **Mic Pin** to **IO36**
4. Select an audio-reactive effect from the Effects palette

---

## Button Behavior
| Action | Result |
|--------|--------|
| Short press | Toggle on/off |
| Long press ~1s | Cycle through preset colors |
| Long press ~10s | **Factory reset** (clears all WiFi/config) |

---

## Firmware Update (Over-the-Air)
1. Navigate to WLED interface → **Config → OTA Firmware Update**
2. Or: Use https://install.wled.me with USB-C cable
3. Check https://github.com/Aircoookie/WLED/releases for latest stable version

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No power LED | No 12V or wrong polarity | Check PSU output, verify polarity |
| WLED-AP doesn't appear | Firmware issue | Reflash via USB-C + install.wled.me |
| LEDs all wrong color | Color order mismatch | Change color order in LED Preferences (try GRBW, RGBW, etc.) |
| First few LEDs correct, rest wrong | SPI signal integrity | Add 300–500Ω resistor in series on DATA line at strip input |
| LEDs flicker | Shared GND missing | Ensure SP803E GND and strip GND share common connection to PSU |
| OTA update fails | Firewall / network | Use USB-C method instead |
| PIR not triggering effects | GPIO not configured | Set GPIO in WLED Usermods → Button/PIR settings |

---

## Official Resources
- WLED documentation: https://kno.wled.ge
- WLED GitHub: https://github.com/Aircoookie/WLED
- WLED installer: https://install.wled.me
- WLED app releases: https://github.com/Aircoookie/WLED-App/releases
- BTF-LIGHTING SP803E product page: https://www.btf-lighting.com/products/esp-32-wled-wifi-music-led-controller
