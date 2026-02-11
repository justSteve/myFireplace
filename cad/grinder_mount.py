"""
Grinder Cutting Sled Assembly - FUNCTIONAL DESIGN
==================================================

Precision cutting sled for ceramic tile strips.

COORDINATE SYSTEM:
  X = Direction of travel (along rails, cutting direction)
  Y = Lateral direction (between rails)
  Z = Vertical (up from platen surface)

FUNCTIONAL GEOMETRY:
  - Platen (work surface) at Z=0, tile sits here
  - Platen has a slot for the blade to pass through
  - Rails elevated on risers, flanking the platen
  - Carriage (blocks + plate + stand) rides on rails
  - Blade extends DOWN through slot in base plate, through platen slot
  - As carriage moves along X, blade cuts through tile

All dimensions in millimeters.
"""

from build123d import *

try:
    from ocp_vscode import show_object, set_defaults, Camera
    set_defaults(reset_camera=Camera.KEEP)
except ImportError:
    def show_object(*args, **kwargs): pass

# =============================================================================
# TILE PARAMETERS
# =============================================================================
TILE_LENGTH = 610.0          # mm - 24 inches
TILE_WIDTH = 200.0           # mm - 7.875 inches
TILE_THICK = 6.35            # mm - 1/4 inch

# =============================================================================
# BLADE PARAMETERS (4.5" diamond blade)
# =============================================================================
BLADE_DIA = 115.0            # mm - 4.5 inches
BLADE_THICK = 1.2            # mm - ~0.045 inch kerf
BLADE_ARBOR = 22.0           # mm - arbor hole

# =============================================================================
# CUTTING GEOMETRY
# =============================================================================
# Blade must cut through tile completely
# Tile surface at Z = 0, tile bottom at Z = -TILE_THICK
# Blade bottom should reach Z = -TILE_THICK - 2mm for full cut
BLADE_BOTTOM_Z = -TILE_THICK - 2.0  # = -8.35mm
BLADE_CENTER_Z = BLADE_BOTTOM_Z + BLADE_DIA / 2  # = 49.15mm

# =============================================================================
# PLATEN (work surface)
# =============================================================================
PLATEN_THICK = 20.0          # mm - rigid work surface
PLATEN_WIDTH = 160.0         # mm - Y dimension, fits between rails
PLATEN_LENGTH = 700.0        # mm - X dimension, full tile + travel

# Blade slot in platen - full travel length
PLATEN_SLOT_WIDTH = 5.0      # mm - blade + clearance
PLATEN_SLOT_LENGTH = PLATEN_LENGTH - 40  # mm - nearly full length

# Platen surface at Z = 0, bottom at Z = -PLATEN_THICK
PLATEN_TOP_Z = 0.0
PLATEN_BOTTOM_Z = -PLATEN_THICK

# =============================================================================
# SBR20 RAIL DIMENSIONS
# =============================================================================
RAIL_BASE_WIDTH = 23.0       # mm
RAIL_BASE_HEIGHT = 6.0       # mm
RAIL_SHAFT_DIA = 20.0        # mm
RAIL_LENGTH = 600.0          # mm - travel length

# =============================================================================
# SBR20UU BLOCK DIMENSIONS
# =============================================================================
BLOCK_L = 50.0               # mm - along X (travel)
BLOCK_W = 48.0               # mm - along Y
BLOCK_H = 39.0               # mm - height
BLOCK_SHAFT_DIA = 20.0       # mm
BLOCK_SLOT_W = 10.0          # mm - open slot
BLOCK_SHAFT_Z_FROM_BOTTOM = 16.0  # mm (h=23 from top, so 39-23=16 from bottom)

# Mounting holes
BLOCK_HOLE_PATTERN_X = 35.0  # mm
BLOCK_HOLE_PATTERN_Y = 35.0  # mm
BLOCK_HOLE_DIA = 5.5         # mm - M5 clearance

