# Precision Router Sled — SBR20 Linear Rail System

## Purpose

A manually operated precision cutting system designed to rip 1/4" ceramic tile into strips as narrow as 3/4" with clean, chip-free edges. Conventional wet tile saws produce unacceptable chipping at these narrow widths.

## Key Insight

The router approach with diamond bits cuts by abrasion rather than impact, producing dramatically cleaner edges on ceramic. The linear rail system constrains movement to a single axis, preventing the lateral wobble that causes chip-out.

## Hardware

### Linear Rails (Acquired)

- **Product**: VEVOR SBR20-1000mm Linear Rail Kit
- **Rails**: 2× SBR20 supported rails, 1000mm (39.37") long
- **Shaft diameter**: 20mm
- **Bearing blocks**: 4× SBR20UU (2 per rail)
- **Mounting**: Rails bolt to flat reference surface through pre-drilled holes

### Router

- Standard plunge router with 1/2" collet
- Diamond-coated router bits (1/4" or 3/8" cutting diameter)
- Variable speed control (slower speeds for ceramic)
- Plunge depth adjustment for multiple passes

## Design Concept

### Assembly Overview

```
[Side View]

   ┌──Router Motor──┐
   │                 │
   └───┤ Bit ├───────┘
       │     │
  ═════╪═════╪═════════  ← Carriage Plate (spans rails)
  ─────┼─────┼─────────  ← SBR20 Rails
       │     │
       │  ↓  │
  ─────┴─────┴─────────  ← Tile on Platen
  ═════════════════════  ← Angled Bed Frame
```

### Component Stack (top to bottom)

1. **Router** — Mounted to carriage plate, bit pointing down
2. **Carriage plate** — Aluminum plate bolted to 4 bearing blocks
3. **Bearing blocks** — Ride on SBR20 rails, single-axis constraint
4. **SBR20 rails** — Mounted to frame, establish the cut line
5. **Air gap** — Clearance for router bit and water
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
  - Center hole for router bit passage
  - Router base mounting holes
  - Handle attachment points

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

- Diamond bits require wet cutting
- Gravity-fed water from reservoir above
- Bed slopes slightly toward drain
- Tile on standoffs so water flows underneath
- Collection tray below catches slurry

## Build123d Modeling Plan

First models to generate once the environment is running:

1. **SBR20 rail and bearing block** — Accurate to datasheet dimensions
2. **Carriage plate** — With all mounting holes
3. **Platen assembly** — Work surface with fence and spacer provisions
4. **Angled bed frame** — Adjustable angle mechanism
5. **Complete assembly** — All components positioned, showing clearances

Each will be a parametric Python script. Change a dimension, re-run, see the update.

## Specifications to Confirm

- [ ] SBR20UU bearing block dimensions and bolt pattern (from VEVOR datasheet)
- [ ] Router base bolt pattern (model-specific)
- [ ] Diamond bit specifications (diameter, flute length, shank)
- [ ] Frame material and dimensions (steel tube size)
- [ ] Working height preference
- [ ] Platen material (aluminum, MDF, phenolic?)

## Cutting Parameters (To Test)

- Router speed: 10,000-15,000 RPM (diamond bits want slower speed)
- Feed rate: Manual, steady pressure
- Depth per pass: 1-2mm (3-4 passes for full 6mm tile)
- Water flow: Continuous drip, not stream
- Bit diameter: Start with 1/4" diamond core, test 3/8"

## SketchUp Models

- `sketchup/tile_cutting_jig.rb` — Parametric SketchUp model of the full jig assembly
  - Run `TileCuttingJig.build` in Ruby Console
  - All dimensions adjustable via constants at top of file

## Visualization

- `visualizations/tile-cutting-jig.html` — Annotated isometric SVG diagram
