"""
Angle Grinder Mount for Precision Cutting Sled
===============================================

Mounts a Makita 4.5" angle grinder to the SBR20 rail carriage plate.

Design features:
- 1/4" steel base plate with kerf slot
- L-brackets bolted through grinder's M10 threaded handle holes
- Shaft collar/brace at original guard mount location
- Bottom 1/3 of blade protrudes below base into wet cutting zone

CRITICAL: Measure your grinder and update parameters before fabrication!

Run with Shift+Enter in VS Code with OCP CAD Viewer extension.
"""

from build123d import *
from math import pi, cos, sin

# Handle OCP CAD Viewer import (works in VS Code, graceful fallback otherwise)
try:
    from ocp_vscode import show, show_object, set_defaults, Camera
    set_defaults(reset_camera=Camera.KEEP)
    HAS_VIEWER = True
except ImportError:
    def show(*args, **kwargs): pass
    def show_object(*args, **kwargs): pass
    HAS_VIEWER = False

# =============================================================================
# PARAMETERS — MEASURE YOUR MAKITA AND UPDATE THESE VALUES
# =============================================================================

# Makita 4.5" grinder reference dimensions (GA4530 / similar)
# These are ESTIMATES - measure your actual grinder!

# Gear head (front section with handle holes)
GEAR_HEAD_DIA = 65.0           # mm - diameter of gear housing (measure across widest part)
GEAR_HEAD_LENGTH = 45.0        # mm - length of gear head section

# Handle mounting holes (M10 threaded holes on either side)
HANDLE_THREAD = 10.0           # mm - M10 thread
HANDLE_HOLE_SPACING = 65.0     # mm - CENTER-TO-CENTER across gear head (MEASURE THIS!)
HANDLE_HOLE_HEIGHT = 32.0      # mm - height of hole center above spindle centerline

# Motor body (barrel section behind gear head)
MOTOR_BODY_DIA = 57.0          # mm - barrel grip diameter (MEASURE THIS!)
MOTOR_BODY_LENGTH = 180.0      # mm - length from gear head to rear

# Guard collar (where original blade guard clamps)
COLLAR_RING_DIA = 58.0         # mm - OD of the guard clamp collar on grinder
COLLAR_DIST_FROM_BLADE = 12.0  # mm - distance from blade face to collar center

# Blade
BLADE_DIA = 115.0              # mm - 4.5" blade
BLADE_THICKNESS = 1.5          # mm - continuous rim diamond blade
SPINDLE_DIA = 22.0             # mm - M14 spindle flange area

# =============================================================================
# MOUNT DESIGN PARAMETERS
# =============================================================================

# Base plate
BASE_THICKNESS = 6.35          # mm - 1/4" steel
BASE_LENGTH = 160.0            # mm - along blade travel direction (X)
BASE_WIDTH = 100.0             # mm - perpendicular to travel (Y)

# L-bracket dimensions
BRACKET_STEEL = 6.35           # mm - 1/4" steel for brackets
BRACKET_WIDTH = 30.0           # mm - width of bracket in Y direction
BRACKET_STANDOFF = 5.0         # mm - gap between bracket and gear head for clearance

# Kerf slot (for blade passage through base)
KERF_SLOT_WIDTH = 4.0          # mm - blade thickness + clearance
KERF_SLOT_LENGTH = BASE_LENGTH - 20  # mm - nearly full length

# Blade exposure (bottom 1/3 below base plate)
BLADE_EXPOSURE = BLADE_DIA / 3  # mm - ~38mm for 115mm blade

# =============================================================================
# DERIVED DIMENSIONS
# =============================================================================

# Calculate blade centerline height above base bottom (Z=0)
# We want BLADE_EXPOSURE mm of blade below base bottom
# Blade bottom = BLADE_CENTER_Z - BLADE_DIA/2 = -BLADE_EXPOSURE
# Solving: BLADE_CENTER_Z = BLADE_DIA/2 - BLADE_EXPOSURE
BLADE_CENTER_Z = (BLADE_DIA / 2) - BLADE_EXPOSURE

