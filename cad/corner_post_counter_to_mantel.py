# %% Full 5-Section Model: Two tapered tiers with constant bases/cap
# Base1 → Tier1 (tapered) → Base2 → Tier2 (constant) → Cap

from build123d import *
from ocp_vscode import show
import math

INCH = 25.4

# Tier1 strip parameters (rounded to 1/10")
N_STRIPS = 12
GROUT_WIDTH = 0.125 * INCH  # 1/8"

# Rounded dimensions for cutting
WIDE_RADIUS = 4.0 * INCH           # Tier1 bottom radius
TIER1_TOP = 2.8 * INCH             # Tier1 top radius
BOTTOM_STRIP_WIDTH = 1.5 * INCH    # Strip width at bottom
TOP_STRIP_WIDTH = 1.0 * INCH       # Strip width at top

# Tier2: constant radius (no taper)
TIER2_RADIUS = 2.5 * INCH
THICKNESS = 0.25 * INCH

# Overhang for bases/caps (creates trim/molding effect)
OVERHANG = 0.15 * INCH      # how much bases/caps extend beyond tiers

# Heights (total 28")
BASE1_HEIGHT = 1 * INCH
TIER1_HEIGHT = 8 * INCH      # tapered: WIDE → TIER1_TOP
BASE2_HEIGHT = 1 * INCH
TIER2_HEIGHT = 15 * INCH     # constant radius
CAP_HEIGHT = 3 * INCH

TOTAL = BASE1_HEIGHT + TIER1_HEIGHT + BASE2_HEIGHT + TIER2_HEIGHT + CAP_HEIGHT

print("=== FULL 5-SECTION MODEL WITH SEGMENTS ===")
print(f"Total height: {TOTAL/INCH:.0f}\"")
print(f"Tier1: {N_STRIPS} strips, {BOTTOM_STRIP_WIDTH/INCH:.2f}\" bottom → {TOP_STRIP_WIDTH/INCH:.2f}\" top, {GROUT_WIDTH/INCH:.3f}\" grout")
print(f"       Radii: {WIDE_RADIUS/INCH:.2f}\" → {TIER1_TOP/INCH:.2f}\" (tapered)")
print(f"Tier2: constant @ {TIER2_RADIUS/INCH:.2f}\" radius")
print()
print(f"1. Base1:  {BASE1_HEIGHT/INCH:.0f}\" @ r={WIDE_RADIUS/INCH:.2f}\" + overhang")
print(f"2. Tier1:  {TIER1_HEIGHT/INCH:.0f}\" @ r={WIDE_RADIUS/INCH:.2f}\" → {TIER1_TOP/INCH:.2f}\" ({N_STRIPS} SEGMENTS)")
print(f"3. Base2:  {BASE2_HEIGHT/INCH:.0f}\" @ r={TIER1_TOP/INCH:.2f}\" + overhang")
print(f"4. Tier2:  {TIER2_HEIGHT/INCH:.0f}\" @ r={TIER2_RADIUS/INCH:.2f}\" (constant)")
print(f"5. Cap:    {CAP_HEIGHT/INCH:.0f}\" @ r={TIER2_RADIUS/INCH:.2f}\" + overhang")
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

def make_tapered_strips(height, bottom_radius, top_radius, z_offset, n_strips, grout_width):
    """Create individual tapered strips by cutting grout lines through full arc"""
    # First create the full tapered arc
    full_arc = make_tapered_arc(height, bottom_radius, top_radius, z_offset)

    # Calculate circumferences
    bottom_circ = 2 * math.pi * bottom_radius * 0.75  # 270°
    top_circ = 2 * math.pi * top_radius * 0.75

    # Calculate strip widths (linear)
    bottom_strip_w = (bottom_circ - (n_strips - 1) * grout_width) / n_strips
    top_strip_w = (top_circ - (n_strips - 1) * grout_width) / n_strips

    # Convert to angular widths (degrees)
    bottom_strip_angle = (bottom_strip_w / bottom_circ) * 270
    bottom_grout_angle = (grout_width / bottom_circ) * 270
    top_strip_angle = (top_strip_w / top_circ) * 270
    top_grout_angle = (grout_width / top_circ) * 270

    # Cut grout lines (n_strips - 1 cuts)
    # Start at -135° to center the 270° arc around the -X axis
    bottom_angle = -135 + bottom_strip_angle  # After first strip
    top_angle = -135 + top_strip_angle

    r_cut = bottom_radius * 1.5  # Extend beyond arc

    strips = []
    remaining = full_arc

    for i in range(n_strips - 1):
        # Grout line center angles
        b_center = bottom_angle + bottom_grout_angle / 2
        t_center = top_angle + top_grout_angle / 2

        # Create a thin radial wedge to cut the grout line
        # Use average angle and cut a rectangular slot radially
        avg_angle = (b_center + t_center) / 2

        # Create grout cut as a box rotated to radial direction
        with BuildPart() as grout_cut:
            with BuildSketch(Plane.XY.offset(z_offset - 1)):
                with Locations((0, 0)):
                    Rectangle(r_cut, grout_width)
            extrude(amount=height + 2)

        grout_box = grout_cut.part.rotate(Axis.Z, avg_angle)
        remaining = remaining - grout_box

        # Advance to next grout position
        bottom_angle += bottom_strip_angle + bottom_grout_angle
        top_angle += top_strip_angle + top_grout_angle

    # Split into individual parts
    strips = remaining.solids()
    return list(strips)

