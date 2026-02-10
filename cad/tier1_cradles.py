"""
Tier1 Assembly Cradles

Two curved rails that cradle tapered ceramic strips during glue-up.
- Strips stand vertically, arranged in an arc
- Strip OUTER faces form the post surface
- Rails wrap around strip OUTER faces (strips sit inside the rail arcs)
- Strips touch edge-to-edge

BUILD123D LESSONS LEARNED:
1. Build123d CENTERS geometry even when you specify coordinates from 0.
   - If you create a Polygon from Y=0 to Y=8", the result is Y=-4" to Y=+4"
   - FIX: After extrusion, shift by half the dimension: part.move(Location((0, HEIGHT/2, 0)))

2. Axis() with off-origin pivot points may not work as expected for rotations.
   - The Axis((point), (direction)) constructor creates an axis, but rotation behavior
     may differ from expectations.
   - FIX: Use translate-rotate-translate pattern:
     part.move(Location((-pivot_x, 0, 0)))  # Move pivot to origin
     part.rotate(Axis.Y, angle)              # Rotate around origin
     part.move(Location((pivot_x, 0, 0)))    # Move back

3. Build in Plane.XY then rotate to final orientation.
   - Using Plane.YZ or Plane.XZ directly can lead to confusion about coordinate mappings.
   - Clearer approach: Build in XY (the default/intuitive plane), then rotate to vertical:
     part.rotate(Axis.X, 90)  # Y becomes Z
     part.rotate(Axis.Z, 90)  # Reorient as needed

4. Debug by printing bounding boxes at each transformation step.
   - bb = part.bounding_box()
   - print(f"X: {bb.min.X} to {bb.max.X}, Y: ..., Z: ...")
   - This reveals exactly where geometry ends up vs. where you expected it.

5. Revolve around Axis.Z creates geometry where:
   - Sketch X coordinate becomes radial distance from Z axis
   - Sketch Z coordinate becomes 3D Z coordinate
   - Revolve arc starts at +X and goes CCW (looking down)
"""

import math
from build123d import *

try:
    from ocp_vscode import show_object, set_defaults, Camera
    set_defaults(reset_camera=Camera.KEEP)
except ImportError:
    def show_object(*args, **kwargs): pass

IN = 25.4

# =============================================================================
# STRIP DIMENSIONS (from cutlist)
# =============================================================================
STRIP_HEIGHT = 8.0 * IN
STRIP_BOTTOM_WIDTH = 1.5 * IN
STRIP_TOP_WIDTH = 1.0 * IN
STRIP_THICKNESS = 0.25 * IN

# =============================================================================
# POST GEOMETRY
# =============================================================================
POST_BOTTOM_RADIUS = 4.0 * IN   # Outer face of strips at bottom
POST_TOP_RADIUS = 2.8 * IN      # Outer face of strips at top
NUM_STRIPS = 4

# =============================================================================
# RAIL DIMENSIONS
# =============================================================================
RAIL_SIZE = 0.5 * IN  # Square cross-section

# =============================================================================
# DERIVED GEOMETRY
# =============================================================================
# Strip inner face radii (where rails contact)
INNER_BOTTOM_RADIUS = POST_BOTTOM_RADIUS - STRIP_THICKNESS
INNER_TOP_RADIUS = POST_TOP_RADIUS - STRIP_THICKNESS

# Tilt angle so strip top is at smaller radius than bottom
TILT_ANGLE_RAD = math.atan2(POST_BOTTOM_RADIUS - POST_TOP_RADIUS, STRIP_HEIGHT)
TILT_ANGLE_DEG = math.degrees(TILT_ANGLE_RAD)

# Strip top Z after tilting
TOP_Z = STRIP_HEIGHT * math.cos(TILT_ANGLE_RAD)

# Angular spacing for touching edges at INNER radius (where strips actually meet)
# chord = strip_width, so angle = 2 * arcsin(width / (2 * radius))
ANGLE_PER_STRIP = math.degrees(2 * math.asin(STRIP_BOTTOM_WIDTH / (2 * INNER_BOTTOM_RADIUS)))