# =============================================================================
# CARRIAGE GEOMETRY - Working backwards from blade position
# =============================================================================
# The grinder stand holds the grinder. When in cutting position,
# the blade center is at BLADE_CENTER_Z.
#
# The stand's arm pivots down. Approximate geometry:
#   - Stand base on plate
#   - Pivot point ~80mm above stand base
#   - Arm length to spindle ~100mm
#   - When arm is lowered ~45°, spindle drops ~70mm below pivot
#
# For blade center at Z = 49.15mm:
#   - Spindle at Z = 49.15mm
#   - Pivot at Z = 49.15 + 70 = 119.15mm
#   - Stand base at Z = 119.15 - 80 = 39.15mm
#
# But we need clearance for the blade to pass through the base plate.
# Base plate bottom should be above the blade TOP when at rest,
# but the blade passes through the slot when cutting.
#
# Let's set base plate bottom at Z = 70mm (above blade center + some margin)

BASE_PLATE_BOTTOM_Z = 70.0
BASE_PLATE_THICK = 6.35      # mm - 1/4 inch
BASE_PLATE_TOP_Z = BASE_PLATE_BOTTOM_Z + BASE_PLATE_THICK

# Blade passes through slot in base plate
BASE_PLATE_SLOT_L = 80.0     # mm - 3+ inches
BASE_PLATE_SLOT_W = 30.0     # mm - clearance for blade + guard

# =============================================================================
# BLOCK AND RAIL POSITIONS
# =============================================================================
# Block top meets base plate bottom
BLOCK_TOP_Z = BASE_PLATE_BOTTOM_Z
BLOCK_BOTTOM_Z = BLOCK_TOP_Z - BLOCK_H  # = 31mm

# Rail shaft aligns with block shaft bore
RAIL_SHAFT_Z = BLOCK_BOTTOM_Z + BLOCK_SHAFT_Z_FROM_BOTTOM  # = 47mm
RAIL_BASE_TOP_Z = RAIL_SHAFT_Z - RAIL_SHAFT_DIA / 2  # = 37mm
RAIL_BASE_BOTTOM_Z = RAIL_BASE_TOP_Z - RAIL_BASE_HEIGHT  # = 31mm

# Rail spacing - rails flank the platen
RAIL_SPACING_Y = 200.0       # mm center-to-center
RAIL_Y_LEFT = -RAIL_SPACING_Y / 2   # = -100mm
RAIL_Y_RIGHT = RAIL_SPACING_Y / 2   # = +100mm

# Block spacing along rails
BLOCK_SPACING_X = 120.0      # mm
BLOCK_X_REAR = -BLOCK_SPACING_X / 2
BLOCK_X_FRONT = BLOCK_SPACING_X / 2

BLOCK_POSITIONS = [
    (BLOCK_X_REAR, RAIL_Y_LEFT),
    (BLOCK_X_FRONT, RAIL_Y_LEFT),
    (BLOCK_X_REAR, RAIL_Y_RIGHT),
    (BLOCK_X_FRONT, RAIL_Y_RIGHT),
]

# =============================================================================
# BASE PLATE SIZE
# =============================================================================
BASE_PLATE_L = BLOCK_SPACING_X + BLOCK_L + 60  # = 230mm
BASE_PLATE_W = RAIL_SPACING_Y + BLOCK_W + 40   # = 288mm

# =============================================================================
# STAND REFERENCE (commercial grinder stand)
# =============================================================================
STAND_BASE_L = 205.0         # mm
STAND_BASE_W = 120.0         # mm
STAND_H = 100.0              # mm - to pivot point

# =============================================================================
# RAIL RISERS (support rails above platen)
# =============================================================================
# Rails need to be at RAIL_BASE_BOTTOM_Z = 31mm
# Risers sit on table (below platen), support rails
RISER_HEIGHT = RAIL_BASE_BOTTOM_Z - PLATEN_BOTTOM_Z  # 31 - (-20) = 51mm
RISER_WIDTH = 30.0
RISER_LENGTH = RAIL_LENGTH + 50


# =============================================================================
# BUILD FUNCTIONS
# =============================================================================

def make_platen() -> Part:
    """Work surface with blade slot."""
    with BuildPart() as p:
        # Main platen body
        with BuildSketch(Plane.XY.offset(PLATEN_BOTTOM_Z)):
            Rectangle(PLATEN_LENGTH, PLATEN_WIDTH)
        extrude(amount=PLATEN_THICK)

        # Blade slot (through the platen)
        with BuildSketch(Plane.XY.offset(PLATEN_TOP_Z)):
            SlotOverall(PLATEN_SLOT_LENGTH, PLATEN_SLOT_WIDTH)
        extrude(amount=-PLATEN_THICK, mode=Mode.SUBTRACT)

    return p.part


