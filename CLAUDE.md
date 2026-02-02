# myFireplace - Custom Masonry Fireplace Insert Project

## Project Overview

Replacing an aging steel Heatilator-style insert with a custom-designed high-efficiency masonry firebox. The project prioritizes heating efficiency with potential hydronic integration to supplement an existing in-floor radiant system.

This repo tracks two parallel workstreams plus shared tooling infrastructure:

1. **Interior Firebox** — Masonry firebox core, secondary combustion, hydronic integration
2. **Exterior Facade** — Stacked ledgestone veneer with precision ceramic tile corner posts
3. **3D Modeling Infrastructure** — Build123d + OCP CAD Viewer for precision drafting

## Repository Structure

```
myFireplace/
├── CLAUDE.md                    # This file — project index
├── designs/
│   ├── ash-removal-system.md    # Rear-access ash extraction
│   ├── corner-post-geometry.md  # 270° ceramic tile corner wraps
│   └── router-sled-design.md    # Precision cutting sled on SBR20 rails
├── docs/
│   ├── 3d-infrastructure-decision.md  # Build123d stack rationale
│   └── polycam-integration.md         # 3D scanning workflow
├── cad/
│   ├── README.md                # Environment setup instructions
│   ├── verify_install.py        # Build123d installation test
│   └── view_polycam_scan.py     # Load Polycam STL into viewer
├── polycam/
│   ├── 2_1_2026.stl             # Fireplace corner scan (mesh)
│   └── 2_1_2026.zip             # OBJ + texture export
└── visualizations/
    └── tile-cutting-jig.html   # Interactive SVG jig diagram
```

---

## Subproject: Exterior Facade — Corner Post System

**Design doc**: `designs/corner-post-geometry.md`

The fireplace exterior has been re-skinned with MSI Alaska Gray Ledger Panel (splitface marble, 6"×24"). The rough outside corners where stone meets at angles — particularly under the vaulted ceiling — need a finished treatment.

**Solution**: Ceramic tile strips arranged in 270° arcs to form rounded "post" effects that cap the imperfect corners. Each post is built from tiers of strips cut from 7.875" × 24" × 0.25" wood-grain ceramic planks.

### Key Geometry

- **Arc**: 270° (360° minus the 90° corner behind)
- **Strips per tier**: ~9 at 13/16" face width
- **Resulting radius**: ~1.7" (3.4" diameter post)
- **Tier height**: 10" tall segments stacked vertically
- **Grout lines**: 1/8" between strips
- **Minimum strip width**: 3/4" (below this, breakage risk during cutting)

### Cutting Challenge

Conventional wet tile saws produce unacceptable edge chipping on narrow strips. The solution is a router-based cutting system with diamond bits, using a precision sled constrained to linear rails.

**Taper design**: Under investigation. The bed fixture introduces the taper angle (tile angled relative to straight rail travel) rather than angled carriage movement. Each straight-line pass cuts at a slight angle across the tile face.

See: `designs/router-sled-design.md` for the SBR20 sled design.

---

## Subproject: Precision Router Sled

**Design doc**: `designs/router-sled-design.md`

A manually operated precision cutting system built on VEVOR SBR20-1000mm linear rails (2 rails, 4 SBR20UU bearing blocks). Designed to cut 1/4" ceramic tile into strips as narrow as 3/4" with clean edges.

### Components

- **Rails**: 2× SBR20-1000mm supported linear rails
- **Bearing blocks**: 4× SBR20UU linear bearing blocks
- **Carriage plate**: Aluminum, spans between rails, holds router
- **Platen**: Flat work surface below carriage
- **Angled bed frame**: Introduces taper angle for strip cuts
- **Fence**: Reference edge for indexing between strips
- **Water management**: Gravity-fed wet cutting with drain

### Status

Hardware (rails/bearings) acquired. Detailed design pending — this is the first target for the Build123d modeling environment.

---

## 3D Modeling Infrastructure

**Decision doc**: `docs/3d-infrastructure-decision.md`
**Setup guide**: `cad/README.md`

### Chosen Stack

**Build123d** (Python parametric BREP modeling) + **OCP CAD Viewer** (VS Code extension) + **WSL backend**