def make_strip(center_angle_deg: float) -> Part:
    """Create one strip: trapezoid, tilted, positioned with outer face at post radius."""

    # Build in XY plane (horizontal), then rotate to vertical
    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            # X = width direction, Y = height direction
            Polygon([
                (-STRIP_BOTTOM_WIDTH/2, 0),
                (STRIP_BOTTOM_WIDTH/2, 0),
                (STRIP_TOP_WIDTH/2, STRIP_HEIGHT),
                (-STRIP_TOP_WIDTH/2, STRIP_HEIGHT)
            ])
        extrude(amount=STRIP_THICKNESS)

    part = bp.part

    # Build123d centers geometry - shift so Y goes 0 to HEIGHT
    part = part.move(Location((0, STRIP_HEIGHT/2, 0)))

    # Rotate to vertical: Y becomes Z (height)
    part = part.rotate(Axis.X, 90)

    # Rotate so thickness is radial: X becomes radial direction
    part = part.rotate(Axis.Z, 90)

    # Move so outer face is at POST_BOTTOM_RADIUS
    part = part.move(Location((POST_BOTTOM_RADIUS - STRIP_THICKNESS, 0, 0)))

    # TILT: rotate around bottom outer edge (X=POST_BOTTOM_RADIUS, Z=0)
    # Using translate-rotate-translate pattern
    part = part.move(Location((-POST_BOTTOM_RADIUS, 0, 0)))  # Move pivot to origin
    part = part.rotate(Axis.Y, -TILT_ANGLE_DEG)               # Tilt inward
    part = part.move(Location((POST_BOTTOM_RADIUS, 0, 0)))    # Move back

    # Rotate around Z to final angular position
    part = part.rotate(Axis.Z, center_angle_deg)

    return part


def make_rail_arc(radius: float, z_pos: float, arc_degrees: float) -> Part:
    """Create curved rail at given radius and Z, centered on +X axis."""
    # Rail cross-section centered at (radius, 0) in XZ plane
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with Locations((radius, 0)):
                Rectangle(RAIL_SIZE, RAIL_SIZE)
        revolve(axis=Axis.Z, revolution_arc=arc_degrees)

    part = bp.part
    # Center the arc on +X axis
    part = part.rotate(Axis.Z, -arc_degrees/2)
    # Move to correct Z
    part = part.move(Location((0, 0, z_pos)))
    return part


# =============================================================================
# CREATE GEOMETRY
# =============================================================================
# Strip angles - centered on +X axis
total_span = NUM_STRIPS * ANGLE_PER_STRIP
start_angle = -total_span/2 + ANGLE_PER_STRIP/2
strip_angles = [start_angle + i * ANGLE_PER_STRIP for i in range(NUM_STRIPS)]

strips = [make_strip(a) for a in strip_angles]

# Rails on OUTSIDE of arc - strips sit INSIDE the rail arcs
# Rail inner edge touches strip outer face
RAIL_ARC = total_span + 10  # Extra margin

# Bottom rail: centered at Z = RAIL_SIZE/2 so bottom sits on Z=0 plane
# Rail inner edge at POST_BOTTOM_RADIUS (strip outer face)
bottom_rail = make_rail_arc(
    radius=POST_BOTTOM_RADIUS + RAIL_SIZE/2,
    z_pos=RAIL_SIZE/2,
    arc_degrees=RAIL_ARC
)

# Top rail: top edge at TOP_Z
# Rail inner edge at POST_TOP_RADIUS (strip outer face at top)
top_rail = make_rail_arc(
    radius=POST_TOP_RADIUS + RAIL_SIZE/2,
    z_pos=TOP_Z - RAIL_SIZE/2,
    arc_degrees=RAIL_ARC
)

# =============================================================================
# DISPLAY
# =============================================================================
show_object(bottom_rail, name="BOTTOM_RAIL", options={"color": (70, 130, 180)})
show_object(top_rail, name="TOP_RAIL", options={"color": (180, 130, 70)})
for i, s in enumerate(strips):
    show_object(s, name=f"Strip_{i+1}", options={"color": (210, 180, 140), "alpha": 0.7})

# =============================================================================
# DEBUG
# =============================================================================
print(f"""
=== Tier1 Cradle ===
Strips: {NUM_STRIPS} at {ANGLE_PER_STRIP:.1f}° each = {total_span:.1f}° total
Tilt: {TILT_ANGLE_DEG:.1f}°

Strip outer face: bottom R={POST_BOTTOM_RADIUS/IN:.1f}", top R={POST_TOP_RADIUS/IN:.1f}"
Strip Z: 0" to ~{TOP_Z/IN:.1f}"
Bottom rail: Z=0" to 0.5", radius ~{(POST_BOTTOM_RADIUS + RAIL_SIZE/2)/IN:.1f}" (wraps outside strips)
Top rail: Z=~{(TOP_Z-RAIL_SIZE)/IN:.1f}" to ~{TOP_Z/IN:.1f}", radius ~{(POST_TOP_RADIUS + RAIL_SIZE/2)/IN:.1f}" (wraps outside strips)
""")
