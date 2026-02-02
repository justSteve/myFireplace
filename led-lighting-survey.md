# LED Lighting Options Survey

A practical survey of LED lighting approaches ranging from high-end addressable strips to simple retrofit fixtures. Organized by use case with named products that have earned reasonable reputations in the DIY and home automation communities.

---

## Use Case Categories

| Category | Smart Features | Animation | Typical Location |
|----------|---------------|-----------|------------------|
| High-end addressable | WLED/WiFi | Full effects | Accent, display |
| Simple smart | WiFi or Zigbee | Color/dimming only | General rooms |
| Quality dumb | None | None | Anywhere reliability matters |
| Linear spans | Optional | Optional | Replacing multiple fixtures |

---

## 1. High-End Addressable (WLED Territory)

For locations where smooth animation, effects, and per-pixel control matter.

### Controllers

| Product | Chip | Pixels | Notes |
|---------|------|--------|-------|
| QuinLED-Dig-Uno | ESP32 | 1-2 strips | Well-documented, level shifter built in |
| QuinLED-Dig-Quad | ESP32 | 4 strips | Same ecosystem, more outputs |
| WLED Controller by Athom | ESP8266/32 | 1-2 strips | Pre-flashed WLED, plug and play |
| Generic ESP32 dev board | ESP32 | DIY | Cheapest, requires soldering level shifter |

**Notes on ESP8266 vs ESP32:**
- ESP8266: Fine for single strips under 300 pixels, cheaper
- ESP32: Better for multiple strips, faster animations, more GPIO, dual-core handles WiFi without stutter

### LED Strips (Addressable)

| Product/Type | LEDs/meter | Quality Tier | Notes |
|--------------|------------|--------------|-------|
| BTF-Lighting WS2812B | 30/60/144 | Budget-good | Amazon staple, decent color consistency |
| BTF-Lighting SK6812 RGBW | 30/60 | Mid | Dedicated white channel, better for illumination |
| QuinLED recommended strips | Various | Vetted | See quinled.info for tested strips |
| Ray Wu's Store (AliExpress) | Various | Good | Longer wait, better price, known vendor |

**SK6812 vs WS2812B:**
- WS2812B: RGB only, white = R+G+B (slightly purple tint)
- SK6812 RGBW: Dedicated white LED, true white, better CRI for general lighting

### Power Supplies

| Product | Output | Notes |
|---------|--------|-------|
| Mean Well LRS series | 5V/12V various amps | Industry standard, reliable |
| Mean Well HLG series | Constant current | Outdoor/wet rated, silent |
| Generic "LED power supply" | 5V/12V | Fine for small runs, inspect before trusting |

**Rule of thumb:** 60mA per pixel at full white, derate to 70-80% for headroom.

---

## 2. Simple Smart (Color/Dimming, No Animation)

For rooms where you want app/voice control and color temperature adjustment but don't need effects.

### Bulbs

| Product | Protocol | Notes |
|---------|----------|-------|
| Philips Hue | Zigbee (proprietary hub) | Premium price, excellent reliability, local API |
| IKEA Trådfri | Zigbee | Budget friendly, works with other Zigbee hubs |
| Sengled | Zigbee | No repeater function, but cheap and reliable |
| Wyze Bulb Color | WiFi | Budget, Tuya-based, can flash to local firmware |
| Athom pre-flashed bulbs | WiFi/ESPHome | Ships with open firmware, no cloud required |

### Switches (Smart, at the switch box)

| Product | Protocol | Notes |
|---------|----------|-------|
| Lutron Caseta | Proprietary RF | Rock solid, requires hub, no neutral needed |
| Inovelli Blue series | Zigbee | Enthusiast favorite, many configuration options |
| Zooz Z-Wave switches | Z-Wave | Good Home Assistant integration |
| Martin Jerry Tasmota | WiFi | Pre-flashed open firmware option |

**If avoiding WiFi/cloud entirely:** Zigbee or Z-Wave with local hub (Home Assistant, Hubitat) keeps everything LAN-only.

---

## 3. Quality Dumb LEDs (No Smart Features)

For locations where simplicity and reliability trump features. Flick the switch, light comes on.

### Retrofit Bulbs

| Product | Notes |
|---------|-------|
| Cree A19 | Long-standing reputation, good CRI |
| Philips Ultra Definition | High CRI (90+), available at big box stores |
| GE Reveal | Enhanced spectrum, good for color rendering |
| Feit Electric | Costco staple, decent quality, good warranty |

### Integrated Fixtures

| Product/Brand | Type | Notes |
|---------------|------|-------|
| Lithonia Lighting | Ceiling, panel, troffer | Commercial quality at consumer prices |
| Halo (Cooper) | Recessed | Well-regarded retrofit kits |
| WAC Lighting | Under-cabinet, accent | Higher end, good build quality |
| GetInLight | Under-cabinet | Budget but decent, hardwired or plug-in |

