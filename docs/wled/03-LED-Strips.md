# BTF-LIGHTING LED Strips — Installation Reference
**Revision:** 2026-02-18  
**Strips Covered:**
1. FCOB COB IP20 (indoor), 9W/m, 480LED/m, 12V, warm white 3000K — non-waterproof
2. FCOB COB IP67 (outdoor), ~9.6W/m, 480LED/m, 12V, warm white 3000K — waterproof
3. WS2814 RGBW IP30 (indoor), 12V, 84LED/m, 28 pixel/m — non-waterproof
4. WS2814 RGBW IP67 (outdoor), 12V, 84LED/m, 28 pixel/m — waterproof

---

## Strip Comparison at a Glance

| Strip | Type | IP | Voltage | LEDs/m | Pixels/m | Width | Cut Point | Connector |
|-------|------|-----|---------|--------|---------|-------|----------|-----------|
| FCOB Indoor | COB, passive | IP20 | DC12V | 480 | N/A | 8mm | ~33mm | Solder or pad |
| FCOB Outdoor | COB, passive | IP67 | DC12V | 480 | N/A | wider | ~33mm | Solder or pad |
| WS2814 Indoor | IC, addressable | IP30 | DC12V | 84 | 28 | 12mm | per LED (1-LED) | JST-SM or solder |
| WS2814 Outdoor | IC, addressable | IP67 | DC12V | 84 | 28 | 14mm | per LED (1-LED) | JST-SM or solder |

---

## 1. FCOB COB LED Strips (Both Variants)

### What FCOB Means
FCOB = Flexible Chip-On-Board. Instead of discrete 5050 or 2835 LED packages spaced apart, hundreds of tiny LED chips are bonded directly to the PCB and covered with phosphor. The result is a **continuous, dotless glow** — no hot spots, no visible individual LEDs. This is ideal for architectural lighting, cove lighting, and ambient glow effects.

### Key Characteristics
- **Not individually addressable.** The entire strip operates as one zone. Control is brightness only via PWM dimming.
- **High density (480LED/m)** means very even light even from close range.
- **CRI 90+** — excellent color rendering, appropriate for task-adjacent uses.
- **DC12V** — do not use 5V or 24V supplies.
- **8mm width (indoor)** is very narrow — fits in tight aluminum channels.
- **IP67 (outdoor)** means the strip PCB is encased in a silicone jacket — it's fully submersible, but this also means you **cannot solder to the outdoor strip** mid-run without breaking the waterproofing.

