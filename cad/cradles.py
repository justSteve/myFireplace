"""
Corner Post Assembly Cradles - Tier1 and Tier2

Curved rails that cradle ceramic strips during glue-up.
- Strips stand vertically, arranged in arcs
- Rails wrap around strip OUTER faces (strips sit inside the rail arcs)

Tier1: TAPERED (4.0" → 2.8" radius), trapezoid strips, 3 glue-up batches of 4
Tier2: CONSTANT (2.5" radius), rectangular strips, 2 glue-up batches of 5
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
# SHARED PARAMETERS
# =============================================================================
STRIP_THICKNESS = 0.25 * IN
RAIL_SIZE = 0.5 * IN
GROUT_WIDTH = 0.125 * IN

# =============================================================================
# TIER1 PARAMETERS (tapered)
# =============================================================================
T1_HEIGHT = 8.0 * IN
T1_BOTTOM_WIDTH = 1.5 * IN
T1_TOP_WIDTH = 1.0 * IN
T1_BOTTOM_RADIUS = 4.0 * IN    # Outer face at bottom
T1_TOP_RADIUS = 2.8 * IN       # Outer face at top
T1_NUM_STRIPS = 4              # Per glue-up batch (3 batches for 12 total)

# Derived tier1 geometry
T1_TILT_RAD = math.atan2(T1_BOTTOM_RADIUS - T1_TOP_RADIUS, T1_HEIGHT)
T1_TILT_DEG = math.degrees(T1_TILT_RAD)
T1_TOP_Z = T1_HEIGHT * math.cos(T1_TILT_RAD)
T1_INNER_BOTTOM = T1_BOTTOM_RADIUS - STRIP_THICKNESS
T1_ANGLE_PER_STRIP = math.degrees(2 * math.asin(T1_BOTTOM_WIDTH / (2 * T1_INNER_BOTTOM)))

# =============================================================================
# TIER2 PARAMETERS (constant radius)
# =============================================================================
T2_HEIGHT = 10.0 * IN
T2_RADIUS = 2.0 * IN           # Outer face (constant)
T2_TOTAL_STRIPS = 9            # Full post
T2_NUM_STRIPS = 5              # Per glue-up batch (2 batches: 5+4)

# Derived tier2 geometry
T2_ARC_RADIANS = 270 * math.pi / 180
T2_ARC_LENGTH = T2_RADIUS * T2_ARC_RADIANS
T2_STRIP_WIDTH = (T2_ARC_LENGTH - (T2_TOTAL_STRIPS - 1) * GROUT_WIDTH) / T2_TOTAL_STRIPS
T2_ANGLE_PER_STRIP = math.degrees(2 * math.asin(T2_STRIP_WIDTH / (2 * T2_RADIUS)))


# =============================================================================
# GEOMETRY FUNCTIONS
# =============================================================================

def make_rail_arc(radius: float, z_pos: float, arc_degrees: float) -> Part:
    """Create curved rail at given radius and Z, centered on +X axis."""
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with Locations((radius, 0)):
                Rectangle(RAIL_SIZE, RAIL_SIZE)
        revolve(axis=Axis.Z, revolution_arc=arc_degrees)
    part = bp.part
    part = part.rotate(Axis.Z, -arc_degrees/2)
    part = part.move(Location((0, 0, z_pos)))
    return part


def make_tier1_strip(center_angle_deg: float) -> Part:
    """Tier1: tapered trapezoid strip."""
    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            Polygon([
                (-T1_BOTTOM_WIDTH/2, 0),
                (T1_BOTTOM_WIDTH/2, 0),
                (T1_TOP_WIDTH/2, T1_HEIGHT),
                (-T1_TOP_WIDTH/2, T1_HEIGHT)
            ])
        extrude(amount=STRIP_THICKNESS)

    part = bp.part
    part = part.move(Location((0, T1_HEIGHT/2, 0)))
    part = part.rotate(Axis.X, 90)
    part = part.rotate(Axis.Z, 90)
    part = part.move(Location((T1_BOTTOM_RADIUS - STRIP_THICKNESS, 0, 0)))

    # Tilt for taper
    part = part.move(Location((-T1_BOTTOM_RADIUS, 0, 0)))
    part = part.rotate(Axis.Y, -T1_TILT_DEG)
    part = part.move(Location((T1_BOTTOM_RADIUS, 0, 0)))

    part = part.rotate(Axis.Z, center_angle_deg)
    return part


def make_tier2_strip(center_angle_deg: float) -> Part:
    """Tier2: constant-width rectangular strip."""
    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            Rectangle(T2_STRIP_WIDTH, T2_HEIGHT)
        extrude(amount=STRIP_THICKNESS)

    part = bp.part
    part = part.move(Location((0, T2_HEIGHT/2, 0)))
    part = part.rotate(Axis.X, 90)
    part = part.rotate(Axis.Z, 90)
    part = part.move(Location((T2_RADIUS - STRIP_THICKNESS, 0, 0)))
    # No tilt needed
    part = part.rotate(Axis.Z, center_angle_deg)
    return part


# =============================================================================
# TIER1 GEOMETRY
# =============================================================================
t1_total_span = T1_NUM_STRIPS * T1_ANGLE_PER_STRIP
t1_start = -t1_total_span/2 + T1_ANGLE_PER_STRIP/2
t1_angles = [t1_start + i * T1_ANGLE_PER_STRIP for i in range(T1_NUM_STRIPS)]

t1_strips = [make_tier1_strip(a) for a in t1_angles]

t1_rail_arc = t1_total_span + 10
t1_bottom_rail = make_rail_arc(
    radius=T1_BOTTOM_RADIUS + RAIL_SIZE/2,
    z_pos=RAIL_SIZE/2,
    arc_degrees=t1_rail_arc
)
t1_top_rail = make_rail_arc(
    radius=T1_TOP_RADIUS + RAIL_SIZE/2,
    z_pos=T1_TOP_Z - RAIL_SIZE/2,
    arc_degrees=t1_rail_arc
)

# =============================================================================
# TIER2 GEOMETRY (offset in Y to separate from Tier1)
# =============================================================================
T2_OFFSET = 12 * IN  # Shift tier2 in Y direction

t2_total_span = T2_NUM_STRIPS * T2_ANGLE_PER_STRIP
t2_start = -t2_total_span/2 + T2_ANGLE_PER_STRIP/2
t2_angles = [t2_start + i * T2_ANGLE_PER_STRIP for i in range(T2_NUM_STRIPS)]

t2_strips = [make_tier2_strip(a).move(Location((0, T2_OFFSET, 0))) for a in t2_angles]

t2_rail_arc = t2_total_span + 10
t2_bottom_rail = make_rail_arc(
    radius=T2_RADIUS + RAIL_SIZE/2,
    z_pos=RAIL_SIZE/2,
    arc_degrees=t2_rail_arc
).move(Location((0, T2_OFFSET, 0)))

t2_top_rail = make_rail_arc(
    radius=T2_RADIUS + RAIL_SIZE/2,
    z_pos=T2_HEIGHT - RAIL_SIZE/2,
    arc_degrees=t2_rail_arc
).move(Location((0, T2_OFFSET, 0)))

# =============================================================================
# DISPLAY
# =============================================================================
# Tier1 group
show_object(t1_bottom_rail, name="T1_BOTTOM_RAIL", options={"color": (70, 130, 180)})
show_object(t1_top_rail, name="T1_TOP_RAIL", options={"color": (180, 130, 70)})
for i, s in enumerate(t1_strips):
    show_object(s, name=f"T1_Strip_{i+1}", options={"color": (210, 180, 140), "alpha": 0.7})

# Tier2 group
show_object(t2_bottom_rail, name="T2_BOTTOM_RAIL", options={"color": (100, 149, 237)})
show_object(t2_top_rail, name="T2_TOP_RAIL", options={"color": (205, 133, 63)})
for i, s in enumerate(t2_strips):
    show_object(s, name=f"T2_Strip_{i+1}", options={"color": (245, 222, 179), "alpha": 0.7})

# =============================================================================
# DEBUG
# =============================================================================
print(f"""
=== TIER1 Cradle (Tapered) ===
Strips: {T1_NUM_STRIPS} per batch (12 total, 3 batches)
Taper: R={T1_BOTTOM_RADIUS/IN:.1f}" → {T1_TOP_RADIUS/IN:.1f}", tilt {T1_TILT_DEG:.1f}°
Strip: {T1_BOTTOM_WIDTH/IN:.2f}" → {T1_TOP_WIDTH/IN:.2f}" W × {T1_HEIGHT/IN:.1f}" H
Rails: bottom R={((T1_BOTTOM_RADIUS + RAIL_SIZE/2)/IN):.2f}", top R={((T1_TOP_RADIUS + RAIL_SIZE/2)/IN):.2f}"

=== TIER2 Cradle (Constant) ===
Strips: {T2_NUM_STRIPS} per batch ({T2_TOTAL_STRIPS} total, 2 batches)
Radius: R={T2_RADIUS/IN:.1f}" (constant)
Strip: {T2_STRIP_WIDTH/IN:.2f}" W × {T2_HEIGHT/IN:.1f}" H
Rails: both R={((T2_RADIUS + RAIL_SIZE/2)/IN):.2f}"
""")

# =============================================================================
# EXPORTS
# =============================================================================
import os
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Tier1 rails (fabricate these)
export_step(t1_bottom_rail, os.path.join(EXPORT_DIR, "tier1_bottom_rail.step"))
export_step(t1_top_rail, os.path.join(EXPORT_DIR, "tier1_top_rail.step"))
print("Exported: tier1_bottom_rail.step, tier1_top_rail.step")

# Tier2 rails (fabricate these)
export_step(t2_bottom_rail, os.path.join(EXPORT_DIR, "tier2_bottom_rail.step"))
export_step(t2_top_rail, os.path.join(EXPORT_DIR, "tier2_top_rail.step"))
print("Exported: tier2_bottom_rail.step, tier2_top_rail.step")

# Full assembly for reference
t1_assembly = Compound(children=[t1_bottom_rail, t1_top_rail, *t1_strips])
t2_assembly = Compound(children=[t2_bottom_rail, t2_top_rail, *t2_strips])
export_step(t1_assembly, os.path.join(EXPORT_DIR, "tier1_cradle_assembly.step"))
export_step(t2_assembly, os.path.join(EXPORT_DIR, "tier2_cradle_assembly.step"))
print("Exported: tier1_cradle_assembly.step, tier2_cradle_assembly.step")
