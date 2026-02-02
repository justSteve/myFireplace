# 3D Modeling Infrastructure — Decision Brief

**Project context**: Design and document a precision router sled built on SBR20-1000mm linear rails for ceramic tile cutting, plus ongoing jig/fixture design. Requires machinist-grade drafting, interactive 3D visualization, and a sustainable workflow where AI generates geometry from narrative and the human refines interactively.

---

## The Winning Stack

**Build123d** (Python modeling library) + **OCP CAD Viewer** (VS Code extension) + **WSL backend**

Code on the left, interactive 3D model on the right, inside the IDE. No context switching. No separate application windows. The model IS a Python script — AI generates it, human runs it with Shift+Enter, geometry appears in the viewer panel. Orbit, zoom, click faces. Discuss. Revise. Re-run.

---

## Requirements Scorecard

| Requirement | Build123d + OCP | CadQuery + Jupyter | FreeCAD + Python | OpenSCAD | SketchUp Pro |
|---|---|---|---|---|---|
| Agent generates from narrative | ★★★★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★ |
| Interactive 3D in IDE | ★★★★★ | ★★★★ | ★★★ | ★★★ | ★★ |
| Precision BREP geometry | ★★★★★ | ★★★★★ | ★★★★★ | ★★ | ★★★ |
| 2D drawing export (DXF/SVG) | ★★★★ | ★★★★ | ★★★★★ | ★★★ | ★★★ |
| Fillets, chamfers, lofts | ★★★★★ | ★★★★★ | ★★★★★ | ★ | ★★★ |
| Windows + WSL | ★★★★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★ |
| VSCode integration | ★★★★★ | ★★★ | ★ | ★★ | ★ |
| Learning curve | ★★★★ | ★★★★ | ★★ | ★★★★★ | ★★★ |
| Community / ecosystem | ★★★★ | ★★★★ | ★★★★★ | ★★★★ | ★★★★★ |
| Dimensioned shop drawings | ★★★ | ★★★ | ★★★★★ | ★★ | ★★★★ |

---

## The Stack in Detail

### Build123d — The Modeling Engine

Python library built on the OpenCascade geometric kernel (same kernel behind FreeCAD, CATIA's open-source components). Creates real BREP (Boundary Representation) geometry — mathematically precise surfaces, not meshes.

**Why Build123d over CadQuery**: Build123d is a fork/rewrite with a cleaner, more Pythonic API. CadQuery uses fluent method chaining; Build123d uses context managers and operators that read more naturally. Same underlying kernel, better interface. Active development, growing community on shared Discord.

**Capabilities for this project**:
- Precise dimensioned geometry in inches or mm
- Fillets and chamfers on edges
- Sweep and loft operations (for tapered post profiles)
- Boolean operations (union, subtract, intersect)
- Assembly support (position multiple parts)
- Export: STEP, STL, DXF, SVG
- 2D projection and section views
- Full Python: loops, functions, variables — parametric by nature

**Example workflow output**:
```python
from build123d import *
from ocp_vscode import show

# Parameters
rail_length = 1000      # mm (VEVOR SBR20)
rail_spacing = 200      # mm between rails
carriage_plate_t = 12   # mm thick aluminum

with BuildPart() as carriage:
    Box(carriage_plate_t, rail_spacing + 80, 200)
    with Locations((0, -rail_spacing/2, 0), (0, rail_spacing/2, 0)):
        Cylinder(5, carriage_plate_t, mode=Mode.SUBTRACT)

show(carriage)
```

### OCP CAD Viewer — The Visual Space

VS Code extension that renders Build123d objects in an interactive 3D panel.

**Features**:
- Split view: Python editor on left, 3D model on right
- Full orbit/zoom/pan with mouse
- Click faces, edges, vertices to inspect
- Transparency control per object
- Measurement tools
- Clipping planes (section views)
- Object tree for showing/hiding components
- Grid and axis display
- Orthographic and perspective projection
- Jupyter cell mode (`# %%` separators) for incremental execution

**Version**: 3.0.1 (November 2025), actively maintained by Bernhard Walter.

### WSL Backend

Python/Build123d runs in Linux (WSL). VS Code on Windows connects via WSL Remote extension. OCP CAD Viewer runs in VS Code on Windows but communicates with Python in WSL.

---

## What Was Considered and Why It Lost

### CadQuery
Same kernel. Solid choice. Fluent API less readable for complex models. Ecosystem shifting toward Build123d. OCP CAD Viewer supports both. If Build123d hits a wall, CadQuery is a lateral move — same kernel, same viewer, different syntax.

### OpenSCAD
Beloved by makers. CSG-only — no fillets, chamfers, sweeps, lofts. For precision tooling where edge treatment matters, this is a dealbreaker.

### FreeCAD
Most capable free CAD application. Full GUI, Python scripting, dimensioned drawings (TechDraw). Problem: collaboration difficulty. Model lives in .FCStd file, GUI state is complex, AI can't see what human is looking at. **Remains valuable downstream**: Build123d → STEP → FreeCAD TechDraw for formal shop drawings.

### SketchUp Pro
Existing subscription. Web version lacks scripting. Desktop has Ruby scripting but no VS Code integration. Less precise geometry engine.

### Blender
Mesh modeler and rendering engine. Not precision CAD. Excellent for photorealistic visualization, terrible for dimensioned drawings.

### SolveSpace
Lightweight constraint-based CAD. No scripting API — AI can't generate models.

### JSCAD
Browser-based. Less geometric capability. Could be useful later for embedding interactive models in web UIs.

---

## The 2D Drawing Question

Build123d exports geometrically accurate 2D projections and sections (DXF/SVG). Does NOT produce dimensioned drawings with leader lines, tolerances, annotations.

**Three paths to dimensioned drawings**:

1. **DXF → Manual annotation**: Export 2D views, open in LibreCAD/DraftSight, add dimensions. Quickest setup.
2. **STEP → FreeCAD TechDraw**: Import 3D model, generate dimensioned orthographic views with title block. Most traditional result.
3. **Custom Python dimensioning**: Programmatic SVG generation. Most automated, most upfront work.

Start with option 1. Option 2 is the upgrade path. Option 3 is long-term infrastructure.

---

## Installation Roadmap

### Phase 1: Core Environment (30 minutes)

See `cad/README.md` for step-by-step instructions.

```bash
mkdir -p ~/cad/projects && cd ~/cad
python3 -m venv .venv
source .venv/bin/activate
pip install build123d ocp-vscode
```

VS Code: Install WSL + OCP CAD Viewer extensions, connect to WSL, select .venv interpreter.

### Phase 2: Verification

Run `cad/verify_install.py` — creates a test object, confirms viewer renders.

### Phase 3: First Real Model

Generate SBR20 rail assembly from VEVOR specs.

---

## Cost

**$0 in software.** Everything open source:
- Build123d: MIT license
- OCP CAD Viewer: MIT license
- VS Code: Free
- WSL: Free
- FreeCAD (if needed later): LGPL

SketchUp Pro subscription remains useful for architectural visualization.
