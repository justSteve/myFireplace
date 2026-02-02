# Precision Cutting Sled — SBR20 Linear Rail System

## Purpose

A manually operated precision cutting system designed to rip 1/4" ceramic tile into strips as narrow as 3/4" with clean, chip-free edges. Conventional wet tile saws produce unacceptable chipping at these narrow widths.

## Key Insight

The angle grinder approach with a thin continuous-rim diamond blade cuts by abrasion rather than impact, producing dramatically cleaner edges on ceramic. The linear rail system constrains movement to a single axis, preventing the lateral wobble that causes chip-out.

## Hardware

### Linear Rails (Acquired)

- **Product**: VEVOR SBR20-1000mm Linear Rail Kit
- **Rails**: 2× SBR20 supported rails, 1000mm (39.37") long
- **Shaft diameter**: 20mm
- **Bearing blocks**: 4× SBR20UU (2 per rail)
- **Mounting**: Rails bolt to flat reference surface through pre-drilled holes

### Angle Grinder (Available)

- **Tool**: Makita 4.5" angle grinder (fixed speed ~10,000-11,000 RPM)
- **Blade**: 4" or 4.5" continuous rim diamond blade
- **Recommended blade**: Montolit CGX 115 or similar porcelain-rated continuous rim
- **Kerf**: ~0.045-0.050" (significantly thinner than router bits)
- **RPM**: Fixed speed is acceptable — diamond blades are rated for standard grinder speeds

### Diamond Blade Selection

| Blade | Kerf | Notes |
|-------|------|-------|
| **Montolit CGX 115** | 0.047" | Pro-grade, excellent edge quality |
| **Alpha Porcellana** | 0.050" | Designed for porcelain/ceramic |
| **QEP 6-4001 (4")** | 0.060" | Budget option, adequate for ceramic |

**Requirements:**
- Continuous rim (NOT segmented or turbo — these chip)
- 7/8" arbor (standard for 4.5" grinders)
- Fine diamond grit for smooth cuts

## Design Concept

### Assembly Overview

```
[Side View]

   ┌─Angle Grinder──┐
   │                 │
   └───┤Blade├───────┘
       │     │
  ═════╪═════╪═════════  ← Carriage Plate (spans rails)
  ─────┼─────┼─────────  ← SBR20 Rails
       │     │
       │  ↓  │
  ─────┴─────┴─────────  ← Tile on Platen
  ═════════════════════  ← Angled Bed Frame
```

### Component Stack (top to bottom)

1. **Angle grinder** — Mounted to carriage plate, blade pointing down
2. **Carriage plate** — Aluminum plate bolted to 4 bearing blocks
3. **Bearing blocks** — Ride on SBR20 rails, single-axis constraint
4. **SBR20 rails** — Mounted to frame, establish the cut line
5. **Air gap** — Clearance for blade and water
6. **Tile** — Workpiece, face down on platen
7. **Platen** — Flat reference surface, may include angle
8. **Angled bed frame** — Introduces taper angle (if needed)
9. **Water tray** — Catches water/slurry, drains to collection
10. **Frame** — Steel tube structure at working height

### Carriage Plate

- Material: 1/2" aluminum plate
- Width: Spans between the two rails + bearing block overhang (~10")
- Length: ~8" in travel direction
- Features:
  - 4× bearing block mounting holes (match SBR20UU bolt pattern)
  - Slot for blade passage (oriented perpendicular to travel)
  - Angle grinder body clamp/mount
  - Handle attachment points

### Angle Grinder Mount

The grinder body needs secure mounting that:
- Positions blade perpendicular to rail travel
- Allows vertical adjustment for depth control
- Provides rigid connection (no flex during cut)
- Permits easy blade changes

Options:
- Custom aluminum clamp blocks matching grinder body diameter
- Commercial grinder stand adapter (modified for carriage mounting)
- 3D-printed clamp prototype for fit testing before metal fabrication

### Platen (Work Surface)

- Flat reference surface below the rail plane
- Tile sits face-down (cut from back to reduce visible chipping)
- Fence on one edge for strip indexing
- Spacer blocks for consistent strip width

### Angled Bed Frame

The taper angle (if the post tapers) is introduced by angling the platen relative to the rail axis. The carriage travels in a perfectly straight line; the tile below is what's angled.

Angle is very small (<2°) — the rise over a 24" tile is fractions of an inch.

### Indexing System

1. Fence on the "downhill" edge provides fixed reference
2. Cut a strip
3. Remove cut strip
4. Slide remaining tile against fence
5. Insert spacer block (machined to strip width + kerf)
6. Clamp tile
7. Cut next strip
8. Repeat

### Water Management

- Diamond blades require wet cutting for blade life and dust control
- Gravity-fed water from reservoir above
- Bed slopes slightly toward drain
- Tile on standoffs so water flows underneath
- Collection tray below catches slurry
- Silica dust hazard eliminated by wet cutting

## Cutting Technique

### Multiple Passes for Edge Quality

Through-cutting in **2-3 passes** produces cleaner edges than a single deep cut:

| Pass | Depth | Purpose |
|------|-------|---------|
| 1 | ~0.100" | Establish kerf, defines edge quality |
| 2 | ~0.100" | Deepen cut |
| 3 | Through | Complete separation |

The first pass matters most — it defines the visible edge. Subsequent passes follow the established groove.

### Feed Rate

- Manual, steady pressure
- Let the blade cut — don't force it
- Consistent speed produces consistent edge quality
- Ceramic (vs. porcelain) allows slightly faster feed

### Depth Control

Adjustable grinder mount height or carriage-mounted depth stop. Must allow repeatable settings for multi-pass cuts.

## Build123d Modeling Plan

First models to generate once the environment is running:

1. **SBR20 rail and bearing block** — Accurate to datasheet dimensions
2. **Carriage plate** — With blade slot and grinder mount provisions
3. **Angle grinder mount** — Clamp geometry for specific grinder model
4. **Platen assembly** — Work surface with fence and spacer provisions
5. **Angled bed frame** — Adjustable angle mechanism
6. **Complete assembly** — All components positioned, showing clearances

Each will be a parametric Python script. Change a dimension, re-run, see the update.

## Specifications to Confirm

- [ ] SBR20UU bearing block dimensions and bolt pattern (from VEVOR datasheet)
- [ ] Angle grinder body diameter and mounting geometry
- [ ] Frame material and dimensions (steel tube size)
- [ ] Working height preference
- [ ] Platen material (aluminum, HDPE, or marine plywood for water resistance)

## Tile Material Notes

The target material is **ceramic** (not porcelain):
- Tan bisque body visible on cut edge
- More forgiving than porcelain — less prone to chipping
- Softer body allows slightly faster feed rates
- Less aggressive blade wear than porcelain

Standard continuous-rim diamond blades (even budget options) perform well on ceramic.

## Visualization

- `visualizations/tile-cutting-jig.html` — Annotated isometric SVG diagram (needs update for grinder config)
