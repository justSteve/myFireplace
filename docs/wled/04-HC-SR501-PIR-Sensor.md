# HC-SR501 PIR Infrared Motion Sensor — Installation & Integration Reference
**Revision:** 2026-02-18  
**Quantity:** 3 units  
**Source:** Component datasheets, makerguides.com, lastminuteengineers.com tutorials

---

## Specifications

| Parameter | Value |
|-----------|-------|
| Input Voltage | 4.5V – 20V DC (5V typical) |
| Standby Current | < 60µA |
| Output Voltage | High = 3.3V, Low = 0V |
| Detection Range | 3m – 7m (adjustable via sensitivity pot) |
| Detection Angle | 110° cone |
| Hold Time (Tx) | 5s – 300s (adjustable via time-delay pot) |
| Blocking Time (Ti) | ~2.5s (fixed, non-adjustable) |
| Trigger Modes | Single (L) and Repeat (H) — jumper selectable |
| Initialize Time | ~30–60 seconds after power-on |
| Output Logic | 3.3V TTL (compatible with ESP32 GPIO directly) |

---

## Pinout

The HC-SR501 has 3 pins, typically labeled on the underside of the board (under the Fresnel dome lens):

```
Left to right (dome facing you):
  VCC  |  OUT  |  GND
```

| Pin | Function |
|-----|---------|
| VCC | Power input (4.5V–20V; use 5V) |
| OUT | Digital output: HIGH when motion detected, LOW when idle |
| GND | Ground |

> The dome lens can be gently pulled off to see pin labels if needed. Replace after confirming orientation.

---

## Board Controls

There are two potentiometers and one jumper on the board:

### Potentiometer 1: Sensitivity (Sx)
- Controls detection range (3m – 7m)
- **Clockwise** = more sensitive (longer range)
- **Counterclockwise** = less sensitive (shorter range)
- Start with middle position and adjust after installation

### Potentiometer 2: Time Delay (Tx)
- Controls how long the output stays HIGH after detecting motion
- Range: approximately **5 seconds to 5 minutes**
- **Clockwise** = longer hold time
- **Counterclockwise** = shorter hold time (minimum ~5s)
- For automated lighting: set to 1–3 minutes depending on use case

### Jumper: Trigger Mode
| Position | Mode | Behavior |
|---------|------|---------|
| **H** (Repeat Trigger) | Retriggerable | Hold time resets every time motion is detected. Output stays HIGH as long as motion continues. |
| **L** (Single Trigger) | Non-retriggerable | Triggers once, holds for Tx duration, then blocks for ~2.5s regardless of continued motion. |

**For lighting automation, use H (repeat trigger mode).** This keeps lights on as long as someone is present.

### Blocking Time (Ti)
After the output returns LOW, there is a fixed ~2.5 second window during which the sensor will NOT trigger, even if motion is present. This is a fixed hardware characteristic of the BISS0001 IC. Design your firmware/WLED integration to account for this brief dead zone.

---

## Wiring to SP803E (ESP32)

> See controller doc for GPIO selection. The SP803E's ESP32 can use any available GPIO not assigned to SPI/PWM.

```
HC-SR501                    SP803E / ESP32
─────────                   ──────────────
VCC ──────────────────────→ 5V (from USB or 5V regulator off 12V PSU)
GND ──────────────────────→ GND (common with PSU ground)
OUT ──────────────────────→ GPIO4 (or GPIO13, GPIO5 — any available GPIO)
```

**Why 5V for VCC, not 3.3V:** The HC-SR501's internal circuitry works best at 5V. While it can technically operate at lower voltages, sensitivity degrades. Power it at 5V.

**OUT to ESP32 GPIO:** The OUT pin outputs 3.3V when HIGH — safe for ESP32 GPIO directly. No level shifting needed.

**Getting 5V from your system:**
- Option A: Dedicated USB 5V charger sharing the same GND as the PSU
- Option B: Small 5V buck converter module (like an LM2596 module) from the 12V PSU rail — cheapest route when already running 12V
- Option C: USB power from the SP803E's USB-C port is not intended for peripheral power — don't use it

---

## Initialization Procedure

> ⚠️ **The HC-SR501 requires 30–60 seconds to initialize after power-on.** During this time the OUT pin may pulse HIGH multiple times spuriously. This is normal.

In your firmware/WLED integration, **ignore PIR output for the first 60 seconds after power-on**. Add a startup delay in any automation logic.

---

## Placement Considerations

### Indoor
- Mount at ceiling level (7–9 feet) for wide coverage of a room
- Point the dome downward, angled toward the expected movement zone
- Avoid pointing at windows (sunlight changes cause false triggers) or heating/AC vents (heat changes cause false triggers)
- Avoid pointing at ceiling fans
- The 110° cone means one sensor covers most of a typical room from a corner

### Outdoor
- Mount under eaves or in a protected location — the HC-SR501 is **not weatherproof**
- Place in a weatherproof enclosure (small project box) with the dome visible through a cutout
- Alternatively: mount indoors behind a window if the window is not thermally insulating (signal passes through thin glass reasonably well, though range is reduced)
- Avoid pointing at roads or areas with frequent vehicle traffic if you want human-only detection

### Multiple PIR Units (You Have 3)
Plan coverage zones:
- **Unit 1:** Indoor zone (e.g., living room/main area)
- **Unit 2:** Outdoor zone (near outdoor LED strip)
- **Unit 3:** Secondary indoor zone or backup/spare

All three can feed into the same SP803E ESP32 on different GPIO pins, or into separate GPIO pins if you want zone-specific responses.

---

## Integration with WLED

WLED supports external button/PIR inputs via the **Usermods → Button** configuration:

1. In WLED → **Config → Usermods**
2. Look for **Button/PIR** settings (available in recent WLED versions)
3. Set the GPIO pin to match your PIR wiring (e.g., GPIO4)
4. Configure action: e.g., "turn on when HIGH, turn off X seconds after LOW"
5. Optionally set a preset to load when triggered (specific effect/color/brightness)

> If your WLED build doesn't have the button usermod, you can flash a custom WLED build with it enabled via install.wled.me with custom compile options, or use a separate microcontroller that sends HTTP API commands to WLED on motion detection.

### WLED HTTP API (alternative integration)
If direct GPIO integration is insufficient, the ESP32 can run custom firmware alongside WLED, or you can use Home Assistant / Node-RED as middleware:

```
PIR HIGH → HTTP GET → http://[wled-ip]/win&T=1   (turn on)
PIR LOW  → HTTP GET → http://[wled-ip]/win&T=0   (turn off, after delay)
```

---

## Standalone Operation (No Microcontroller)
The HC-SR501 can also operate standalone — the OUT pin directly controls a relay or transistor to switch 12V power to the LED strips. This is the simplest possible integration and requires no code:

```
PIR OUT → Base of NPN transistor (2N2222 etc.) → transistor switches 12V to LED strip
```

This approach loses WLED's dimming and effects capability on motion events — appropriate only if you want pure on/off behavior.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Constant false triggers | Pointing at heat source / sunlight | Reposition or use cardboard mask to limit cone |
| No trigger at all | Wrong VCC voltage / wiring | Verify 5V at VCC; verify OUT connected to correct GPIO |
| Triggers only once then stops | Trigger mode set to L | Move jumper to H |
| Very short hold time | Tx pot at minimum | Turn Tx pot clockwise |
| Short range | Sx pot at minimum | Turn Sx pot clockwise |
| Spurious triggers at startup | Normal initialization behavior | Add 60s startup delay in automation logic |
| PIR works but WLED doesn't respond | GPIO not configured in WLED usermod | Check Usermods config in WLED |

---

## Mounting Hardware Note
The HC-SR501 board has mounting holes. Use M2 screws (non-conductive standoffs recommended) to mount inside an enclosure. Do not allow the underside of the board to contact metal — there are exposed traces and components.