# L-bracket vertical height (from base top to handle hole center)
BRACKET_VERTICAL = HANDLE_HOLE_HEIGHT + BLADE_CENTER_Z - BASE_THICKNESS

# Bracket horizontal reach (from edge toward grinder)
BRACKET_HORIZONTAL = (HANDLE_HOLE_SPACING / 2) - (GEAR_HEAD_DIA / 2) + BRACKET_STANDOFF + 15

# =============================================================================
# BASE PLATE
# =============================================================================

with BuildPart() as base_plate:
    # Main plate - centered at origin
    with BuildSketch(Plane.XY):
        Rectangle(BASE_LENGTH, BASE_WIDTH)
    extrude(amount=BASE_THICKNESS)

    # Kerf slot for blade passage (centered, along X axis)
    with BuildSketch(Plane.XY.offset(BASE_THICKNESS)):
        SlotOverall(KERF_SLOT_LENGTH, KERF_SLOT_WIDTH)
    extrude(amount=-BASE_THICKNESS, mode=Mode.SUBTRACT)

    # Corner mounting holes for attachment to carriage plate
    hole_inset = 12.0
    with BuildSketch(Plane.XY.offset(BASE_THICKNESS)):
        with Locations([
            (BASE_LENGTH/2 - hole_inset, BASE_WIDTH/2 - hole_inset),
            (BASE_LENGTH/2 - hole_inset, -BASE_WIDTH/2 + hole_inset),
            (-BASE_LENGTH/2 + hole_inset, BASE_WIDTH/2 - hole_inset),
            (-BASE_LENGTH/2 + hole_inset, -BASE_WIDTH/2 + hole_inset),
        ]):
            Circle(4.25)  # 8.5mm clearance holes for M8 bolts
    extrude(amount=-BASE_THICKNESS, mode=Mode.SUBTRACT)

base = base_plate.part

# =============================================================================
# L-BRACKETS (bolted to grinder handle holes, welded to base)
# =============================================================================

def make_bracket():
    """Create L-bracket profile for grinder mounting."""
    with BuildPart() as bracket:
        # L-profile in XZ plane
        with BuildSketch(Plane.XZ):
            with BuildLine():
                # Horizontal leg (sits on base plate)
                Polyline([
                    (0, 0),
                    (BRACKET_HORIZONTAL, 0),
                    (BRACKET_HORIZONTAL, BRACKET_VERTICAL),
                    (BRACKET_HORIZONTAL - BRACKET_STEEL, BRACKET_VERTICAL),
                    (BRACKET_HORIZONTAL - BRACKET_STEEL, BRACKET_STEEL),
                    (0, BRACKET_STEEL),
                ], close=True)
            make_face()
        extrude(amount=BRACKET_WIDTH)

        # M10 clearance hole at top for grinder handle thread
        hole_x = BRACKET_HORIZONTAL - BRACKET_STEEL / 2
        hole_z = BRACKET_VERTICAL
        with BuildSketch(Plane.XY.offset(hole_z)):
            with Locations((hole_x, BRACKET_WIDTH / 2)):
                Circle(HANDLE_THREAD / 2 + 0.5)  # M10 + clearance
        extrude(amount=-BRACKET_STEEL, mode=Mode.SUBTRACT)

    return bracket.part

# Create and position brackets
left_bracket = make_bracket()
left_bracket = left_bracket.move(Location((0, HANDLE_HOLE_SPACING/2 - BRACKET_WIDTH/2, BASE_THICKNESS)))

right_bracket = mirror(make_bracket(), about=Plane.XZ)
right_bracket = right_bracket.move(Location((0, -HANDLE_HOLE_SPACING/2 + BRACKET_WIDTH/2, BASE_THICKNESS)))