### Quality Indicators

- **CRI 90+**: Better color rendering, worth seeking out
- **Flicker-free / DC driver**: Reduces visible flicker
- **5-year warranty**: Signals manufacturer confidence
- **ETL/UL listed**: Safety certification

---

## 4. Linear Spans (6-12 foot runs)

For replacing multiple fixtures with a continuous light source.

### Aluminum Channel + Strip

This approach: LED strip mounted inside aluminum extrusion with diffuser cover. Clean look, good heat dissipation, customizable length.

| Product | Notes |
|---------|-------|
| Muzata LED channels | Amazon, various profiles, cheap but functional |
| Klus / WAC channels | Higher quality extrusions |
| SnapLight / Liteline | Semi-custom linear fixtures |

**Strip options for pure illumination (non-addressable):**

| Type | Notes |
|------|-------|
| COB LED strip | No visible dots, smooth light, newer tech |
| 2835 high-density (120/m) | Nearly seamless with good diffuser |
| 5050 single-color | Old standby, visible dots without diffuser |

### Pre-Made Linear Fixtures

| Product/Brand | Notes |
|---------------|-------|
| Lithonia FMLWL | Budget linear wrap, 2-4 foot |
| Barrina linkable | Popular garage/shop option, linkable to span |
| HyperSelect | Various lengths, decent reviews |
| WAC InvisiLED | Higher end, minimal profile |

### Non-WiFi Dimming Options

| Approach | Notes |
|----------|-------|
| Standard dimmer + dimmable driver | Lutron Diva + Mean Well PWM driver |
| 0-10V dimming | Commercial approach, requires compatible driver |
| RF remote (433MHz) | Cheap, local, no network needed |
| Inline dial dimmer | Simplest, manual adjustment |

---

## 5. Physical Control Options (Non-Smart Fallback)

For any smart setup, local control that survives network outages.

### Momentary Wall Switches

| Product | Notes |
|---------|-------|
| Zooz ZAC99 | Decora form factor, dry contact |
| Martin Jerry momentary | Designed for Home Assistant use cases |
| Generic "dry contact momentary rocker" | Various sources, same function |

### Other Physical Controls

| Type | Notes |
|------|-------|
| 433MHz RF remote | Cheap, no pairing hassles, works with many controllers |
| IR remote | WLED native support, line-of-sight required |
| Rotary encoder | Volume-knob style for dimming |
| ESPNow wireless button | ESP-to-ESP, no WiFi infrastructure needed |

---

## 6. Decision Framework

### Choose WLED/addressable when:
- Animation or effects are desired
- Per-segment or per-pixel control matters
- Color-chasing, music sync, holiday modes
- You want the flexibility even if you don't use it immediately

### Choose simple smart when:
- On/off, dimming, color temperature are sufficient
- Voice control is desired
- Integration with broader home automation
- Lower complexity than WLED

### Choose quality dumb when:
- Reliability is paramount
- No interest in automation at this location
- Budget matters and smart features don't
- Rental or temporary installation

### Choose linear span when:
- Replacing multiple fixtures on one circuit
- Even illumination over distance matters
- Cleaner look than multiple point sources
- Task lighting over counters or workspaces

---

## 7. Vendor Notes

**Generally well-regarded sources:**

- **QuinLED (quinled.info)**: Controllers and vetted component recommendations
- **DrZZs**: YouTube + store, WLED-focused
- **BTF-Lighting**: Amazon, decent price/quality ratio
- **Athom**: Pre-flashed ESPHome/WLED devices
- **Ray Wu (AliExpress)**: Bulk LED strip source, known vendor
- **Mean Well**: Power supplies, the safe default

**Approach with caution:**

- Random AliExpress LED strips (quality lottery)
- No-name Amazon power supplies (fire risk)
- Anything "smart" requiring proprietary cloud with no local option

---

## 8. Installation Considerations

### Wiring for WLED with local button

```
[120V from panel]
       |
       v
[Always-hot to LED power supply] --> [5V/12V to ESP + strip]
       |
[Switch box: momentary button] ---- [2-conductor low-voltage to ESP GPIO + GND]
```

### Wiring for dumb linear span with dimmer

```
[120V from panel]
       |
       v
[Dimmer switch] --> [Dimmable LED driver] --> [LED strip]
```

### Low-voltage wire for button runs

- 22-24 AWG sufficient
- Thermostat wire works well
- CAT5/6 if already available
- CL2/CL3 rated for in-wall

---

## 9. Open Questions for Your Install

- [ ] Which locations are high-end (animation) vs. simple illumination?
- [ ] Existing switch box wiring situation (neutral present?)
- [ ] Aesthetic preference: warm white, tunable white, or full RGB?
- [ ] Integration target: Home Assistant, standalone WLED, or no automation?
- [ ] Budget tier per location?

---

*Document created: January 2026*
*Purpose: Planning survey for multi-location LED installation*
