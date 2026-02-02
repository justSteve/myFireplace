# Session Handoff: Corner Post CAD Development
**Date**: 2026-02-01
**Context**: Build123d parametric modeling for ceramic tile corner posts

---

## Summary

Established a working CAD environment (Build123d + OCP CAD Viewer) and created the first parametric model for the **counter-to-mantel corner post section**. The model demonstrates a tapered 270° arc post with 5 vertical subsections.

---

## Environment Setup (COMPLETE)

| Component | Status | Details |
|-----------|--------|---------|
| WSL | ✅ | Ubuntu 24.04.3 LTS |
| Python venv | ✅ | `/root/cad/.venv` |
| Build123d | ✅ | Installed, verified |
| OCP CAD Viewer | ✅ | Extension `bernhard-42.ocp-cad-viewer` |
| tmux session | ✅ | `cad-setup` - attach with `tmux attach -t cad-setup` |
| Polycam scan | ⚠️ | Imported but too low-res for precision work; pivoted to declarative approach |

**Workspace layout**: Dual-monitor setup documented in `.vscode/cad-layout-profile.md`
- Left monitor: VS Code with Claude Code chat
- Right monitor: OCP CAD Viewer (full screen)

---

## Corner Post Project Structure

### The 6 Post Sections (left & right corners)

| Section | Height | Status |
|---------|--------|--------|
| Floor → Counter | TBD | Not started |
| **Counter → Mantel** | **28"** | **IN PROGRESS** |
| Mantel → Cap | TBD | Not started |

### Counter-to-Mantel Breakdown (current focus)

```
┌─────────────────┐  ← Cap: 3" @ r=1.7"
│                 │
│     Tier 2      │  ← 15" @ r=1.7" (standard 8" plank)
│                 │
├─────────────────┤  ← Base 2: 1" (transition ~1.9"r)
│                 │
│     Tier 1      │  ← 8" @ r=2.1" (wider plank needed)
│                 │
├─────────────────┤  ← Base: 1" @ r=2.1"
└─────────────────┘
     Total: 28"
```

### Taper Rationale

- **Tier 1 (bottom)**: Wider radius (2.1") requires strips from wider plank material
- **Tier 2 (top)**: Standard radius (1.7") uses strips from standard 8" ceramic planks
- **Transition**: Base 2 provides visual step-down between radii
- Both tiers use **9 strips** over **270°** arc

---

## Key Geometry Parameters

From `CLAUDE.md` and refined during session:

```python
ARC_ANGLE = 270°          # 360° - 90° corner
STRIP_COUNT = 9           # strips per tier
GROUT_GAP = 1/8"         # between strips
TILE_THICKNESS = 0.25"   # ceramic plank thickness

TIER1_RADIUS = 2.1"      # wider (bottom)
TIER2_RADIUS = 1.7"      # narrower (top)
```

---

## Files Created/Modified

### New Files
- `cad/corner_post_counter_to_mantel.py` — Main parametric model
- `cad/view_polycam_scan.py` — STL viewer (Polycam imports)
- `.vscode/settings.json` — Workspace settings
- `.vscode/cad-layout-profile.md` — Dual-monitor layout docs
- `.gitignore` — Excludes large Polycam files

### Modified Files
- `CLAUDE.md` — Updated environment checklist, removed SketchUp refs
- `cad/verify_install.py` — Simplified show() call

---

## Git Commits This Session

1. `32a8843` — Mark Build123d environment setup complete
2. `a8fe75e` — Remove SketchUp, add Polycam viewer script
3. `7474e62` — Exclude large Polycam scan files from repo
4. `8af7f91` — Add VS Code workspace settings and CAD layout profile
5. `fed0359` — WIP: Corner post counter-to-mantel section (draft)
6. *(uncommitted)* — Tapered model with 2.1" → 1.7" radius

---

## Next Steps (Priority Order)

### Immediate
1. **Commit current tapered model** — Capture the 2.1" → 1.7" taper
2. **Add individual strip rendering** — Show 9 segments per tier with grout gaps
3. **Validate strip widths** — Calculate actual face widths for each radius

### Short-term
4. **Define floor-to-counter section** — Get dimensions from user
5. **Define mantel-to-cap section** — Get dimensions from user
6. **Mirror geometry for left corner** — May be identical or reflected

### Downstream
7. **Router sled design** — SBR20 rail system for cutting strips (hardware acquired)
8. **Export cut lists** — Generate strip dimensions for fabrication
9. **FreeCAD integration** — TechDraw for dimensioned shop drawings

---

## Technical Notes

### 270° Arc Orientation
The arc is oriented for the **right corner** of the fireplace when viewed from the front:
- Arc starts at front facade (135°)
- Wraps around outside corner clockwise
- Ends at side wall (-135°)
- 90° gap faces INTO the corner diagonal (180° / -X axis)

### Build123d Approach
Using **annulus minus wedge** subtraction method for reliable arc creation:
```python
# Full donut
Circle(outer_radius)
Circle(inner_radius, mode=Mode.SUBTRACT)
# Subtract triangular wedge for 90° gap
```

Direct arc wire construction caused `TopoDS::Face` errors due to wire closure issues.

---

## To Resume Work

1. Open VS Code to `/root/projects/myFireplace`
2. Attach tmux: `tmux attach -t cad-setup`
3. Open OCP Viewer: Ctrl+Shift+P → "OCP CAD Viewer: Open Viewer"
4. Pop viewer to right monitor
5. Run: `python cad/corner_post_counter_to_mantel.py`

---

## Questions for Next Session

- Dimensions for floor-to-counter section?
- Dimensions for mantel-to-cap section?
- Are left and right corners mirror images or identical?
- Exact plank dimensions available for tier 1 (wider strips)?