# Build stack
z = 0
parts = []
colors = []
names = []

# 1 & 2. Base1 + Tier1 with continuous grout lines
print("Building Base1 + Tier1 with grout lines...")

# Build Base1 (constant) and Tier1 (tapered) as one unit, then cut grout
base1_z = z
base1 = make_constant_arc(BASE1_HEIGHT, WIDE_RADIUS + OVERHANG, base1_z)
tier1_z = z + BASE1_HEIGHT
tier1_full = make_tapered_arc(TIER1_HEIGHT, WIDE_RADIUS, TIER1_TOP, tier1_z)

# Calculate grout cut positions (same as in make_tapered_strips)
bottom_circ = 2 * math.pi * WIDE_RADIUS * 0.75
top_circ = 2 * math.pi * TIER1_TOP * 0.75
bottom_strip_w = (bottom_circ - (N_STRIPS - 1) * GROUT_WIDTH) / N_STRIPS
top_strip_w = (top_circ - (N_STRIPS - 1) * GROUT_WIDTH) / N_STRIPS
bottom_strip_angle = (bottom_strip_w / bottom_circ) * 270
bottom_grout_angle = (GROUT_WIDTH / bottom_circ) * 270
top_strip_angle = (top_strip_w / top_circ) * 270
top_grout_angle = (GROUT_WIDTH / top_circ) * 270

# Cut grout lines through both Base1 and Tier1
bottom_angle = -135 + bottom_strip_angle
top_angle = -135 + top_strip_angle
r_cut = (WIDE_RADIUS + OVERHANG) * 1.5
combined_height = BASE1_HEIGHT + TIER1_HEIGHT

remaining_base = base1
remaining_tier = tier1_full

for i in range(N_STRIPS - 1):
    b_center = bottom_angle + bottom_grout_angle / 2
    t_center = top_angle + top_grout_angle / 2
    avg_angle = (b_center + t_center) / 2

    with BuildPart() as grout_cut:
        with BuildSketch(Plane.XY.offset(base1_z - 1)):
            with Locations((0, 0)):
                Rectangle(r_cut, GROUT_WIDTH)
        extrude(amount=combined_height + 2)

    grout_box = grout_cut.part.rotate(Axis.Z, avg_angle)
    remaining_base = remaining_base - grout_box
    remaining_tier = remaining_tier - grout_box

    bottom_angle += bottom_strip_angle + bottom_grout_angle
    top_angle += top_strip_angle + top_grout_angle

# Add Base1 segments
for i, seg in enumerate(remaining_base.solids()):
    parts.append(seg)
    colors.append("slategray")
    names.append(f"Base1-{i+1}")

# Add Tier1 segments
for i, seg in enumerate(remaining_tier.solids()):
    parts.append(seg)
    colors.append("sienna")
    names.append(f"Strip {i+1}")

z += BASE1_HEIGHT + TIER1_HEIGHT

# 3. Base2 (constant, tier1_top + overhang - creates trim between tiers)
print("Building Base2...")
base2 = make_constant_arc(BASE2_HEIGHT, TIER1_TOP + OVERHANG, z)
parts.append(base2)
colors.append("darkgray")
names.append(f"Base2 {BASE2_HEIGHT/INCH:.0f}\" (overhang)")
z += BASE2_HEIGHT

# 4. Tier2 (CONSTANT at 2.5" radius)
print("Building Tier2 (constant)...")
tier2 = make_constant_arc(TIER2_HEIGHT, TIER2_RADIUS, z)
parts.append(tier2)
colors.append("peru")
names.append(f"Tier2 {TIER2_HEIGHT/INCH:.0f}\" (constant)")
z += TIER2_HEIGHT

# 5. Cap (constant, tier2 radius + overhang - crowns the top)
print("Building Cap...")
cap = make_constant_arc(CAP_HEIGHT, TIER2_RADIUS + OVERHANG, z)
parts.append(cap)
colors.append("dimgray")
names.append(f"Cap {CAP_HEIGHT/INCH:.0f}\" (overhang)")

print("\nSending to viewer...")
show(*parts, colors=colors, names=names)

print("Done! 5 sections with tapered Tier1 segments")
