# %% Corner Post: Counter-to-Mantel Section
# Parametric model of the 270° corner post

from build123d import *
from ocp_vscode import show
from math import cos, sin, radians

# === UNITS ===
INCH = 25.4  # mm

# === POST GEOMETRY (from CLAUDE.md) ===
ARC_ANGLE = 270  # degrees (360 - 90° corner)
POST_RADIUS = 1.7 * INCH  # outer radius of post
STRIP_COUNT = 9
STRIP_FACE_WIDTH = 13/16 * INCH  # visible face width
GROUT_GAP = 1/8 * INCH
TILE_THICKNESS = 0.25 * INCH

# === COUNTER-TO-MANTEL DIMENSIONS ===
TOTAL_HEIGHT = 28 * INCH

# Vertical sections (bottom to top)
BASE_HEIGHT = 1 * INCH
TIER1_HEIGHT = 10 * INCH
BASE2_HEIGHT = 1 * INCH
CAP_HEIGHT = 3 * INCH
TIER2_HEIGHT = TOTAL_HEIGHT - (BASE_HEIGHT + TIER1_HEIGHT + BASE2_HEIGHT + CAP_HEIGHT)

print("=== Counter-to-Mantel Corner Post ===")
print(f"Total height: {TOTAL_HEIGHT/INCH:.1f}\"")
print(f"  Base:    {BASE_HEIGHT/INCH:.1f}\"")
print(f"  Tier 1:  {TIER1_HEIGHT/INCH:.1f}\"")
print(f"  Base 2:  {BASE2_HEIGHT/INCH:.1f}\"")
print(f"  Tier 2:  {TIER2_HEIGHT/INCH:.1f}\"")
print(f"  Cap:     {CAP_HEIGHT/INCH:.1f}\"")
print(f"Post radius: {POST_RADIUS/INCH:.2f}\"")
print(f"Arc: {ARC_ANGLE}°")
print()

# %% Build the post profile
# Create 270° arc sections at each height

def make_arc_section(height, inner_radius, outer_radius, z_offset, name="section"):
    """Create a 270° arc tube section by subtracting wedge from annulus"""
    with BuildPart() as section:
        # Create full annulus (donut)
        with BuildSketch(Plane.XY.offset(z_offset)):
            Circle(outer_radius)
            Circle(inner_radius, mode=Mode.SUBTRACT)
        extrude(amount=height)

        # Subtract a 90° pie wedge to leave 270°
        # Gap faces into corner diagonal - rotated 45° right from before
        # Wedge spans from 135° to 225° (centered on 180°, the -X axis)
        wedge_radius = outer_radius * 1.5  # extend beyond the arc
        r = wedge_radius
        diag = r * 0.7071  # cos/sin of 45°
        with BuildSketch(Plane.XY.offset(z_offset - 1)):
            with BuildLine():
                # Triangle from center to 135° to 225° back to center
                Line((0, 0), (-diag, diag))      # to 135°
                Line((-diag, diag), (-diag, -diag))  # to 225°
                Line((-diag, -diag), (0, 0))     # back to center
            make_face()
        extrude(amount=height + 2, mode=Mode.SUBTRACT)

    return section.part

# Inner radius (post radius minus tile thickness)
INNER_RADIUS = POST_RADIUS - TILE_THICKNESS

# Build each section
z = 0

base = make_arc_section(BASE_HEIGHT, INNER_RADIUS * 0.95, POST_RADIUS * 1.02, z, "base")
z += BASE_HEIGHT

tier1 = make_arc_section(TIER1_HEIGHT, INNER_RADIUS, POST_RADIUS, z, "tier1")
z += TIER1_HEIGHT

base2 = make_arc_section(BASE2_HEIGHT, INNER_RADIUS * 0.95, POST_RADIUS * 1.02, z, "base2")
z += BASE2_HEIGHT

tier2 = make_arc_section(TIER2_HEIGHT, INNER_RADIUS, POST_RADIUS, z, "tier2")
z += TIER2_HEIGHT

cap = make_arc_section(CAP_HEIGHT, INNER_RADIUS * 0.95, POST_RADIUS * 1.02, z, "cap")

print("Sections created. Sending to viewer...")

# %% Display
# Show all sections with different colors
show(
    base, tier1, base2, tier2, cap,
    colors=["gray", "sienna", "gray", "sienna", "gray"],
    names=["Base (1\")", "Tier 1 (10\")", "Base 2 (1\")", "Tier 2 (13\")", "Cap (3\")"],
)

print("Done! Rotate view to see 270° arc profile.")
