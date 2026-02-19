# Mean Well LRS-200-12 — Power Supply Installation Reference
**Revision:** 2026-02-18  
**Source:** Mean Well official installation manual (Enclosed Type EN), product datasheet

---

## Specifications Summary

| Parameter | Value |
|-----------|-------|
| Model | LRS-200-12 |
| Output Voltage | 12V DC (adjustable ±10% via ADJ pot) |
| Output Current | 17A max |
| Output Power | 204W max |
| Input Voltage | 85–264VAC (switch selectable: 115V or 230V) |
| Input Frequency | 47–63 Hz |
| Efficiency | ~88% |
| No-load Power | < 0.75W |
| Operating Temp | -25°C to +70°C |
| Dimensions | 215mm × 115mm × 30mm (8.46" × 4.53" × 1.18") |
| Weight | ~0.54kg |
| Cooling | Convection (no fan — silent) |
| Protections | OVP, OCP, SCP, OTP |
| Approvals | UL 62368-1, IEC 62368-1 |

---

## Terminal Layout

### AC Input (left side of terminal block)
```
[ L ]  [ N ]  [ FG ]
```
- **L** = Line/Live (Black wire in North America)
- **N** = Neutral (White wire in North America)
- **FG** = Frame Ground (Green or bare copper)

### DC Output (right side of terminal block)
```
[ +V ]  [ -V ]  [ ADJ ]
```
- **+V** = Positive DC output (connect to your +12V bus)
- **-V** = Common/Negative (connect to your GND bus)
- **ADJ** = Fine-tune output voltage (factory set to 12.0V — leave alone unless compensating for voltage drop in very long runs)

---

## Terminal Screw Specs (LRS series)
- Screw size: **M3.5**
- Recommended torque: **8–10 kgf-cm**

---

## AC Wiring Steps (North America, 120V single-phase)

> ⚠️ De-energize at breaker and verify dead before proceeding.

1. Set the **115V/230V selector switch** on the unit side panel to **115V**.
2. Run 3-conductor wire (14 AWG minimum for 15A circuit) through a strain relief into your enclosure.
3. Strip 7mm of insulation from each conductor.
4. Connect:
   - Black (Hot) → terminal **L**
   - White (Neutral) → terminal **N**
   - Green/Bare (Ground) → terminal **FG**
5. Torque each terminal to 8–10 kgf-cm.
6. Tug-test each wire. No movement should occur.
7. Confirm no exposed copper outside terminals.

---

## DC Output Wiring Steps

1. Run appropriate gauge wire (see Master Guide §3.5) from +V and -V terminals.
2. For the LED installation, create a distribution bus if running multiple loads:
   - Main +V run → terminal block or bus bar → SP803E VCC + strip V+ feeds
   - Main -V run → terminal block or bus bar → SP803E GND + strip GND feeds
3. **Polarity is critical.** Label positive and negative clearly before energizing.

---

## Mounting

- Four mounting holes, one in each corner.
- Mount to non-conductive surface or grounded metal panel.
- Screw depth must not exceed the values in the case drawing (check the case drawing on the product page at meanwell.com) to avoid contacting internal PCB.
- Maintain 10–15 cm clearance from any heat source. Do not block the ventilation mesh on the top cover.
- Standard orientation: horizontal, label facing up. Vertical is acceptable at slight derating.

---

## Protection Behaviors

| Protection | Behavior | Recovery |
|-----------|---------|---------|
| Over Voltage (OVP) | Shuts output off | Cycle AC input |
| Over Current (OCP) | Hiccup mode | Auto-recovers when load returns to normal |
| Short Circuit (SCP) | Hiccup mode | Auto-recovers when short is cleared |
| Over Temperature (OTP) | Shuts output off | Auto-recovers when temp drops |

**Hiccup mode** means the unit pulses — tries to start, can't, tries again. If you see this, you have an overload or short. Find the cause before re-energizing.

---

## Peak Load Note
The LRS-200-12 supports **150% peak load (up to 25.5A) for up to 1 second**. If sustained beyond 1 second, it enters hiccup mode and recovers when load drops to rated levels. This means it handles LED startup inrush gracefully but cannot sustain overload.

---

## Output Voltage Adjustment (ADJ)
The ADJ pot can trim output between ~10.8V and 13.2V. If your outdoor DC run is long and you're seeing brightness dropoff at the far end, you can increase the output slightly (to 12.5V) to compensate. Do not exceed 13.2V — some LED strips and the SP803E controller have 12V max ratings.

---

## LED Power Supply Safety Notes (from MW's LED PSU manual)
- Do not install in high-moisture areas (the LRS-200-12 is **not waterproof**)
- Do not install near fire sources
- Output wattage must not exceed rated values
- Ground (FG) must be connected to earth
- If the AC cable is damaged, it must be replaced by a qualified person

---

## Support
- Mean Well official: www.meanwell.com
- Mean Well USA: www.meanwellusa.com | +1-510-683-8886
- Full datasheet PDF: https://www.meanwell.com/Upload/PDF/LRS-200/LRS-200-SPEC.PDF
- Installation manual PDF: https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf
