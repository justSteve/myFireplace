# Corner Post Geometry — 270° Ceramic Tile Wrap

## Problem

The fireplace exterior is clad with stacked ledgestone veneer (MSI Alaska Gray Ledger Panel). At outside corners — particularly under the vaulted ceiling — rough stone edges meet at angles that need a finished treatment. Standard corner trim doesn't exist for this stone profile.

## Solution

Ceramic tile strips arranged in a 270° arc to form rounded "post" effects that cap the imperfect corners. The post wraps the exposed 270° of the corner (360° minus the 90° that tucks into the wall junction behind).

## Material

- **Plank**: 7.875" × 24" × 0.25" wood-grain ceramic tile
- **Cut from**: Single plank ripped into parallel strips
- **Pattern**: Wood grain runs vertically (same as natural column/post)

## Geometry

### Strip Count and Width

From a 7.875" plank, accounting for 0.1" kerf per cut:

| Strips | Strip Width | Radius | Diameter | Notes |
|--------|------------|--------|----------|-------|
| 6 | 1-1/4" | 2.016" | 4.032" | Chunky, visible facets |
| 7 | 1-1/16" | 1.746" | 3.492" | Still visible facets |
| 8 | 15/16" | 1.581" | 3.163" | Approaching smooth |
| **9** | **13/16"** | **1.710"** | **3.420"** | **Recommended — reads as smooth curve** |
| 10 | 3/4" | 1.543" | 3.085" | At minimum width limit |

### Recommended Configuration

- **9 strips** at 13/16" face width
- **Radius**: ~1.7" (center to mid-thickness)
- **Diameter**: ~3.4" visible post
- **Arc angle per strip**: 30° (270° / 9)
- **Grout lines**: 1/8" between strips

At 30° per facet with 1/8" grout lines, the post reads as a continuous rounded surface from normal viewing distance.

### Vertical Tiers

- **Tier height**: 10" (tile cut to length)
- Tiers stack vertically with horizontal grout lines between
- Total post height determined by ceiling intersection

## Arc Calculation

The relationship between strip count, width, and resulting radius:

```
arc_length = n × strip_width + (n-1) × grout_width
radius = arc_length / arc_radians
arc_radians = 270° × π/180 = 4.712 rad
```

For 9 strips at 13/16" (0.8125") with 1/8" (0.125") grout:
```
arc_length = 9 × 0.8125 + 8 × 0.125 = 7.3125 + 1.0 = 8.3125"
radius = 8.3125 / 4.712 = 1.764"
```

## Taper (Under Investigation)

If the post tapers (wider at base, narrower at top), each strip must be cut with a slight taper along its 10" length. The taper angle is built into the cutting bed fixture rather than the carriage movement — the tile sits at an angle relative to the straight rail travel.

Taper geometry TBD pending final post diameter specifications at top and bottom.

## Cutting Method

Conventional wet tile saws produce unacceptable edge chipping on narrow strips (especially at 3/4" width on 1/4" thick ceramic). The solution is a **router-based cutting system** with diamond bits on SBR20 linear rails.

See: `router-sled-design.md`

## SketchUp Models

- `sketchup/corner_post.rb` — Strip calculator and 3D post model generator
  - Run `CornerPost.calculate` for strip options table
  - Run `CornerPost.build(9)` to generate 3D model with 9 strips
  - Includes reference walls at 50% opacity showing corner context

## Visualization

- `visualizations/tile-cutting-jig.html` — Interactive SVG showing the router sled concept with angled bed, rails, carriage, and tile positioning

## Open Questions

1. Final taper specification (degree of taper, if any)
2. Optimal grout color for wood-grain ceramic
3. Adhesive system for mounting strips to corner substrate
4. Whether bottom tier meets a baseboard or floor transition
5. Whether top tier meets ceiling trim or terminates with a cap
