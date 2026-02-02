# Session Handoff: Corner Post CAD Development
**Date**: 2026-02-01
**Final commit**: `21feafc`
**Status**: Working parametric model with tapers, overhangs, and tier offset

---

## Executive Summary

Established Build123d CAD environment and created a **fully parametric 5-section corner post model** demonstrating:
- True tapered geometry (lofted angled surfaces, not stepped)
- Trim/molding overhangs on bases and cap
- Distinct tier offset (0.2" step-in at tier transition)
- 270° arc oriented for right fireplace corner

**The model is ready for dimension refinement based on actual measurements.**

---

## Environment (VERIFIED WORKING)

| Component | Status | Location/Details |
|-----------|--------|------------------|
| WSL | ✅ | Ubuntu 24.04.3 LTS |
| Python venv | ✅ | `/root/cad/.venv` |
| Build123d | ✅ | Parametric BREP modeling |
| OCP CAD Viewer | ✅ | `bernhard-42.ocp-cad-viewer` |
| tmux session | ✅ | `cad-setup` |

**To resume**:
```bash
tmux attach -t cad-setup
# Then in VS Code: Ctrl+Shift+P → "OCP CAD Viewer: Open Viewer"
python /root/projects/myFireplace/cad/taper_demo.py
```

---

## Current Model: `cad/taper_demo.py`

### Geometry Specification

```
┌─────────────────────┐  Cap: 3" @ r=1.55" (1.4" + overhang)
│    ═══════════════  │
│         ╲     ╱     │  Tier2: 15" TAPERED 1.7" → 1.4"
│          ╲   ╱      │  (angled surfaces)
│           ╲ ╱       │
├───────────────────┤  Base2: 1" @ r=2.05" (1.9" + overhang)
│                     │  ════ 0.2" STEP-IN OFFSET ════
│      ╲         ╱    │  Tier1: 8" TAPERED 2.3" → 1.9"
│       ╲       ╱     │  (angled surfaces)
│        ╲     ╱      │
├─────────────────────┤  Base1: 1" @ r=2.45" (2.3" + overhang)
└─────────────────────┘
        TOTAL: 28"
```

### Key Parameters

```python
# Radii (4 distinct values)
WIDE_RADIUS = 2.3"      # Tier1 bottom
TIER1_TOP = 1.9"        # Tier1 top / Base2
TIER2_START = 1.7"      # Tier2 bottom (0.2" offset from Tier1 top)
NARROW_RADIUS = 1.4"    # Tier2 top / Cap

# Trim details
OVERHANG = 0.15"        # Bases/cap extend beyond tiers
THICKNESS = 0.25"       # Tile thickness

# Heights
BASE1 = 1", TIER1 = 8", BASE2 = 1", TIER2 = 15", CAP = 3"
TOTAL = 28"
```

### Technical Approach

1. **Constant sections** (bases/cap): Extruded 270° annulus
2. **Tapered sections** (tiers): Lofted between two different-radius annulus profiles
3. **90° wedge removal**: Triangle subtraction centered on 180° (into corner)
4. **Arc orientation**: Gap faces -X axis (into corner diagonal for right-side post)

---

## Files in Repository

### CAD Models
| File | Purpose | Status |
|------|---------|--------|
| `cad/taper_demo.py` | **Main model** - 5-section tapered post | ✅ Working |
| `cad/corner_post_counter_to_mantel.py` | Earlier iteration (stepped, not tapered) | Superseded |
| `cad/view_polycam_scan.py` | STL viewer for Polycam imports | ✅ Working |
| `cad/verify_install.py` | Environment verification | ✅ Working |

### Documentation
| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project overview, geometry specs, material notes |
| `docs/session-handoff-2026-02-01.md` | This file |
| `.vscode/cad-layout-profile.md` | Dual-monitor workflow |
| `.vscode/settings.json` | Workspace Python path, OCP port |

### Other
| File | Purpose |
|------|---------|
| `polycam/` | Scan files (gitignored, local only) |
| `.gitignore` | Excludes large STL/ZIP files |

---

## Git History This Session

```
21feafc - Corner post: add tier2 offset (0.2" step-in)
b95b08a - Corner post: 5-section model with tapers and overhangs
de95bda - Corner post: tapered model + session handoff documentation
fed0359 - WIP: Corner post counter-to-mantel section (draft)
8af7f91 - Add VS Code workspace settings and CAD layout profile
7474e62 - Exclude large Polycam scan files from repo
a8fe75e - Remove SketchUp, add Polycam viewer script
32a8843 - Mark Build123d environment setup complete
```

---

## What Was Accomplished

1. ✅ **Build123d environment** verified and documented
2. ✅ **OCP CAD Viewer** integration with dual-monitor workflow
3. ✅ **Polycam scan** imported but deemed insufficient for precision work
4. ✅ **Pivoted to declarative approach** - parametric model from dimensions
5. ✅ **270° arc geometry** correctly oriented for right corner
6. ✅ **True tapered surfaces** using loft operations (not stepped offsets)
7. ✅ **Trim overhangs** on bases and cap
8. ✅ **Tier offset** - visible step-in where tier2 starts narrower than tier1 ended

---

## Next Steps (Priority Order)

### Immediate
1. **Get actual measurements** for counter-to-mantel section
2. **Validate/adjust radii** to match real tile strip widths
3. **Add individual strip visualization** (9 segments per tier with grout gaps)

### Short-term
4. **Define floor-to-counter** section dimensions
5. **Define mantel-to-cap** section dimensions
6. **Mirror for left corner** (may be identical or reflected)

### Downstream
7. **Router sled design** for cutting strips (SBR20 hardware acquired)
8. **Export cut lists** with strip dimensions
9. **FreeCAD TechDraw** for dimensioned shop drawings

---

## Questions for Next Session

- What are the actual measurements for counter-to-mantel height and tier breaks?
- What plank widths are available? (affects achievable radii)
- Are left and right corners symmetric?
- Should base2 (the transition trim) be taller to accommodate the step-in offset?

---

## Technical Notes

### Why Loft Instead of Extrude?
Extrusion creates stepped cylinders. Lofting between two different-sized profiles creates true conical/tapered surfaces with angled walls.

### 270° Arc Construction
Build123d's wire-based arc construction had closure issues. Solution: create full annulus, then subtract a triangular 90° wedge.

### Coordinate System
- +Z = up (height)
- Arc gap faces -X direction (180°)
- For right corner: front facade at ~135°, side wall at ~-135°

---

*Session conducted with Claude Opus 4.5 via Claude Code CLI*