This gives code-on-left, interactive-3D-on-right inside VS Code. The model IS a Python script — AI generates it from narrative, human runs it (Shift+Enter), geometry appears in the viewer panel. Human orbits, zooms, clicks faces. Discussion happens. AI revises script. Human re-runs.

### Why This Stack

- Same OpenCascade kernel as FreeCAD/CATIA (real BREP, not meshes)
- Fully parametric via Python (loops, variables, functions)
- VS Code native (no context switching)
- Fillets, chamfers, sweeps, lofts (critical for post profiles)
- Exports: STEP, STL, DXF, SVG
- Zero cost (all MIT/open source)

### What Was Considered

- **CadQuery**: Same kernel, less readable API. Viable fallback.
- **FreeCAD**: Most capable GUI CAD. Use downstream for TechDraw dimensioned drawings.
- **OpenSCAD**: CSG-only, no fillets/chamfers. Insufficient.
- **SketchUp Pro**: Subscription expired. Was limited anyway — web version lacks scripting, desktop has no VS Code integration.

See decision doc for full scorecard and rationale.

### 3D Scanning — Polycam Integration

**Doc**: `docs/polycam-integration.md`

Polycam Basic subscription adds real-world-to-digital pipeline:
- Scan fireplace corners with phone → export as STL/OBJ
- Import into Build123d as reference geometry
- Design precision parts around actual scanned surfaces
- Verify fit before cutting tile

### Environment Setup Status

- [x] WSL version confirmed (Ubuntu 24.04.3 LTS)
- [x] VS Code WSL extension verified
- [x] Build123d + ocp-vscode installed in WSL venv (`/root/cad/.venv`)
- [x] OCP CAD Viewer extension installed (`bernhard-42.ocp-cad-viewer`)
- [x] Verification script (`cad/verify_install.py`) runs successfully
- [ ] Polycam scan exported and imported

---

## Existing Conditions

### Firebox Dimensions
- **Primary chamber**: 36"W x 24"D x 24"H
- **Convection channels**: ~10" additional depth on sides/back (TBD - requires demolition to confirm)
- **Total available depth**: ~34" (firebox + channels)

### Retained Components
- Ceramic glass doors (airtight, damper-controlled)
- Upgraded faceplate (cemented in place - installation from rear only)
- Outdoor combustion air intake (routed to front damper)

### Chimney
- Existing: 1 sq ft tile flue (~12" x 12")
- Geometry: Straight run through 2nd floor and minimal attic (no offsets)
- Planned: Add stainless steel liner (size TBD based on design)

### Structure
- Full masonry surround - no combustible clearance concerns
- Limited overhead clearance on front/visible side

### Facade (Previously Completed)

Exterior has been re-skinned with new facade over original red brick:

- **Front face**: 10" offset from original brick, clad with MSI Alaska Gray Ledger Panel (splitface marble, 6"x24")
- **Sides**: Ledger panel mortared directly to red brick
- **Front air channels**: Vents behind facade allow air to flow across front face and upward, routing surface heat to upstairs
- **Surface temps**: Front face exceeded 300°F during typical fire (before channeling)

**Implication for firebox design:**
No concern about insulating firebox from exterior. Full thermal mass approach is viable - maximize heat storage in masonry without worrying about overheating facade or surrounding structure. Ceramic fiber blanket between firebox and shell is for expansion tolerance, not heat protection.

## Design Goals (Priority Order)

1. **Heating efficiency** - Maximize BTU extraction per cord of wood
2. **Hydronic integration** - Supplement existing electric boiler radiant floor system
3. **Thermal mass** - Extended heat release after fire dies down
4. **Ambiance** - Secondary consideration but retain fire visibility through existing doors

## Location Context

- **Climate**: Wisconsin (design for -20°F to -30°F cold snaps)
- **Use case**: Supplemental heat for large multi-story home
- **Fuel**: Cord wood only

## Design Features Under Consideration

### Secondary Combustion Chamber

Route smoke through high-temperature zone (1100°F+) before flue exit. Captures unburned gases for additional heat (15-30% efficiency gain) and dramatically cleaner exhaust.

**Requirements:**
1. Sustained temperature 1100-1400°F (insulated refractory lining)
2. Secondary air injection (fresh O2 into hot zone)
3. Turbulence/dwell time (baffles for mixing)

