# %% Full 5-Section Model: Two tapered tiers with constant bases/cap
# Base1 → Tier1 (tapered) → Base2 → Tier2 (tapered) → Cap

from build123d import *
from ocp_vscode import show

INCH = 25.4

# Three radii for the taper progression (tier surfaces)
WIDE_RADIUS = 2.3 * INCH    # Tier1 bottom
MID_RADIUS = 1.9 * INCH     # Tier1 top = Tier2 bottom
NARROW_RADIUS = 1.5 * INCH  # Tier2 top
THICKNESS = 0.25 * INCH

# Overhang for bases/caps (creates trim/molding effect)
OVERHANG = 0.15 * INCH      # how much bases/caps extend beyond tiers

# Heights (total 28")
BASE1_HEIGHT = 1 * INCH
TIER1_HEIGHT = 8 * INCH      # tapered: WIDE → MID
BASE2_HEIGHT = 1 * INCH
TIER2_HEIGHT = 15 * INCH     # tapered: MID → NARROW
CAP_HEIGHT = 3 * INCH

TOTAL = BASE1_HEIGHT + TIER1_HEIGHT + BASE2_HEIGHT + TIER2_HEIGHT + CAP_HEIGHT

print("=== FULL 5-SECTION TAPERED MODEL WITH OVERHANGS ===")
print(f"Total height: {TOTAL/INCH:.0f}\"")
print(f"Overhang: {OVERHANG/INCH:.2f}\" (bases/caps extend beyond tiers)")
print()
print(f"1. Base1:  {BASE1_HEIGHT/INCH:.0f}\" @ r={WIDE_RADIUS/INCH:.1f}\" + {OVERHANG/INCH:.2f}\" overhang")
print(f"2. Tier1:  {TIER1_HEIGHT/INCH:.0f}\" @ r={WIDE_RADIUS/INCH:.1f}\" → {MID_RADIUS/INCH:.1f}\" (TAPERED)")
print(f"3. Base2:  {BASE2_HEIGHT/INCH:.0f}\" @ r={MID_RADIUS/INCH:.1f}\" + {OVERHANG/INCH:.2f}\" overhang")
print(f"4. Tier2:  {TIER2_HEIGHT/INCH:.0f}\" @ r={MID_RADIUS/INCH:.1f}\" → {NARROW_RADIUS/INCH:.1f}\" (TAPERED)")
print(f"5. Cap:    {CAP_HEIGHT/INCH:.0f}\" @ r={NARROW_RADIUS/INCH:.1f}\" + {OVERHANG/INCH:.2f}\" overhang")
print()

def make_constant_arc(height, radius, z_offset):
    """Constant-radius 270° arc (cylindrical)"""
    inner = radius - THICKNESS
    with BuildPart() as section:
        with BuildSketch(Plane.XY.offset(z_offset)):
            Circle(radius)
            Circle(inner, mode=Mode.SUBTRACT)
        extrude(amount=height)
        # Cut 90° wedge
        r = radius * 2
        diag = r * 0.7071
        with BuildSketch(Plane.XY.offset(z_offset - 1)):
            with BuildLine():
                Line((0, 0), (-diag, diag))
                Line((-diag, diag), (-diag, -diag))
                Line((-diag, -diag), (0, 0))
            make_face()
        extrude(amount=height + 2, mode=Mode.SUBTRACT)
    return section.part

def make_tapered_arc(height, bottom_radius, top_radius, z_offset):
    """Tapered 270° arc (lofted, angled surfaces)"""
    bottom_inner = bottom_radius - THICKNESS
    top_inner = top_radius - THICKNESS

    with BuildSketch(Plane.XY.offset(z_offset)) as bottom:
        Circle(bottom_radius)
        Circle(bottom_inner, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(z_offset + height)) as top:
        Circle(top_radius)
        Circle(top_inner, mode=Mode.SUBTRACT)

    with BuildPart() as tapered:
        loft([bottom.sketch, top.sketch])
        # Cut 90° wedge
        r = bottom_radius * 2
        diag = r * 0.7071
        with BuildSketch(Plane.XY.offset(z_offset - 1)):
            with BuildLine():
                Line((0, 0), (-diag, diag))
                Line((-diag, diag), (-diag, -diag))
                Line((-diag, -diag), (0, 0))
            make_face()
        extrude(amount=height + 2, mode=Mode.SUBTRACT)

    return tapered.part

# Build stack
z = 0
parts = []
colors = []
names = []

# 1. Base1 (constant, wide + overhang)
print("Building Base1...")
base1 = make_constant_arc(BASE1_HEIGHT, WIDE_RADIUS + OVERHANG, z)
parts.append(base1)
colors.append("slategray")
names.append(f"Base1 {BASE1_HEIGHT/INCH:.0f}\" (overhang)")
z += BASE1_HEIGHT

# 2. Tier1 (TAPERED wide → mid)
print("Building Tier1 (tapered)...")
tier1 = make_tapered_arc(TIER1_HEIGHT, WIDE_RADIUS, MID_RADIUS, z)
parts.append(tier1)
colors.append("sienna")
names.append(f"Tier1 {TIER1_HEIGHT/INCH:.0f}\" (TAPERED)")
z += TIER1_HEIGHT

# 3. Base2 (constant, mid + overhang - creates trim between tiers)
print("Building Base2...")
base2 = make_constant_arc(BASE2_HEIGHT, MID_RADIUS + OVERHANG, z)
parts.append(base2)
colors.append("darkgray")
names.append(f"Base2 {BASE2_HEIGHT/INCH:.0f}\" (overhang)")
z += BASE2_HEIGHT

# 4. Tier2 (TAPERED mid → narrow)
print("Building Tier2 (tapered)...")
tier2 = make_tapered_arc(TIER2_HEIGHT, MID_RADIUS, NARROW_RADIUS, z)
parts.append(tier2)
colors.append("peru")
names.append(f"Tier2 {TIER2_HEIGHT/INCH:.0f}\" (TAPERED)")
z += TIER2_HEIGHT

# 5. Cap (constant, narrow + overhang - crowns the top)
print("Building Cap...")
cap = make_constant_arc(CAP_HEIGHT, NARROW_RADIUS + OVERHANG, z)
parts.append(cap)
colors.append("dimgray")
names.append(f"Cap {CAP_HEIGHT/INCH:.0f}\" (overhang)")

print("\nSending to viewer...")
show(*parts, colors=colors, names=names)

print("Done! 5 sections: constant-tapered-constant-tapered-constant")
