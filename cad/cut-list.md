# Corner Post Cut List

Locked dimensions for precision cutting sled. Source: `cradles.py`

---

## Source Material

| Parameter | Value |
|-----------|-------|
| Tile size | 7.875" × 24" × 0.25" |
| Material | Wood-grain ceramic plank |
| Blade kerf | 0.045" (continuous-rim diamond) |

---

## Tier1 Strips (Tapered)

### Dimensions
| Parameter | Value |
|-----------|-------|
| Bottom width | 1.5" |
| Top width | 1.0" |
| Height | 8.0" |
| Thickness | 0.25" |
| Taper angle | **1.8°** |
| Quantity | 12 strips × 4 corners = **48 strips** |

### Taper Geometry
- Width change: 0.5" over 8" height
- Per edge: 0.25" / 8" = 0.031"/inch
- tan(1.8°) = 0.0314

### Yield per Tile
- Tile length: 24"
- Strip width (avg): 1.25"
- Strips per tile: ~18 (accounting for kerf)
- **Tiles needed**: 48 ÷ 18 = **3 tiles** (+ spares)

---

## Tier2 Strips (Parallel)

### Dimensions
| Parameter | Value |
|-----------|-------|
| Width | 0.58" (calculated from 270° arc at R=2.0") |
| Height | 10.0" |
| Thickness | 0.25" |
| Taper angle | **0°** (parallel cuts) |
| Quantity | 9 strips × 4 corners = **36 strips** |

### Yield per Tile
- Tile length: 24"
- Strip width: 0.58"
- Strips per tile: ~38 (accounting for kerf)
- **Tiles needed**: 36 ÷ 38 = **1 tile** (+ spares)

---

## Cutting Sled Configuration

### L-Frame Indexing System

The L-frame positions the tile relative to the fixed blade path. Two pins on the L-frame bottom drop into indexed holes on the bed.

| Parameter | Value | Notes |
|-----------|-------|-------|
| Pin diameter | 1/4" | Standard dowel |
| Pin spacing | 3" | Along L-frame arm |
| Hole spacing (Tier1) | 1.5" | Bottom width of strip |
| Hole spacing (Tier2) | 0.58" | Strip width |
| Lever arm | 6" | Distance from shim to cut line |

### Shim for Taper (Tier1 only)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Shim thickness | **3/16"** (0.1875") | 6" × tan(1.8°) = 0.188" |
| Material | Aluminum or steel shim stock | |
| Location | Under one leg of L-frame | |

**Workflow:**
- Shim IN → taper cut (narrow end up)
- Shim OUT → taper cut (narrow end down)
- Alternate each cut for nesting strips

### Tier2 Cutting (No Shim)

Remove shim entirely. All cuts are parallel.

---

## Cut Sequence

### Tier1 (48 tapered strips)

```
Pass 1: L at hole 1, no shim    → strip with narrow-up taper
Pass 2: L at hole 2, add shim   → strip with narrow-down taper
Pass 3: L at hole 3, no shim    → strip with narrow-up taper
...
```

Each tile yields ~18 strips. Process 3 tiles.

### Tier2 (36 parallel strips)

```
All passes: no shim, parallel cuts at 0.58" spacing
```

Single tile yields ~38 strips.

---

## Radii Reference

| Location | Outer Radius | Inner Radius | Arc |
|----------|--------------|--------------|-----|
| Tier1 bottom | 4.0" | 3.75" | 270° |
| Tier1 top | 2.8" | 2.55" | 270° |
| Tier2 | 2.0" | 1.75" | 270° |

---

## Grout Lines

| Parameter | Value |
|-----------|-------|
| Width | 1/8" (0.125") |
| Tier1 | 11 lines between 12 strips |
| Tier2 | 8 lines between 9 strips |

---

## Edge Quality Requirements

- Continuous-rim diamond blade (Montolit CGX or equivalent)
- Kerf: ~0.045"
- Multiple passes (2-3) for clean edges
- Wet cutting mandatory (blade life + silica control)
- Minimum strip width: 3/4" (below this, breakage risk)

---

## Open Questions

1. ~~Taper angle~~ → **1.8° locked**
2. ~~Shim thickness~~ → **3/16" locked**
3. Pin diameter preference: 1/4" or 3/8"?
4. Bed material: MDF, HDPE, aluminum?
5. Clamp design for L-frame arm (later)
