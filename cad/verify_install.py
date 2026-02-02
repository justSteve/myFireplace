# %% Build123d Installation Verification
# Run this file to confirm the modeling environment is working.
# In VS Code: Shift+Enter to execute this cell, or F5 for full file.

from build123d import *
from ocp_vscode import show

print("Build123d imported successfully")
print(f"Version info: build123d is ready")

# %% Create a simple test object
# This creates a small bracket-like part to verify all core operations work.

# Parameters (inches, converted to mm for Build123d default)
INCH = 25.4  # mm per inch

with BuildPart() as test_part:
    # Base plate
    Box(3 * INCH, 2 * INCH, 0.25 * INCH)
    
    # Add a vertical wall
    with BuildSketch(test_part.faces().sort_by(Axis.Z)[-1]):
        with Locations((0, 0.75 * INCH)):
            Rectangle(3 * INCH, 0.5 * INCH)
    extrude(amount=1.5 * INCH)
    
    # Add mounting holes in base
    with BuildSketch(test_part.faces().sort_by(Axis.Z)[0]):
        with Locations(
            (-1 * INCH, -0.5 * INCH),
            (1 * INCH, -0.5 * INCH),
        ):
            Circle(0.15 * INCH)
    extrude(amount=-0.25 * INCH, mode=Mode.SUBTRACT)
    
    # Fillet the base-to-wall junction
    wall_edges = test_part.edges().filter_by(Axis.X).sort_by(Axis.Z)
    if len(wall_edges) > 2:
        fillet(wall_edges[2:4], radius=0.125 * INCH)

print(f"Test part created: {test_part.part.bounding_box()}")
print("Sending to OCP CAD Viewer...")

show(test_part, name="Verification Part")

print("")
print("="*50)
print("SUCCESS — Build123d environment is working!")
print("="*50)
print("")
print("You should see a small L-bracket with mounting holes")
print("in the OCP CAD Viewer panel.")
print("")
print("Try: orbit (right-drag), zoom (scroll), click faces.")