**Placement options:**
- **Above firebox**: Natural draft assists; requires ~12" clearance (TBD after demo)
- **Behind firebox**: Uses rear channel space; needs strong draft or startup fan

**Secondary air source:**
Existing holes beneath front doors could route air to secondary chamber via channel through firebox walls. Preheating air en route improves combustion.

### Hydronic Heat Exchanger

**Existing radiant system:**
- Electric boiler ~30 feet from fireplace
- 3 manifolds, 4 zones each (12 zones total)
- Operating temperature: typically <150°F
- Fireplace location is "on the way" to manifold 2 (favorable routing)
- Loop type: Closed loop, no glycol (water only)

**Temperature considerations:**
- PEX rating: 180°F continuous, 200°F short-term peaks
- Wood-fired coils can produce 170-180°F or spike higher during active fire
- Thermostatic mixing valve required to temper hot output before entering PEX

**Safety: Overheat protection**
Risk: Fire burning + no circulation = water trapped in coil → localized boiling → steam/pressure spike

**Chosen approach: Continuous coil circulation**
- Circulation pump runs whenever fire is active (not tied to thermostat call)
- Fire detection via temperature sensor on coil outlet
- Pump activates when coil temp exceeds threshold (e.g., 100°F)
- Ensures heat always has somewhere to go

**Integration components:**
- **Thermostatic mixing valve**: Blend hot coil output with cooler return, protect PEX
- **Coil circulation pump**: Dedicated pump, temp-sensor activated
- **Check valve/isolation**: Prevent backflow when wood system inactive
- **Buffer tank** (optional but recommended): Thermal storage for extended heat after fire dies

**Open questions:**
- [ ] Determine heat exchanger placement: in convection channels vs. in exhaust path vs. both
- [ ] Buffer tank sizing (if included)
- [ ] Coil material selection (stainless vs. copper) based on placement

### Rear Ash Removal System

**Design doc**: `designs/ash-removal-system.md`

Rear-access ash removal enabling ash extraction while fire is burning. Key elements:
- Angled grate at rear of hearth (starts at floor level, slopes up to back wall)
- Wide shallow trough beneath grate (~24" × 8" × 4-5")
- Removable covered tray accessible from wood storage room
- Large coals prop on upward slope; cooled ash falls through bars

Status: Provisional design. Requires detailed fabrication drawings.

### Thermal Mass Integration
Potential to fill some/all convection channel space with firebrite, sand, or other thermal mass material for extended heat release.

### Masonry Firebox Core

Preference for firebrick/refractory construction over steel. DIY-feasible with masonry; metal fabrication reserved for specific components (heat exchanger, secondary combustion chamber liner if needed).

**Why masonry:**
- Heat retention: Firebrick absorbs heat during burn, radiates for hours after
- Durability: Quality firebrick lasts decades vs. steel warping/cracking
- DIY-friendly: Bricklaying is learnable, no welding required

#### Materials

| Material | Purpose | Notes |
|----------|---------|-------|
| Firebrick (dense) | Firebox walls, floor | 9"x4.5"x2.5" or 3" thick, rated 2300-3000°F |
| Refractory mortar | Joints | Thin 1/8" joints, NOT regular mortar |
| Castable refractory | Odd shapes, hearth base | Pourable/moldable, good for fills |
| Ceramic fiber blanket | Expansion gaps | 1-2" thick, 2300°F rated - NOT for insulation, allows thermal expansion |

*Note: Insulating firebrick (IFB) not needed - exterior heat is desirable for thermal mass distribution. Facade already handles heat routing to upstairs.*

#### Firebox Anatomy

```
         [to flue]
              │
    ┌─────────┴─────────┐
    │    (throat)       │  ← Transition to flue, ~12" above firebox
    ├───────────────────┤
    │                   │  ← Back wall (vertical or angled)
    │                   │
    │                   │  ← Side walls (4.5" firebrick)
    │                   │
    ├───────────────────┤  ← Hearth floor (firebrick on sand/castable)
    │///////////////////│
    └───────────────────┘
          [DOORS]
```

#### Interior Dimensions After Lining

With 4.5" firebrick walls:
- **Width**: 36" - (2 × 4.5") = **27" interior**
- **Depth**: 24" - 4.5" (back) = **19.5" interior**
- **Height**: 24" - 4.5" (floor) = **19.5" interior**

