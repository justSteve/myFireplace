# Polycam 3D Scanning Integration

## Overview

Polycam (Basic subscription) provides a real-world-to-digital pipeline for the fireplace project. Scan actual surfaces with a phone, export as mesh, import into Build123d as reference geometry for precision part design.

## Primary Use Case

Scan the fireplace corner geometry — the rough stone edges, angles under the vaulted ceiling, the relationship between hearth extension and upper chimney — to get actual 3D reference surfaces. Design the corner post geometry around the real scanned shape rather than idealized measurements.

## Workflow

1. **Scan** — Capture corner with Polycam on phone
2. **Export** — STL (primary) and OBJ (secondary, for texture)
3. **Import** — `import_stl()` in Build123d drops scan into viewer
4. **Overlay** — Modeled post geometry sits alongside scanned surface
5. **Verify fit** — Check clearances, angles, transitions before cutting tile

## Export Formats

### Recommended

- **STL** — Build123d native import via `import_stl()`. No texture, but geometrically clean. Use for dimensional reference.
- **OBJ** — Carries texture coordinates. Stone surface renders recognizably. Use for visual context.

### Available on Basic Tier

OBJ, FBX, GLTF, DAE, STL, USDZ, images, video, blueprints (12 formats total).

### Not Available on Basic

Point cloud formats (LAS, PLY, PTS, XYZ, DXF) require Business or Enterprise tier.

## Scan Quality Notes

- **LiDAR** (iPhone Pro / iPad Pro): Best dimensional accuracy, typically ±2-3mm at room scale. Fast capture.
- **Photogrammetry** (any phone): Higher visual detail, less dimensional accuracy. Slower (cloud processing).
- **Mesh density**: Medium resolution is sufficient for reference geometry. Hundreds of thousands of triangles is plenty; millions would slow the OCP Viewer.

## Build123d Import

```python
from build123d import *
from ocp_vscode import show

# Import scanned mesh as reference
scanned_corner = import_stl("polycam_corner_scan.stl")

# Import or create precision post model
# ... (Build123d geometry here)

# Show both in viewer
show(scanned_corner, post_assembly)
```

The scanned mesh appears as a reference body in the same viewer alongside precision-modeled parts. It cannot be edited as BREP (it's a mesh), but it provides visual and dimensional reference.

## Existing Scan

A scan was made approximately one year ago. May need to be re-done with current Polycam version for better quality, but existing scan is usable for initial import testing.

## Device

TBD — confirm whether scanning device has LiDAR (iPhone Pro/iPad Pro) or is photogrammetry-only.

## Open Questions

1. Scanning device capabilities (LiDAR or photogrammetry only?)
2. Quality of existing year-old scan
3. Whether multiple corner locations need separate scans
4. Scale calibration — does existing scan have accurate dimensional scale?
