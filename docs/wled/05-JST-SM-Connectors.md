# BTF-LIGHTING JST-SM 3-Pin Connectors — Installation Reference
**Revision:** 2026-02-18  
**Item:** 5-pack, 20AWG, 3-pin JST SM male+female, 1.64ft/0.5m extension cable

---

## What These Are

JST-SM (sometimes called "SM" connectors or "ZH" in loose usage) are a widely-used standard for LED strip connections. Each pair consists of:
- **Male plug** (pins) — typically attached to the power/controller end
- **Female socket** (receptacle) — typically attached to the LED strip end

The 0.5m (20-inch) extension cables let you bridge the gap between the strip and the controller/PSU without soldering.

---

## Specifications

| Parameter | Value |
|-----------|-------|
| Pitch | 2.54mm (JST SM standard) |
| Pin count | 3 pins |
| Wire gauge | 20 AWG |
| Extension length | 1.64ft / 0.5m per piece |
| Quantity | 5 pairs (male + female) per pack |
| Rated current | ~3A per pin (conservative for 20AWG) |
| Max current | Safe up to ~5A with good connection; derate for heat |

---

## Pin Assignment (Standard for WS2811/WS2812/WS2814 strips)

| Pin # | Function | Wire Color (common) |
|-------|---------|-------------------|
| 1 | V+ (12V power) | Red |
| 2 | DATA (signal) | Green or Yellow |
| 3 | GND | Black or White |

> ⚠️ **Wire colors are not universal.** Always verify against the strip manufacturer's labeling before connecting. BTF-LIGHTING strips are generally consistent but confirm visually.

---

## Critical Notes on Current Capacity

20 AWG wire is rated for approximately 3–4A at acceptable voltage drop for short runs. Your FCOB strips may draw up to 4A per strip — this is at the edge of what 20 AWG handles comfortably.

**For FCOB strips (pure power connections):**
- 20 AWG is marginal for 4A over 20 inches. Acceptable if the ambient is cool and runs are short.
- If you notice warm/hot connectors during operation, upgrade to 18 or 16 AWG wire for power runs and use these JST-SM cables only for the signal/data connections.

**For WS2814 addressable strips:**
- Power (V+, GND) carries higher current — consider direct heavier wire runs from PSU to strip, using these connectors only for the DATA line connection.

---

## Connecting to WS2814 Strips

The WS2814 IP30 and IP67 strips use 3-pin (or 4-pin with backup data) connectors. The JST-SM 3-pin connectors cover the primary three: V+, DATA, GND.

**Connection flow:**
```
PSU +12V → Heavy wire → Strip V+ pad
               OR
PSU +12V → JST-SM pin 1 (Red) → Strip
SP803E GND ← JST-SM pin 3 (Black) ← Strip GND
SP803E IO16 → JST-SM pin 2 (Green) → Strip DATA
```

For the backup/return data wire (WS2814's 4th wire), solder directly to the strip pad — no JST-SM breakout for this wire.

---

## Connecting to FCOB Strips

FCOB strips have only two electrical connections: V+ and GND. The third JST-SM pin (DATA) is unused for passive FCOB strips. Options:
- Use only pins 1 and 3 (V+ and GND); leave pin 2 disconnected
- Or solder direct with heavier wire to the exposed FCOB pads

---

## Making a Field Connection

1. Verify polarity of the strip end before mating. Look for (+) and (-) labels near the strip connector or pads.
2. Hold the connector with the locking tab accessible (usually top-facing).
3. Press male into female until you feel/hear a click. The tab locks them together.
4. To disconnect: press the locking tab on the female receptacle and pull straight out. Do not yank by the wire — grip the connector body.

---

## Weatherproofing Outdoor Connections

JST-SM connectors have no inherent weatherproofing. For outdoor use:
1. Apply **dielectric grease** (e.g., Permatex 22058 or Dow Corning 111) inside both sides of the mated pair before connecting.
2. Wrap the mated connector with **self-amalgamating silicone tape** (stretchy, bonds to itself) — wrap 2–3 layers, starting 1 inch back from the joint and extending 1 inch past.
3. Alternatively, house the connections inside a small IP65+ weatherproof junction box (e.g., a PVC handy box with a foam seal cover — available at any hardware store).

---

## Extending Beyond 0.5m

You have five 0.5m extension cables. If you need longer runs, options:
- Daisy-chain up to 2 extension cables for data signals (max ~1m total extension before signal degradation risk on DATA)
- For power pins (V+ and GND), you can use longer/heavier direct wire runs — the JST-SM is a convenient connection point, not the power delivery medium
- Do NOT chain more than 2 of these for DATA — the signal integrity degrades on long thin 20 AWG runs for addressable strips

---

## Troubleshooting Connector Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| LEDs dim or flickering | Loose connector contact | Re-seat; check for bent pin |
| Warm connector body | Over-current through 20 AWG | Upgrade to direct heavier wire for power pins |
| No signal to strip | DATA pin connected to wrong position | Verify pin 2 = DATA (not V+ or GND) |
| Connector won't mate | Bent or misaligned pin | Straighten pin carefully with small pick |
| Outdoor connection corroded | No weatherproofing applied | Disconnect, clean, apply dielectric grease, re-seal |
