# LED Lighting System — Master Installation Guide
**Revision:** 2026-02-18  
**Scope:** Indoor + Outdoor LED installation using Mean Well LRS-200-12, SP803E WLED controller, FCOB/WS2814 strips, HC-SR501 PIR sensor

---

## 1. System Overview

You have two physical installation points sharing a single LRS-200-12 power supply:

| Zone | Strip Type | Controller | Notes |
|------|-----------|------------|-------|
| **Indoor** | FCOB 9W/m non-waterproof IP20 | SP803E (PWM channel) | Warm white only, dimmable |
| **Indoor** | WS2814 RGBW IP30 (84LED/m) | SP803E (SPI channel) | Full dream-color |
| **Outdoor** | FCOB IP67 waterproof (480LED/m) | SP803E or second controller | Warm white, weatherproof |
| **Outdoor** | WS2814 RGBW IP67 (84LED/m) | SP803E (SPI channel) | Dream-color, weatherproof |
| **Sensor** | HC-SR501 PIR | GPIO input to ESP32 on SP803E | Motion trigger for auto-on |

The SP803E has **one SPI output** (IO16) and **three PWM channels** (IO25, IO26, IO27). You can run the FCOB white strips on PWM and one WS2814 run on SPI — but **you cannot independently address both WS2814 zones simultaneously from a single SP803E**. Plan accordingly: either both WS2814 zones run in sync, or you add a second SP803E for the outdoor WS2814 run (they can be synced via WLED's sync protocol).

---

## 2. Power Budget — Critical Before You Wire Anything

### Component Inventory
| Strip | Length | Power/m | Total Power |
|-------|--------|---------|------------|
| FCOB 480LED/m IP67 (outdoor) | 5m (16.4ft) | ~9.6W/m est. | ~48W |
| FCOB 9W/m IP20 (indoor) | 5m (16.4ft) | 9W/m | 45W |
| WS2814 RGBW IP30 (indoor) | 5m (16.4ft) | ~12W/m @ full white | ~60W |
| WS2814 RGBW IP67 (outdoor) | 5m (16.4ft) | ~12W/m @ full white | ~60W |
| SP803E controller | — | 0.15A max = 1.8W | ~2W |
| HC-SR501 PIR (×3) | — | ~0.04W each | <1W |
| **TOTAL THEORETICAL MAX** | | | **~216W** |

**The LRS-200-12 is rated 200W (17A @ 12V). This is tight at theoretical max.** However:
- WS2814 full-white max is a worst case. Normal operation (effects, partial brightness) runs 30–50% of that.
- You almost certainly won't run all strips at 100% simultaneously.
- **Safety rule:** Never load the PSU above 80% sustained = 160W. For full-brightness white scenes on all strips, you'd exceed this. Use brightness caps in WLED (see controller doc).

**Recommended WLED global brightness cap:** Set to **~70%** in WLED config to stay under 160W sustained. This still yields excellent brightness in practice.

If you later want true 100% capacity on all strips simultaneously, add a second LRS-200-12 and split zones.

---

## 3. 120V Mains Wiring — READ BEFORE TOUCHING

> ⚠️ **STOP.** If you are not confident working with 120V mains, hire a licensed electrician for this section. The LRS-200-12 is a component power supply — it is not a consumer appliance with a standard plug. Wiring it requires connecting line voltage to screw terminals inside the enclosure. There is lethal voltage present.

### 3.1 Safety Precautions
- **Always de-energize the circuit at the breaker before working.** Lock out or tape the breaker. Confirm dead with a non-contact voltage tester.
- The LRS-200-12 has **no built-in power switch**. Once wired, it is live whenever the circuit is energized. Plan a switch or smart outlet in your design.
- The unit **must be mounted** — do not leave it free-hanging by wires. See section 3.3.
- The FG (Frame Ground) terminal **must be connected** to your household earth ground (bare copper or green wire). Skipping this is a shock hazard.
- Confirm your existing circuit is rated appropriately. The LRS-200-12 draws a max of ~2.4A @ 120VAC (200W ÷ 120V ÷ ~0.88 efficiency). A 15A circuit handles this fine. Confirm no other heavy loads share the circuit.

### 3.2 Voltage Selector Switch
The LRS-200-12 has a **115V / 230V selector switch** on the side. Before first power-on, confirm it is set to **115V** for North American household current. This is typically set at the factory for US-destined units but verify — running it on the wrong setting can damage the unit or be a fire hazard.

### 3.3 Mounting
- Mount the unit with screws through the four corner holes to a non-conductive panel, DIN rail adapter, or plywood backboard inside an enclosure.
- Preferred orientation: horizontal (label facing up). Vertical mounting is acceptable but derate by 5–10% in sustained load.
- The LRS-200-12 is convection-cooled (no fan). Maintain **at least 4 inches clearance** on all sides, especially above. Do not enclose in a sealed box without ventilation.
- Never install in a wet location. The PSU is not weatherproof. Both your indoor and outdoor runs must originate from a dry, interior mounting point.

### 3.4 Wiring the AC Input Terminals (L, N, FG)

The LRS-200-12 input terminal block has three positions:

| Terminal Label | Wire (North America) | Color |
|----------------|---------------------|-------|
| L (Live/Line) | Hot | Black |
| N (Neutral) | Neutral | White |
| FG (Frame Ground) | Earth Ground | Green or bare copper |

**Procedure:**
1. De-energize at breaker. Verify dead.
2. Route your household wire (must be 14 AWG min for 15A circuit, 12 AWG for 20A circuit) through an appropriate strain relief into the PSU enclosure area or your junction box.
3. Strip approximately 7mm (¼ inch) of insulation from each wire end.
4. Insert into the correct terminal and tighten to **8–10 kgf-cm** (M3.5 screws). This is moderate finger-tight plus a quarter turn with a small flathead. Overtightening damages the terminal; undertightening causes arcing.
5. Tug each wire firmly after tightening to confirm it will not pull free.
6. Ensure no bare copper is exposed outside of the terminal.

> **INDOOR POINT:** Your existing wiring runs to an indoor location. Mount the PSU at this location inside an appropriate enclosure (a project box, junction box, or electrical panel surface-mount box). All mains connections must be inside an enclosure — no exposed line voltage.

> **OUTDOOR POINT:** Your existing wiring runs to an outdoor location. The PSU itself must NOT be mounted outdoors unless in a NEMA-rated weatherproof enclosure. Best practice: mount the PSU indoors or in a protected junction box near the exterior wall, and run only 12VDC to the outdoor strips. 12VDC outdoors is safe, low-voltage — no permit concerns and no shock hazard.

### 3.5 Wiring the DC Output Terminals (+V, -V / COM)

| Terminal | Connection |
|----------|-----------|
| +V | Positive (red) to SP803E VCC and LED strip V+ |
| -V (COM) | Negative (black) to SP803E GND and LED strip GND |
| ADJ | Output voltage trim potentiometer — do not adjust unless needed |

**Wire gauge for DC runs:**
| Run Length | Current | Min Wire Gauge |
|-----------|---------|---------------|
| < 3 feet | Up to 17A | 16 AWG |
| 3–6 feet | Up to 17A | 14 AWG |
| > 6 feet | Up to 17A | 12 AWG |
| To controller only (<2A) | — | 20 AWG fine |

For runs from the PSU to the strips (especially the high-density FCOB strips), use 14 AWG minimum if the run is more than a few feet. Voltage drop on DC runs degrades brightness.

### 3.6 Voltage Drop on Long DC Runs
For the outdoor zone, if your DC run from PSU to the strip start is more than ~6 feet, you will see voltage drop. With the 480LED/m FCOB strip drawing significant current, this matters.

**Rule of thumb:** Measure the round-trip wire length (positive + negative, both ways), multiply by resistance. Use online voltage drop calculators if in doubt.

**Mitigation options:**
- Power the strip from **both ends** (run a parallel feed from the PSU to the far end of the strip). This halves the effective resistance.
- Keep DC wire gauge as heavy as practical.
- Install the PSU as close as possible to the strips.

---

## 4. System Topology Diagram (Text)

```
120V Household Circuit (existing wiring)
│
├── [INDOOR POINT]
│   └── Junction Box
│       └── Mean Well LRS-200-12
│           ├── +12V ──→ SP803E VCC (and common bus)
│           ├── GND  ──→ SP803E GND (and common bus)
│           │
│           ├── SP803E SPI out (IO16) ──→ WS2814 IP30 RGBW Indoor (JST-SM connector)
│           ├── SP803E PWM1 (IO25)    ──→ FCOB 9W/m Indoor (direct or JST-SM)
│           └── SP803E GPIO  ──────── ──→ HC-SR501 OUT (motion trigger)
│
└── [OUTDOOR POINT] (existing 120V run)
    └── *** OPTION A: Small weatherproof box with PSU here ***
        OR
        *** OPTION B (RECOMMENDED): PSU stays indoor, only 12VDC runs outside ***
            ├── 12VDC run (14 AWG, in conduit if long) ──→ Outdoor Distribution Point
            │   ├── WS2814 IP67 RGBW Outdoor (JST-SM)
            │   └── FCOB IP67 480LED/m (direct connection)
            └── Second SP803E (optional, for independent outdoor control)
                synced to indoor SP803E via WLED Sync
```

---

## 5. Sequencing / First-Power-Up Order

Follow this order to avoid damage:

1. **Before any power:** Complete all DC wiring (PSU to controller, controller to strips) with the AC breaker OFF.
2. **Verify polarity** on every DC connection with a multimeter before energizing. Reverse polarity on the strips destroys them instantly.
3. **Configure WLED first** (see controller doc) — connect to SP803E via USB-C and configure LED type and count before attaching strips, or at minimum before running effects.
4. **First energize:** Turn on breaker. The SP803E green LED should illuminate. Do NOT touch the PSU's AC terminals at this point.
5. **Check DC voltage** at the output terminals with a multimeter: should read 12.0V ±0.5V.
6. **Connect strips** one at a time via JST-SM connectors. Verify the first strip lights up correctly in WLED before connecting the next.
7. **Test PIR** last, after all lighting is confirmed working.

---

## 6. Outdoor Weatherproofing Notes

- Your IP67 strips (FCOB and WS2814) are waterproof along their length, but **the cut ends and JST-SM connection points are not automatically sealed**.
- Seal all cut ends with clear silicone sealant. Allow 24 hours to cure before exposing to weather.
- Use weatherproof wire nuts or IP-rated junction boxes for any outdoor DC connections.
- JST-SM connectors have basic splash resistance but are not IP67-rated at the joint. Mount connectors in a protected location (under eave, inside conduit fitting) or apply dielectric grease and weatherproof tape.
- Secure strips to surfaces with clips (aluminum channel recommended — diffuses light, protects strip, conducts heat away). For outdoor FCOB 480LED/m, heat is significant — aluminum channel is not optional, it's required for longevity.

---

## 7. Safety Checklist Before Going Live

- [ ] Voltage selector set to 115V on LRS-200-12
- [ ] PSU mounted rigidly, not free-hanging
- [ ] FG (frame ground) connected to earth ground
- [ ] All AC connections inside enclosed junction box
- [ ] DC polarity verified with multimeter before connecting strips
- [ ] WLED configured with correct LED type and pixel count before running effects
- [ ] WLED global brightness capped at ~70% to stay within PSU safe load
- [ ] Outdoor DC connections protected from weather
- [ ] Strip cut ends sealed with silicone (outdoor strips)
- [ ] Adequate clearance around PSU for convection cooling
- [ ] No load exceeds 80% of PSU rating (160W) for sustained operation

---

## 8. Component Quick Reference

| Component | File |
|-----------|------|
| Mean Well LRS-200-12 PSU | `01-PSU-MeanWell-LRS200-12.md` |
| SP803E WLED Controller | `02-SP803E-WLED-Controller.md` |
| FCOB & WS2814 LED Strips | `03-LED-Strips.md` |
| HC-SR501 PIR Sensor | `04-HC-SR501-PIR-Sensor.md` |
| JST-SM Connectors | `05-JST-SM-Connectors.md` |
