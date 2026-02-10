"""
Firebox Parameters - Single Source of Truth

All dimensions in INCHES (as measured/documented).
Use to_cm() when passing values to Fusion 360 API.

Every CAD script and design document references this file.
When dimensions change, update HERE and propagate.
"""

# --- Conversion ---

INCH_TO_CM = 2.54

def to_cm(inches: float) -> float:
    """Convert inches to centimeters (Fusion 360 API unit)."""
    return inches * INCH_TO_CM


# === EXISTING SHELL (as-built) ===

# Primary chamber (steel Heatilator cavity)
SHELL_WIDTH = 36.0          # inches
SHELL_DEPTH = 24.0          # inches
SHELL_HEIGHT = 24.0         # inches

# Convection channels (sides/back, TBD - requires demolition)
CHANNEL_DEPTH_EST = 10.0    # inches, estimated additional depth
TOTAL_DEPTH_EST = 34.0      # inches, firebox + channels

# Flue
FLUE_WIDTH = 12.0           # inches (1 sq ft tile flue)
FLUE_DEPTH = 12.0           # inches

# Facade offset
FACADE_OFFSET = 10.0        # inches, front face from original brick


# === FIREBRICK LINING ===

# Standard firebrick dimensions
FIREBRICK_LENGTH = 9.0      # inches
FIREBRICK_WIDTH = 4.5       # inches (used as wall thickness)
FIREBRICK_THICKNESS = 2.5   # inches (or 3.0 for thicker variant)

# Mortar joints
MORTAR_JOINT = 0.125        # inches (1/8")

# Ceramic fiber blanket (expansion gaps, NOT insulation)
FIBER_BLANKET_MIN = 1.0     # inches
FIBER_BLANKET_MAX = 2.0     # inches

# Wall thickness (firebrick laid flat)
WALL_THICKNESS = FIREBRICK_WIDTH   # 4.5 inches


# === INTERIOR DIMENSIONS (after lining) ===

INTERIOR_WIDTH = SHELL_WIDTH - (2 * WALL_THICKNESS)    # 27.0 inches
INTERIOR_DEPTH = SHELL_DEPTH - WALL_THICKNESS           # 19.5 inches
INTERIOR_HEIGHT = SHELL_HEIGHT - WALL_THICKNESS          # 19.5 inches (floor brick)


# === ASH REMOVAL SYSTEM ===

# Angled grate
GRATE_WIDTH_MIN = 24.0      # inches
GRATE_WIDTH_MAX = 26.0      # inches
GRATE_DEPTH = 8.0           # inches (front-to-back)
GRATE_ANGLE_DEG = 22.5      # degrees (midpoint of 20-25 range)
GRATE_RISE = 3.5            # inches (midpoint of 3-4" rise)
GRATE_BAR_SPACING = 0.875   # inches (midpoint of 3/4" - 1")

# Ash trough
TROUGH_WIDTH = GRATE_WIDTH_MIN  # 24 inches (conservative)
TROUGH_DEPTH = 8.0              # inches (same as grate)
TROUGH_HEIGHT = 4.5             # inches (midpoint of 4-5")


# === THERMAL / SAFETY ===

# PEX temperature limits
PEX_CONTINUOUS_MAX_F = 180.0    # degrees F
PEX_PEAK_MAX_F = 200.0         # degrees F

# Secondary combustion temperature range
SECONDARY_COMB_MIN_F = 1100.0  # degrees F
SECONDARY_COMB_MAX_F = 1400.0  # degrees F

# Coil circulation activation threshold
COIL_PUMP_THRESHOLD_F = 100.0  # degrees F


# === DERIVED VALUES (Fusion 360 API, centimeters) ===

SHELL_WIDTH_CM = to_cm(SHELL_WIDTH)         # 91.44
SHELL_DEPTH_CM = to_cm(SHELL_DEPTH)         # 60.96
SHELL_HEIGHT_CM = to_cm(SHELL_HEIGHT)       # 60.96

INTERIOR_WIDTH_CM = to_cm(INTERIOR_WIDTH)   # 68.58
INTERIOR_DEPTH_CM = to_cm(INTERIOR_DEPTH)   # 49.53
INTERIOR_HEIGHT_CM = to_cm(INTERIOR_HEIGHT) # 49.53

WALL_THICKNESS_CM = to_cm(WALL_THICKNESS)   # 11.43


if __name__ == "__main__":
    print("Firebox Parameters")
    print("=" * 40)
    print(f"\nShell (inches):  {SHELL_WIDTH} x {SHELL_DEPTH} x {SHELL_HEIGHT}")
    print(f"Shell (cm):      {SHELL_WIDTH_CM:.2f} x {SHELL_DEPTH_CM:.2f} x {SHELL_HEIGHT_CM:.2f}")
    print(f"\nInterior (inches): {INTERIOR_WIDTH} x {INTERIOR_DEPTH} x {INTERIOR_HEIGHT}")
    print(f"Interior (cm):     {INTERIOR_WIDTH_CM:.2f} x {INTERIOR_DEPTH_CM:.2f} x {INTERIOR_HEIGHT_CM:.2f}")
    print(f"\nWall thickness: {WALL_THICKNESS}\" / {WALL_THICKNESS_CM:.2f} cm")
    print(f"Mortar joint:   {MORTAR_JOINT}\"")