# =============================================================================
# SHAFT COLLAR / BRACE (clamps around motor body at guard mount location)
# =============================================================================

with BuildPart() as collar_brace:
    # Split collar ring
    collar_id = MOTOR_BODY_DIA + 1.0   # clearance
    collar_od = MOTOR_BODY_DIA + 14.0  # 6.5mm wall
    collar_width = 25.0

    with BuildSketch(Plane.YZ):
        Circle(collar_od / 2)
        Circle(collar_id / 2, mode=Mode.SUBTRACT)
        # Split gap at top
        with Locations((0, collar_od/2)):
            Rectangle(10, 12, mode=Mode.SUBTRACT)
    extrude(amount=collar_width)

    # Clamp ears with bolt holes
    ear_height = 20.0
    ear_width = 25.0
    with BuildSketch(Plane.YZ):
        with Locations([(-collar_od/2 - ear_width/2 + 5, collar_od/2 + ear_height/2 - 3)]):
            Rectangle(ear_width, ear_height)
        with Locations([(collar_od/2 + ear_width/2 - 5, collar_od/2 + ear_height/2 - 3)]):
            Rectangle(ear_width, ear_height)
    extrude(amount=collar_width)

    # M6 bolt holes through ears
    with BuildSketch(Plane.XY.offset(collar_width/2)):
        with Locations([(-collar_od/2 - 8, collar_od/2 + 8),
                        (collar_od/2 + 8, collar_od/2 + 8)]):
            Circle(3.5)  # M6 clearance
    extrude(amount=-collar_width, mode=Mode.SUBTRACT)

    # Support legs down to base plate
    leg_height = BLADE_CENTER_Z - BASE_THICKNESS
    leg_width = 12.0
    with BuildSketch(Plane.YZ):
        # Left leg
        with Locations([(-collar_od/2 - leg_width/2 + 3, -leg_height/2 - collar_od/4)]):
            Rectangle(leg_width, leg_height + collar_od/2)
        # Right leg
        with Locations([(collar_od/2 + leg_width/2 - 3, -leg_height/2 - collar_od/4)]):
            Rectangle(leg_width, leg_height + collar_od/2)
    extrude(amount=collar_width)

# Position collar at guard mount location
collar_x = -COLLAR_DIST_FROM_BLADE - collar_width/2
shaft_collar = collar_brace.part.move(Location((collar_x, 0, BLADE_CENTER_Z)))

# =============================================================================
# GRINDER REFERENCE GEOMETRY (detailed for visualization)
# =============================================================================

# Gear head - more realistic shape with flats for handle holes
with BuildPart() as gear_head_ref:
    # Main gear housing - slightly flattened on sides where handle holes are
    with BuildSketch(Plane.YZ):
        # Rounded rectangle profile (gear head isn't perfectly round)
        RectangleRounded(GEAR_HEAD_DIA, GEAR_HEAD_DIA * 0.85, radius=GEAR_HEAD_DIA * 0.3)
    extrude(amount=-GEAR_HEAD_LENGTH)

    # Spindle boss (front protrusion where blade mounts)
    with BuildSketch(Plane.YZ):
        Circle(SPINDLE_DIA / 2 + 5)
    extrude(amount=8)

    # LEFT SIDE M10 threaded hole (this is what we bolt through!)
    # Hole goes INTO the gear head from the left side
    with BuildSketch(Plane.XZ.offset(GEAR_HEAD_DIA / 2)):
        with Locations((-GEAR_HEAD_LENGTH / 2, HANDLE_HOLE_HEIGHT)):
            Circle(HANDLE_THREAD / 2)
    extrude(amount=-15, mode=Mode.SUBTRACT)  # blind hole ~15mm deep

    # RIGHT SIDE M10 threaded hole (mirror of left)
    with BuildSketch(Plane.XZ.offset(-GEAR_HEAD_DIA / 2)):
        with Locations((-GEAR_HEAD_LENGTH / 2, HANDLE_HOLE_HEIGHT)):
            Circle(HANDLE_THREAD / 2)
    extrude(amount=15, mode=Mode.SUBTRACT)  # blind hole ~15mm deep

gear_head = gear_head_ref.part.move(Location((0, 0, BLADE_CENTER_Z)))

# Motor body (barrel you grip)
with BuildPart() as motor_ref:
    with BuildSketch(Plane.YZ):
        Circle(MOTOR_BODY_DIA / 2)
    extrude(amount=-MOTOR_BODY_LENGTH)

    # Collar ring where guard clamps (raised ring)
    collar_x = -COLLAR_DIST_FROM_BLADE
    with BuildSketch(Plane.YZ.offset(collar_x)):
        Circle(COLLAR_RING_DIA / 2 + 2)
        Circle(MOTOR_BODY_DIA / 2, mode=Mode.SUBTRACT)
    extrude(amount=8)

motor_body = motor_ref.part.move(Location((-GEAR_HEAD_LENGTH, 0, BLADE_CENTER_Z)))

# Blade (disc with arbor hole)
with BuildPart() as blade_ref:
    with BuildSketch(Plane.YZ):
        Circle(BLADE_DIA / 2)
        Circle(SPINDLE_DIA / 2, mode=Mode.SUBTRACT)
    extrude(amount=BLADE_THICKNESS)

blade = blade_ref.part.move(Location((BLADE_THICKNESS/2, 0, BLADE_CENTER_Z)))

# M10 BOLTS (show the bolts that go through brackets into grinder)
with BuildPart() as bolt_left_ref:
    # Bolt head
    with BuildSketch(Plane.XZ):
        RegularPolygon(radius=8, side_count=6)  # M10 hex head ~16mm across flats
    extrude(amount=7)
    # Bolt shank
    with BuildSketch(Plane.XZ):
        Circle(HANDLE_THREAD / 2)
    extrude(amount=-30)  # through bracket into grinder

bolt_left = bolt_left_ref.part.move(Location((
    -GEAR_HEAD_LENGTH / 2,
    GEAR_HEAD_DIA / 2 + BRACKET_STEEL + 2,  # outside of bracket
    BLADE_CENTER_Z + HANDLE_HOLE_HEIGHT
)))

bolt_right = mirror(bolt_left, about=Plane.XZ)

# =============================================================================
# DISPLAY ASSEMBLY
# =============================================================================

show_object(base, name="Base Plate (1/4\" steel)", options={"color": (70, 70, 80)})
show_object(left_bracket, name="L-Bracket Left", options={"color": (90, 90, 100)})
show_object(right_bracket, name="L-Bracket Right", options={"color": (90, 90, 100)})
show_object(shaft_collar, name="Shaft Collar Brace", options={"color": (85, 85, 95)})

# Reference geometry (semi-transparent)
show_object(gear_head, name="Grinder Gear Head (ref)", options={"color": (40, 120, 40), "alpha": 0.4})
show_object(motor_body, name="Grinder Motor Body (ref)", options={"color": (50, 50, 60), "alpha": 0.3})
show_object(blade, name="Blade (ref)", options={"color": (180, 50, 50), "alpha": 0.4})
show_object(bolt_left, name="M10 Bolt Left", options={"color": (30, 30, 35)})
show_object(bolt_right, name="M10 Bolt Right", options={"color": (30, 30, 35)})

# =============================================================================
# OUTPUT SUMMARY
# =============================================================================

blade_bottom = BLADE_CENTER_Z - BLADE_DIA/2
blade_below_base = -blade_bottom if blade_bottom < 0 else 0

print(f"""
================================================================================
GRINDER MOUNT ASSEMBLY — Precision Cutting Sled
================================================================================

GRINDER PARAMETERS (from your measurements):

  Gear Head:
    - Diameter: {GEAR_HEAD_DIA} mm
    - Handle hole spacing: {HANDLE_HOLE_SPACING} mm (center-to-center)
    - Handle hole height above spindle: {HANDLE_HOLE_HEIGHT} mm
    - Handle thread: M{HANDLE_THREAD:.0f}

  Motor Body:
    - Barrel diameter: {MOTOR_BODY_DIA} mm

  Blade:
    - Diameter: {BLADE_DIA} mm (4.5")
    - Blade centerline: {BLADE_CENTER_Z:.1f} mm above base bottom

--------------------------------------------------------------------------------
FABRICATED COMPONENTS:
--------------------------------------------------------------------------------

  BASE PLATE (1/4" steel):
    - Size: {BASE_LENGTH:.0f} x {BASE_WIDTH:.0f} x {BASE_THICKNESS:.2f} mm
    - Size: {BASE_LENGTH/25.4:.2f}" x {BASE_WIDTH/25.4:.2f}" x 0.250"
    - Kerf slot: {KERF_SLOT_WIDTH:.0f} x {KERF_SLOT_LENGTH:.0f} mm (centered)
    - Corner holes: 4x Ø8.5mm, {12.0}mm from edges

  L-BRACKETS x2 (1/4" steel):
    - Vertical leg: {BRACKET_VERTICAL:.1f} mm ({BRACKET_VERTICAL/25.4:.2f}")
    - Horizontal leg: {BRACKET_HORIZONTAL:.1f} mm ({BRACKET_HORIZONTAL/25.4:.2f}")
    - Width: {BRACKET_WIDTH:.0f} mm
    - Top hole: Ø{HANDLE_THREAD + 1:.0f}mm (M{HANDLE_THREAD:.0f} clearance)
    - Attachment: Spot weld horizontal leg to base plate

  SHAFT COLLAR BRACE:
    - ID: {MOTOR_BODY_DIA + 1:.0f} mm (fits Ø{MOTOR_BODY_DIA:.0f}mm body + clearance)
    - OD: {MOTOR_BODY_DIA + 14:.0f} mm
    - Split clamp with M6 bolt
    - Support legs weld to base plate

--------------------------------------------------------------------------------
BLADE GEOMETRY:
--------------------------------------------------------------------------------

  Blade centerline Z: {BLADE_CENTER_Z:.1f} mm (above base bottom)
  Blade bottom edge:  {blade_bottom:.1f} mm {"(BELOW base)" if blade_bottom < 0 else "(above base)"}
  Blade exposure:     {blade_below_base:.1f} mm below base plate

  Target was {BLADE_EXPOSURE:.1f} mm (bottom 1/3 of {BLADE_DIA:.0f}mm blade)
  {"✓ ACHIEVED" if abs(blade_below_base - BLADE_EXPOSURE) < 1 else "✗ ADJUST PARAMETERS"}

================================================================================
CRITICAL: MEASURE YOUR GRINDER BEFORE FABRICATION!
================================================================================

  1. HANDLE_HOLE_SPACING = {HANDLE_HOLE_SPACING} mm
     → Put calipers across gear head, measure center-to-center of M10 holes

  2. HANDLE_HOLE_HEIGHT = {HANDLE_HOLE_HEIGHT} mm
     → Measure from spindle centerline UP to handle hole center

  3. GEAR_HEAD_DIA = {GEAR_HEAD_DIA} mm
     → Measure widest diameter of gear housing

  4. MOTOR_BODY_DIA = {MOTOR_BODY_DIA} mm
     → Measure barrel diameter where you grip it

Update parameters, re-run script (Shift+Enter), verify fit in viewer.
================================================================================
""")

# =============================================================================
# EXPORT (uncomment to generate files)
# =============================================================================

# base.export_step("grinder_mount_base.step")
# left_bracket.export_step("grinder_mount_bracket_left.step")
# shaft_collar.export_step("grinder_mount_collar.step")
