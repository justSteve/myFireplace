# myFireplace - Custom Masonry Fireplace Insert Project

## Project Overview

Replacing an aging steel Heatilator-style insert with a custom-designed high-efficiency masonry firebox. The project prioritizes heating efficiency with potential hydronic integration to supplement an existing in-floor radiant system.

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

**Bead**: myStuff-4q2 | **Design doc**: `designs/ash-removal-system.md`

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

### Pending (requires demolition)
1. Actual convection channel dimensions and geometry
2. Condition of existing masonry behind steel insert
3. Confirm ~12" clearance above firebox to flue (estimated, may allow above-firebox secondary chamber)

### Design Decisions
1. Secondary combustion chamber placement (above vs. behind)
2. Heat exchanger type and placement (channels vs. exhaust path vs. both)
3. Liner diameter (depends on final design BTU output)
4. Balance between hydronic extraction vs. radiant room heat
5. Buffer tank sizing and placement in wood storage room

## Research Areas

- [ ] EPA-certified fireplace emission standards (may not apply to masonry heaters but good reference)
- [ ] Masonry heater design principles (Finnish contraflow, Russian stove concepts)
- [ ] Hydronic coil/jacket sizing for wood-fired systems
- [ ] Appropriate liner sizing for BTU output
- [ ] Secondary combustion chamber design parameters

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
