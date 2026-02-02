# %% Polycam Scan Viewer
# Load and display the fireplace corner scan in OCP CAD Viewer

from build123d import *
from ocp_vscode import show
import os

# Path to the Polycam STL export
SCAN_PATH = os.path.join(os.path.dirname(__file__), "../polycam/2_1_2026.stl")

print(f"Loading scan from: {SCAN_PATH}")

# Import the mesh
scan_mesh = import_stl(SCAN_PATH)

print(f"Mesh loaded successfully")
print(f"Bounding box: {scan_mesh.bounding_box()}")

# Display in viewer
show(scan_mesh)

print("Scan displayed in OCP CAD Viewer")
print("Use right-drag to orbit, scroll to zoom")
