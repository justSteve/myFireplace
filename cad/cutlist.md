# Corner Post Cutlist

Generated from `taper_demo.py` — dimensions rounded to 1/10"

## Summary

| Section | Height | Radius | Strip Width | Notes |
|---------|--------|--------|-------------|-------|
| Base1 | 1" | 4.0" + overhang | 1.5" | Constant, grout lines extend through |
| Tier1 | 8" | 4.0" → 2.8" | 1.5" → 1.0" | **Tapered**, 12 strips |
| Base2 | 1" | 2.8" + overhang | — | Constant, solid trim band |
| Tier2 | 15" | 2.5" | — | Constant, solid (no strips) |
| Cap | 3" | 2.5" + overhang | — | Constant, solid |

**Total height: 28"**

---

## Tier1 Strip Cutting

### Dimensions (per strip)
| Parameter | Value |
|-----------|-------|
| Bottom width | 1.5" |
| Top width | 1.0" |
| Height | 8" |
| Thickness | 0.25" (1/4") |
| Quantity | 12 strips × 4 corners = **48 strips** |

### Taper Geometry
- Width change: 1.5" → 1.0" over 8" height
- **Taper per side**: (1.5 - 1.0) / 2 / 8 = **0.031"/inch** = ~1/32" per inch
- **Taper angle**: arctan(0.031) = **1.8°**

### Grout Lines
- Width: 1/8" (0.125")
- 11 grout lines between 12 strips
- Grout extends continuously through Base1 and Tier1

---

## Cutting Notes

### Material
- Source tile: 8" × 36" × 0.25" wood-grain ceramic planks
- Strip height (8") matches tile width — cut across the 36" length
- At 1.5" strip width: 36" / 1.5" = **24 strips per tile**
- **Tiles needed for Tier1**: 48 strips ÷ 24 = **2 tiles** (+ spares)

### Taper Cutting Approach
The 1.8° taper is introduced by angling the tile on the bed fixture:
1. Tile sits on angled bed (1.8° relative to rail travel)
2. Each straight-line pass cuts at slight angle across tile face
3. Result: trapezoidal strip (wider at one end)

### Cut Sequence (per tile)
1. Set fence at 1.5" from blade
2. Cut full 8" width of tile (strip wide edge)
3. Advance tile, cut again — each pass produces one tapered strip
4. ~24 strips per 36" tile length (minus kerf losses)

### Edge Quality
- Use continuous-rim diamond blade (~0.045" kerf)
- Multiple shallow passes (2-3) for clean edges
- Wet cutting required for blade life and silica control

---

## Base1 Strips

Same width as Tier1 bottom (1.5") but constant (no taper):
- Height: 1"
- Width: 1.5"
- Quantity: 12 × 4 = **48 strips**
- These can be cut from Tier1 offcuts or tile ends

---

## Radii Reference

For layout and dry-fit verification:

| Location | Outer Radius | Inner Radius |
|----------|--------------|--------------|
| Base1/Tier1 bottom | 4.0" | 3.75" |
| Tier1 top / Base2 | 2.8" | 2.55" |
| Tier2 / Cap | 2.5" | 2.25" |

Arc span: 270° (leaving 90° corner behind)

---

## Open Questions

1. **Overhang dimension**: Currently 0.15" — round to 0.2" or keep as-is?
2. **Tier2 strips**: Currently solid — add segments to match Tier1 aesthetic?
3. **Base2 treatment**: Solid band or segmented to match?
4. **Horizontal grout lines**: Between tiers? At base/cap transitions?