### Power Planning for FCOB Strips
- Indoor FCOB: 9W/m × 5m = **45W total**
- Outdoor FCOB: nominal ~9.6W/m × 5m ≈ **48W total** (manufacturer's rating may vary — check packaging)
- Combined FCOB load: ~93W

At 12V:
- Indoor FCOB current: 45W ÷ 12V = **3.75A**
- Outdoor FCOB current: 48W ÷ 12V = **4.0A**

Use wire sized accordingly. For runs over 3 feet, use at least 18 AWG; over 6 feet, use 16 AWG.

### Cutting FCOB Strips
- Cut on marked cut lines only (approximately every 33mm for 480LED/m density).
- Cut cleanly with sharp scissors or wire cutters. A ragged cut may short adjacent traces.
- **Indoor (IP20):** Solder wires directly to the exposed copper pads at the cut point. Polarity is marked (+) and (−).
- **Outdoor (IP67):** The silicone jacket must be carefully slit and peeled back at the cut point to expose pads. Re-seal with silicone sealant after soldering. This is fiddly — consider planning your run length to avoid mid-strip cuts on the outdoor IP67 strip.

### Dimming the FCOB Strips
These are connected to the SP803E's PWM channels (IO25, IO26, IO27). The PWM signal controls brightness 0–100%. In WLED, the FCOB zones appear as white channels and can be animated, faded, triggered by PIR, and scheduled.

### Heat Management (Critical for FCOB)
480LED/m is very high density. The strip generates real heat — enough that **prolonged operation without a heat sink will significantly shorten strip life** and can cause color shift (the phosphor degrades with heat).

**Aluminum channel is mandatory for reliable operation.** The channel conducts heat from the PCB to the ambient. Options:
- U-channel (diffuser clips on top) — good for recessed cove mounting
- V-channel — concentrates light, good for narrow gaps
- Surface-mount flat channel — easiest to work with

Adhesive on the back of the strip helps but the primary thermal path is the aluminum channel contact. Apply the strip firmly, full contact.

---

## 2. WS2814 RGBW LED Strips (Both Variants)

### What WS2814 Means
WS2814 is an RGBW IC — each "pixel" contains one red, one green, one blue, and one warm-white LED, all driven by an embedded control IC. It is similar to WS2812B but operates at **12V** (not 5V) and adds the warm-white channel for a four-channel color capability.

Each pixel is individually addressable — you can set any pixel to any RGBW combination independently. This enables chasing effects, animations, and dynamic patterns.

**28 pixels per meter** × 5m = **140 pixels** per 16.4ft strip.

### Key Characteristics
- **DC12V operation** — confirmed, same PSU as FCOB strips.
- **RGBW** (4 channels per pixel). In WLED, configure as WS2814, color order RGBW.
- **84 LEDs/m, 28 pixels/m** — each pixel contains 3 color LEDs (R+G+B) + 1 white LED.
- **IP30 (indoor)** — no protection. Keep dry.
- **IP67 (outdoor)** — silicone jacket, same handling considerations as FCOB IP67 above.
- **12mm PCB width (IP30)** vs **14mm PCB width (IP67)**.

### Dual-Signal Architecture (WS2814 Reliability Feature)
WS2814 strips have a **backup data line**: if one pixel's IC fails, the signal passes around it to the next pixel. This means a single failed LED doesn't kill the rest of the strip — remaining pixels continue to function. When wiring, look for the DATA IN and DATA RETURN (or backup) connectors.

### Connector Pinout (WS2814)
The strip has a 4-wire interface, typically:
```
Pin 1: V+ (12V positive)
Pin 2: DATA (signal from controller)
Pin 3: GND
Pin 4: BACKUP/RETURN DATA (connect to controller's backup output if available; can be left floating on SP803E single-output setups)
```

> The included JST-SM connectors are 3-pin. WS2814 technically has 4 wires. Verify the connector on your specific strip before assuming JST-SM compatibility. You may need to solder the backup data wire separately or leave it unconnected (the strip works without it — you just lose the failover feature).

### Power Planning for WS2814 Strips
Full-white (all R+G+B+W at max) is worst case:
- Typical estimate: ~12W/m × 5m = ~60W per strip
- Two WS2814 strips (indoor + outdoor): **~120W combined at absolute max**

Normal operation (effects, partial brightness, mixed colors) will be 30–50% of max. WLED's current limiting handles this automatically if configured.

### Cutting WS2814 Strips
- Cut every 1 LED (at marked cut lines)
- Each cut point exposes solder pads for V+, DATA, GND, (BACKUP)
- Seal cut ends on IP67 outdoor strip with silicone
- After cutting, the strip can be reconnected using the JST-SM connector kit or by soldering

### WS2814 and WLED Configuration
In WLED LED Preferences:
- **LED Type:** WS2814 (listed in WLED as of v0.13+)
- **Color Order:** RGBW (if colors appear wrong, try GRBW, WRGB, etc.)
- **Length:** Number of pixels (28 per meter × your cut length)
- **Voltage:** 12V (WLED uses this for current estimation)
- **Max mA:** Set to your PSU's budget

> WS2814 may also appear in WLED as SK6812 RGBW — they use the same protocol. If WS2814 is not a listed option, select **SK6812 RGBW** as a fallback and verify correct color output.

---

## 3. Connecting Strips in Series vs. Parallel

### Data (SPI/IC strips only): Always Series
Data flows from controller → pixel 1 → pixel 2 → ... → last pixel. You cannot branch the data line.

### Power: Always Parallel (from PSU bus)
Do NOT daisy-chain power (PSU → strip A → strip B). Instead, run independent power feeds from the PSU bus to each strip's start. This avoids cumulative voltage drop.

**For long runs (>3m), power from both ends:**
- Run a second feed wire from the PSU to the far end of the strip
- Connect to V+ and GND pads at the far end
- This halves the effective resistance and dramatically reduces brightness dropoff

---

## 4. Outdoor Strip Weatherproofing (IP67 Strips)

### What IP67 Protects Against
IP67 means the strip body is sealed against dust (6) and water immersion up to 1m for 30 minutes (7). This covers rain, splashing, and typical outdoor moisture. It does **not** protect against:
- Pressure washing
- Constant submersion
- Exposed cut ends
- Un-sealed connection joints

### Field Sealing Procedure
1. **Cut ends:** Apply clear RTV silicone sealant over the cut end. Work it into any gaps. Let cure 24 hours.
2. **JST-SM connections outdoors:** Apply dielectric grease (Dow 111 or equivalent) inside the connector before mating. Wrap with self-amalgamating (silicone) tape. Or position connections inside a weatherproof junction box.
3. **Power injection points:** Any solder joint or pad must be fully covered with silicone before outdoor exposure.

### Aluminum Channel for IP67 Strips
IP67 strips are slightly thicker (silicone jacket). Verify your channel has sufficient internal depth. Most standard U-channels accommodate IP67 strips — check the internal depth spec (need at least 5mm, ideally 7mm for good contact).

---

## 5. Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| WS2814: No light | No data signal or wrong LED type | Check WLED LED type = WS2814 or SK6812 RGBW |
| WS2814: Wrong colors | Color order incorrect | Try RGBW, GRBW, WRGB in WLED color order setting |
| WS2814: First pixel lights, rest dark | Insufficient data signal amplitude | Add 300–500Ω resistor in series on DATA line |
| FCOB: Dim at far end | Voltage drop on long run | Power from both ends; increase wire gauge |
| FCOB: Flickering | Poor PWM ground connection | Ensure SP803E and strip share common GND |
| IP67: Water got inside | Cut end not sealed | Remove moisture, dry fully, re-seal with silicone |
| All strips: Dim overall | PSU overloaded | Cap WLED brightness; check PSU output voltage |

---

## 6. Return Window Note
Per your order information: **return/replacement eligible through March 18, 2026.** Test all strips within this window. Specifically verify:
- IP67 rating: inspect for obvious silicone jacket defects
- WS2814: verify all pixels light up with a solid color test in WLED
- FCOB: verify even illumination with no dark spots