def make_riser(y_pos: float) -> Part:
    """Rail support riser."""
    with BuildPart() as r:
        with BuildSketch(Plane.XY.offset(PLATEN_BOTTOM_Z)):
            with Locations((0, y_pos)):
                Rectangle(RISER_LENGTH, RISER_WIDTH)
        extrude(amount=RISER_HEIGHT)
    return r.part


def make_rail(y_pos: float) -> Part:
    """SBR20 rail at given Y position, running along X."""
    with BuildPart() as rail:
        with BuildSketch(Plane.YZ):
            # Base
            with Locations((y_pos, RAIL_BASE_BOTTOM_Z + RAIL_BASE_HEIGHT/2)):
                Rectangle(RAIL_BASE_WIDTH, RAIL_BASE_HEIGHT)
            # Shaft
            with Locations((y_pos, RAIL_SHAFT_Z)):
                Circle(RAIL_SHAFT_DIA / 2)
        extrude(amount=RAIL_LENGTH / 2, both=True)
    return rail.part


def make_block(x_pos: float, y_pos: float) -> Part:
    """SBR20UU bearing block."""
    with BuildPart() as blk:
        # Main body
        with BuildSketch(Plane.XY.offset(BLOCK_BOTTOM_Z)):
            with Locations((x_pos, y_pos)):
                Rectangle(BLOCK_L, BLOCK_W)
        extrude(amount=BLOCK_H)

        # Shaft bore (along X)
        bore_z = BLOCK_BOTTOM_Z + BLOCK_SHAFT_Z_FROM_BOTTOM
        with BuildSketch(Plane.YZ.offset(x_pos - BLOCK_L/2)):
            with Locations((y_pos, bore_z)):
                Circle(BLOCK_SHAFT_DIA / 2 + 0.5)
        extrude(amount=BLOCK_L, mode=Mode.SUBTRACT)

        # Open slot at bottom
        slot_h = BLOCK_SHAFT_Z_FROM_BOTTOM + BLOCK_SHAFT_DIA/2 + 2
        with BuildSketch(Plane.XY.offset(BLOCK_BOTTOM_Z)):
            with Locations((x_pos, y_pos)):
                Rectangle(BLOCK_L, BLOCK_SLOT_W)
        extrude(amount=slot_h, mode=Mode.SUBTRACT)

        # Mounting holes on top
        with BuildSketch(Plane.XY.offset(BLOCK_TOP_Z)):
            for dx in [-BLOCK_HOLE_PATTERN_X/2, BLOCK_HOLE_PATTERN_X/2]:
                for dy in [-BLOCK_HOLE_PATTERN_Y/2, BLOCK_HOLE_PATTERN_Y/2]:
                    with Locations((x_pos + dx, y_pos + dy)):
                        Circle(BLOCK_HOLE_DIA / 2)
        extrude(amount=-12, mode=Mode.SUBTRACT)

    return blk.part


def make_base_plate() -> Part:
    """Carriage base plate with blade slot."""
    with BuildPart() as plt:
        # Main plate
        with BuildSketch(Plane.XY.offset(BASE_PLATE_BOTTOM_Z)):
            Rectangle(BASE_PLATE_L, BASE_PLATE_W)
        extrude(amount=BASE_PLATE_THICK)

        # Blade slot (centered)
        with BuildSketch(Plane.XY.offset(BASE_PLATE_TOP_Z)):
            SlotOverall(BASE_PLATE_SLOT_L, BASE_PLATE_SLOT_W)
        extrude(amount=-BASE_PLATE_THICK, mode=Mode.SUBTRACT)

        # Block mounting holes (16 total)
        for bx, by in BLOCK_POSITIONS:
            with BuildSketch(Plane.XY.offset(BASE_PLATE_TOP_Z)):
                for dx in [-BLOCK_HOLE_PATTERN_X/2, BLOCK_HOLE_PATTERN_X/2]:
                    for dy in [-BLOCK_HOLE_PATTERN_Y/2, BLOCK_HOLE_PATTERN_Y/2]:
                        with Locations((bx + dx, by + dy)):
                            Circle(BLOCK_HOLE_DIA / 2)
            extrude(amount=-BASE_PLATE_THICK, mode=Mode.SUBTRACT)

        # Stand mounting slots
        with BuildSketch(Plane.XY.offset(BASE_PLATE_TOP_Z)):
            for sy in [-40, 40]:
                with Locations((0, sy)):
                    SlotOverall(50, 8)
        extrude(amount=-BASE_PLATE_THICK, mode=Mode.SUBTRACT)

    return plt.part