Still a generous firebox (~27" × 20" × 20"). Channel space (~10") reserved for secondary combustion / heat exchanger.

#### Construction Sequence (Rear Access)

1. **Hearth first** - Lay floor firebrick (may need to start from front before fully blocked)
2. **Walls from rear** - Stack courses working backward toward faceplate
3. **Expansion gap at front** - Ceramic fiber blanket where brick meets faceplate
4. **Back wall / throat** - Leave opening for flue; placeholder for secondary combustion
5. **Expansion gaps** - Ceramic fiber at shell contact points (thermal movement, not insulation)

#### DIY Requirements

**Skills:**
- Dry-fit everything before mortaring
- Keep joints thin (1/8")
- Soak firebrick briefly before laying
- Cure slowly with small fires over several days

**Tools:**
- Masonry trowel, brick hammer, chisel
- Angle grinder with masonry blade
- Level, square, string line
- Mixing tub, drill with paddle

## Physical Access

- **Installation**: From rear of firebox only (faceplate fixed)
- **Rear access**: 3' x 5' wood storage room (8' ceiling)
- **Wall construction**: 4" unfilled cinder block - jackhammer access feasible
- **Work space**: Excellent for construction, plumbing, and potential buffer tank placement

## Timeline

- **Current phase**: Research and design (Winter 2025-26)
- **Demolition/investigation**: Spring 2026
- **Construction**: TBD based on design finalization

## Open Questions

### Resolved
- [x] What's behind the fireplace? → 3x5 wood storage room, 4" cinder block wall
- [x] Flue geometry? → Straight run, no offsets
- [x] Boiler temp/zones? → <150°F, 12 zones across 3 manifolds, favorable routing to manifold 2
- [x] Loop type? → Closed loop, water only (no glycol)
- [x] Overheat protection? → Continuous coil circulation via temp-sensor activated pump
- [x] Corner post material? → 7.875" × 24" × 0.25" wood-grain ceramic planks
- [x] Corner post geometry? → 9 strips at 13/16", ~1.7" radius, 270° arc
- [x] 3D modeling stack? → Build123d + OCP CAD Viewer + WSL

### Pending (requires demolition)
1. Actual convection channel dimensions and geometry
2. Condition of existing masonry behind steel insert
3. Confirm ~12" clearance above firebox to flue (estimated, may allow above-firebox secondary chamber)

### Pending (requires setup)
1. ~~WSL environment details~~ → Ubuntu 24.04.3 LTS ✓
2. ~~VS Code WSL extension status~~ → Working ✓
3. ~~Build123d environment installation~~ → Verified ✓
4. Polycam scan export and import test

### Design Decisions
1. Secondary combustion chamber placement (above vs. behind)
2. Heat exchanger type and placement (channels vs. exhaust path vs. both)
3. Liner diameter (depends on final design BTU output)
4. Balance between hydronic extraction vs. radiant room heat
5. Buffer tank sizing and placement in wood storage room
6. Router sled taper angle (requires final post diameter confirmation)

## Research Areas

- [ ] EPA-certified fireplace emission standards (may not apply to masonry heaters but good reference)
- [ ] Masonry heater design principles (Finnish contraflow, Russian stove concepts)
- [ ] Hydronic coil/jacket sizing for wood-fired systems
- [ ] Appropriate liner sizing for BTU output
- [ ] Secondary combustion chamber design parameters
- [ ] Diamond router bit selection for ceramic tile
- [ ] SBR20 bearing block mounting patterns and tolerances

## Resources

### Reference Designs
- Finnish contraflow masonry heaters
- Tulikivi-style soapstone stoves
- Woodstock Soapstone secondary combustion approach
- Econoburn/Greenwood gasification boiler principles (for hydronic insights)

### Potential Contractors/Fabricators
- [ ] Local masonry heater guild members
- [ ] Custom metal fabrication shops (for heat exchanger, chamber components)

## Notes

This project explores applying modern wood-burning efficiency principles within the constraints of an existing masonry fireplace shell. The goal is not to replicate a commercial insert but to create a custom solution optimized for this specific installation.

The exterior facade work (corner posts) is a separate but related subproject that drives the precision tooling and 3D modeling infrastructure investment. The Build123d environment will serve both the ceramic tile cutting jig design and eventually the interior firebox component design.
