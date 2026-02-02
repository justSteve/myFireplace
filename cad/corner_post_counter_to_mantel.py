# %% Corner Post: Counter-to-Mantel Section
# Parametric model with TAPER - wider at bottom, narrower at top

from build123d import *
from ocp_vscode import show
from math import cos, sin, radians, pi

# === UNITS ===
INCH = 25.4  # mm

# === POST GEOMETRY ===
ARC_ANGLE = 270  # degrees (360 - 90° corner)
STRIP_COUNT = 9
GROUT_GAP = 1/8 * INCH
TILE_THICKNESS = 0.25 * INCH

# === TAPER: Two different radii ===
# Tier 1 (lower): wider plank, larger radius
TIER1_RADIUS = 2.1 * INCH

# Tier 2 (upper): standard 8" plank, smaller radius
TIER2_RADIUS = 1.7 * INCH

# === COUNTER-TO-MANTEL DIMENSIONS ===
TOTAL_HEIGHT = 28 * INCH

BASE_HEIGHT = 1 * INCH
TIER1_HEIGHT = 8 * INCH
BASE2_HEIGHT = 1 * INCH
CAP_HEIGHT = 3 * INCH
TIER2_HEIGHT = TOTAL_HEIGHT - (BASE_HEIGHT + TIER1_HEIGHT + BASE2_HEIGHT + CAP_HEIGHT)

print("=== Counter-to-Mantel Corner Post (TAPERED) ===")
print(f"Total height: {TOTAL_HEIGHT/INCH:.1f}\"")
print(f"  Base:    {BASE_HEIGHT/INCH:.1f}\" @ r={TIER1_RADIUS/INCH:.2f}\"")
print(f"  Tier 1:  {TIER1_HEIGHT/INCH:.1f}\" @ r={TIER1_RADIUS/INCH:.2f}\"")
print(f"  Base 2:  {BASE2_HEIGHT/INCH:.1f}\" (transition)")
print(f"  Tier 2:  {TIER2_HEIGHT/INCH:.1f}\" @ r={TIER2_RADIUS/INCH:.2f}\"")
print(f"  Cap:     {CAP_HEIGHT/INCH:.1f}\" @ r={TIER2_RADIUS/INCH:.2f}\"")
print()

# %% Helper: create 270° arc section
def make_arc_section(height, outer_radius, z_offset):
    """Create a 270° arc tube section"""
    inner_radius = outer_radius - TILE_THICKNESS

    with BuildPart() as section:
        with BuildSketch(Plane.XY.offset(z_offset)):
            Circle(outer_radius)
            Circle(inner_radius, mode=Mode.SUBTRACT)
        extrude(amount=height)

        # Remove 90° wedge (centered on 180°, the -X axis)
        r = outer_radius * 2
        diag = r * 0.7071
        with BuildSketch(Plane.XY.offset(z_offset - 1)):
            with BuildLine():
                Line((0, 0), (-diag, diag))      # to 135°
                Line((-diag, diag), (-diag, -diag))  # to 225°
                Line((-diag, -diag), (0, 0))     # back
            make_face()
        extrude(amount=height + 2, mode=Mode.SUBTRACT)

    return section.part

# %% Helper: create individual strips for a tier
def make_tier_with_strips(height, outer_radius, z_offset):
    """Create a tier as individual strip segments"""
    inner_radius = outer_radius - TILE_THICKNESS
    strips = []

    angle_per_strip = ARC_ANGLE / STRIP_COUNT  # 30°
    grout_angle = 1.0  # simplified: 1° gap between strips

    for i in range(STRIP_COUNT):
        # Strip angular range: from 135° going clockwise
        strip_start = 135 - (i * angle_per_strip)
        strip_end = strip_start - angle_per_strip + grout_angle

        with BuildPart() as strip:
            # Full annulus
            with BuildSketch(Plane.XY.offset(z_offset)):
                Circle(outer_radius)
                Circle(inner_radius, mode=Mode.SUBTRACT)
            extrude(amount=height)

            # Remove everything outside this strip
            r = outer_radius * 2

            # Wedge before strip (from 135° to strip_start)
            if strip_start < 135:
                with BuildSketch(Plane.XY.offset(z_offset - 0.5)):
                    with Locations((r/2 * cos(radians((135 + strip_start)/2)),
                                    r/2 * sin(radians((135 + strip_start)/2)))):
                        Rectangle(r, r, rotation=(135 + strip_start)/2 - 90)
                extrude(amount=height + 1, mode=Mode.SUBTRACT)

            # Wedge after strip (from strip_end to -135°)
            if strip_end > -135:
                with BuildSketch(Plane.XY.offset(z_offset - 0.5)):
                    with Locations((r/2 * cos(radians((strip_end + -135)/2)),
                                    r/2 * sin(radians((strip_end + -135)/2)))):
                        Rectangle(r, r, rotation=(strip_end + -135)/2 - 90)
                extrude(amount=height + 1, mode=Mode.SUBTRACT)

            # Always remove the corner gap (135° to 225°)
            diag = r * 0.7071
            with BuildSketch(Plane.XY.offset(z_offset - 0.5)):
                with BuildLine():
                    Line((0, 0), (-diag, diag))
                    Line((-diag, diag), (-diag, -diag))
                    Line((-diag, -diag), (0, 0))
                make_face()
            extrude(amount=height + 1, mode=Mode.SUBTRACT)

        strips.append(strip.part)

    return strips

# %% Build the tapered post
parts = []
colors = []
names = []
z = 0

# Base (wider)
print("Building base...")
base = make_arc_section(BASE_HEIGHT, TIER1_RADIUS * 1.02, z)
parts.append(base)
colors.append("slategray")
names.append(f"Base 1\" @ {TIER1_RADIUS/INCH:.1f}\"r")
z += BASE_HEIGHT

# Tier 1 (wider)
print("Building tier 1...")
tier1 = make_arc_section(TIER1_HEIGHT, TIER1_RADIUS, z)
parts.append(tier1)
colors.append("sienna")
names.append(f"Tier1 8\" @ {TIER1_RADIUS/INCH:.1f}\"r")
z += TIER1_HEIGHT

# Base 2 (transition)
print("Building base 2 (transition)...")
base2 = make_arc_section(BASE2_HEIGHT, (TIER1_RADIUS + TIER2_RADIUS) / 2, z)
parts.append(base2)
colors.append("darkgray")
names.append("Base2 1\" (transition)")
z += BASE2_HEIGHT

# Tier 2 (narrower)
print("Building tier 2...")
tier2 = make_arc_section(TIER2_HEIGHT, TIER2_RADIUS, z)
parts.append(tier2)
colors.append("peru")
names.append(f"Tier2 15\" @ {TIER2_RADIUS/INCH:.1f}\"r")
z += TIER2_HEIGHT

# Cap (narrower)
print("Building cap...")
cap = make_arc_section(CAP_HEIGHT, TIER2_RADIUS * 1.02, z)
parts.append(cap)
colors.append("dimgray")
names.append(f"Cap 3\" @ {TIER2_RADIUS/INCH:.1f}\"r")

print(f"\nTaper visible: {TIER1_RADIUS/INCH:.2f}\" → {TIER2_RADIUS/INCH:.2f}\" radius")
print("Sending to viewer...")

show(*parts, colors=colors, names=names)

print("Done! Note the wider base/tier1 vs narrower tier2/cap.")