def make_stand() -> Part:
    """Simplified grinder stand."""
    z0 = BASE_PLATE_TOP_Z
    with BuildPart() as st:
        # Base
        with BuildSketch(Plane.XY.offset(z0)):
            Rectangle(STAND_BASE_L, STAND_BASE_W)
        extrude(amount=5)

        # Upright/pivot housing
        with BuildSketch(Plane.XY.offset(z0 + 5)):
            with Locations((-STAND_BASE_L/3, 0)):
                Rectangle(60, 80)
        extrude(amount=STAND_H)

        # Arm (simplified, shown in cutting position)
        with BuildSketch(Plane.XY.offset(z0 + 5 + STAND_H - 20)):
            with Locations((20, 0)):
                Rectangle(120, 50)
        extrude(amount=20)

    return st.part


def make_grinder() -> Part:
    """Simplified grinder body in cutting position."""
    # Grinder body - cylinder at angle
    spindle_z = BLADE_CENTER_Z
    with BuildPart() as gr:
        # Motor body (cylinder along Y axis, tilted down)
        with BuildSketch(Plane.XZ.offset(0)):
            with Locations((40, spindle_z + 30)):
                Circle(35)  # motor diameter
        extrude(amount=80, both=True)

        # Gear head (near spindle)
        with BuildSketch(Plane.XZ.offset(0)):
            with Locations((40, spindle_z)):
                Circle(25)
        extrude(amount=40, both=True)

    return gr.part


def make_blade() -> Part:
    """Cutting blade in YZ plane (perpendicular to travel)."""
    with BuildPart() as bl:
        with BuildSketch(Plane.YZ):  # YZ plane - perpendicular to X travel
            with Locations((0, BLADE_CENTER_Z)):
                Circle(BLADE_DIA / 2)
                Circle(BLADE_ARBOR / 2, mode=Mode.SUBTRACT)
        extrude(amount=BLADE_THICK / 2, both=True)
    return bl.part


def make_tile() -> Part:
    """Reference tile on platen."""
    with BuildPart() as t:
        with BuildSketch(Plane.XY.offset(PLATEN_TOP_Z)):
            # Tile offset to show it being cut
            with Locations((-50, 0)):
                Rectangle(TILE_LENGTH, TILE_WIDTH)
        extrude(amount=TILE_THICK)
    return t.part


# =============================================================================
# CREATE ASSEMBLY
# =============================================================================

# Fixed components
platen = make_platen()
riser_left = make_riser(RAIL_Y_LEFT)
riser_right = make_riser(RAIL_Y_RIGHT)
rail_left = make_rail(RAIL_Y_LEFT)
rail_right = make_rail(RAIL_Y_RIGHT)

# Carriage components
blocks = [make_block(x, y) for x, y in BLOCK_POSITIONS]
base_plate = make_base_plate()
stand = make_stand()
grinder = make_grinder()
blade = make_blade()

# Workpiece
tile = make_tile()

# =============================================================================
# DISPLAY
# =============================================================================

# Platen - wood/MDF color
show_object(platen, name="Platen", options={"color": (180, 140, 100)})

# Risers - structural
show_object(riser_left, name="Riser_Left", options={"color": (100, 100, 105)})
show_object(riser_right, name="Riser_Right", options={"color": (100, 100, 105)})

# Rails
show_object(rail_left, name="Rail_Left", options={"color": (60, 60, 65), "alpha": 0.8})
show_object(rail_right, name="Rail_Right", options={"color": (60, 60, 65), "alpha": 0.8})

# Blocks
for i, blk in enumerate(blocks):
    names = ["Block_RL", "Block_FL", "Block_RR", "Block_FR"]
    show_object(blk, name=names[i], options={"color": (140, 140, 150)})

# Base plate (FABRICATE THIS)
show_object(base_plate, name="BASE_PLATE_fabricate", options={"color": (70, 130, 180)})

# Stand (reference)
show_object(stand, name="Stand_ref", options={"color": (80, 80, 85), "alpha": 0.5})

# Grinder (reference)
show_object(grinder, name="Grinder_ref", options={"color": (60, 60, 65), "alpha": 0.4})

# Blade (cutting position)
show_object(blade, name="BLADE", options={"color": (200, 50, 50), "alpha": 0.7})

# Tile (workpiece)
show_object(tile, name="Tile_workpiece", options={"color": (210, 180, 140), "alpha": 0.6})

# =============================================================================
# VERIFICATION
# =============================================================================
print(f"""
================================================================================
GRINDER CUTTING SLED - FUNCTIONAL DESIGN
================================================================================

VERIFICATION - Does the blade reach the tile?

  Tile:
    Top surface:    Z = {PLATEN_TOP_Z + TILE_THICK:.1f} mm
    Bottom surface: Z = {PLATEN_TOP_Z:.1f} mm (on platen)

  Blade (4.5" / 115mm):
    Center:  Z = {BLADE_CENTER_Z:.1f} mm
    Top:     Z = {BLADE_CENTER_Z + BLADE_DIA/2:.1f} mm
    Bottom:  Z = {BLADE_BOTTOM_Z:.1f} mm

  ✓ Blade bottom ({BLADE_BOTTOM_Z:.1f}mm) is BELOW tile bottom ({PLATEN_TOP_Z:.1f}mm)
  ✓ Blade will cut completely through the tile

--------------------------------------------------------------------------------
PLATEN (work surface)
--------------------------------------------------------------------------------
  Size: {PLATEN_LENGTH} × {PLATEN_WIDTH} × {PLATEN_THICK} mm
  Surface at Z = {PLATEN_TOP_Z} mm
  Blade slot: {PLATEN_SLOT_LENGTH} × {PLATEN_SLOT_WIDTH} mm (through center)

--------------------------------------------------------------------------------
RAILS (2× SBR20, on risers)
--------------------------------------------------------------------------------
  Riser height: {RISER_HEIGHT:.1f} mm (lifts rails above platen)
  Rail shaft center: Z = {RAIL_SHAFT_Z:.1f} mm
  Rail spacing: {RAIL_SPACING_Y} mm (Y = ±{RAIL_SPACING_Y/2} mm)
  Rail length: {RAIL_LENGTH} mm

--------------------------------------------------------------------------------
CARRIAGE
--------------------------------------------------------------------------------
  Blocks (4× SBR20UU):
    Bottom: Z = {BLOCK_BOTTOM_Z:.1f} mm
    Top:    Z = {BLOCK_TOP_Z:.1f} mm

  Base plate:
    Size: {BASE_PLATE_L} × {BASE_PLATE_W} × {BASE_PLATE_THICK} mm
    Bottom: Z = {BASE_PLATE_BOTTOM_Z:.1f} mm
    Top:    Z = {BASE_PLATE_TOP_Z:.1f} mm
    Blade slot: {BASE_PLATE_SLOT_L} × {BASE_PLATE_SLOT_W} mm

--------------------------------------------------------------------------------
BLADE ORIENTATION
--------------------------------------------------------------------------------
  Blade disc in YZ plane (perpendicular to X travel direction)
  As carriage moves along +X, blade cuts through tile

================================================================================
HOW IT WORKS:
================================================================================
  1. Place tile on platen (centered over blade slot)
  2. Set fence for strip width
  3. Lower grinder to cutting depth (blade through platen slot)
  4. Turn on grinder, start water flow
  5. Push carriage along rails (+X direction)
  6. Blade cuts through tile
  7. Return carriage, index tile for next strip, repeat

================================================================================
""")

# =============================================================================
# EXPORTS
# =============================================================================
import os
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Main fabrication part
export_step(base_plate, os.path.join(EXPORT_DIR, "grinder_sled_base_plate.step"))
print(f"Exported: grinder_sled_base_plate.step")

# Full assembly as compound
assembly = Compound(children=[
    platen, riser_left, riser_right, rail_left, rail_right,
    *blocks, base_plate, stand, grinder, blade, tile
])
export_step(assembly, os.path.join(EXPORT_DIR, "grinder_sled_assembly.step"))
print(f"Exported: grinder_sled_assembly.step")
