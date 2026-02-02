# Build123d + OCP CAD Viewer — Setup Guide

## Prerequisites

- Windows with WSL installed
- VS Code with WSL extension
- Python 3.10+ in WSL

## Phase 1: Install Build123d (in WSL terminal)

```bash
# Create dedicated CAD environment
mkdir -p ~/cad/projects && cd ~/cad
python3 -m venv .venv
source .venv/bin/activate

# Install Build123d and the VS Code viewer bridge
pip install build123d ocp-vscode
```

## Phase 2: Configure VS Code

1. **Install extensions** (in VS Code on Windows):
   - "WSL" (Microsoft) — if not already installed
   - "OCP CAD Viewer" (Bernhard Walter) — search for `ocp-cad-viewer`
   - "Python" (Microsoft) — if not already installed

2. **Connect to WSL**:
   - `Ctrl+Shift+P` → "WSL: Connect to WSL"
   - Open the `~/cad` folder

3. **Select Python interpreter**:
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Choose the `.venv` interpreter (`~/cad/.venv/bin/python3`)

4. **Verify OCP CAD Viewer**:
   - Look for the OCP CAD Viewer icon in the sidebar
   - Click "Quickstart build123d" to confirm installation

## Phase 3: Run Verification

```bash
cd ~/cad
source .venv/bin/activate
python verify_install.py
```

This should render a test object in the OCP CAD Viewer panel.

Alternatively, open `verify_install.py` in VS Code and run it with `Shift+Enter` (if using Jupyter cell mode with `# %%` separators) or `F5`.

## Workflow

1. **AI generates .py script** from narrative description
2. **Human runs script** in VS Code (`Shift+Enter` or `F5`)
3. **`show()` call** sends geometry to OCP CAD Viewer panel
4. **Interactive inspection**: orbit, zoom, pan, click faces/edges
5. **Iterate**: AI modifies script based on feedback, human re-runs

## File Conventions

- Model scripts go in `~/cad/projects/` (or the repo's `cad/` directory)
- Use `# %%` cell separators for incremental execution
- Parameters at top of file for easy adjustment
- `show()` at end of each cell for progressive visualization
- Export with `export_step()`, `export_stl()`, `export_svg()`, `export_dxf()`

## Importing Polycam Scans

```python
from build123d import *
from ocp_vscode import show

# Import STL scan as reference mesh
scanned = import_stl("path/to/polycam_export.stl")
show(scanned)
```

## Troubleshooting

- **Viewer doesn't open**: Make sure OCP CAD Viewer extension is installed and VS Code is connected to WSL
- **Import errors**: Ensure the `.venv` is activated and `build123d` is installed (`pip list | grep build123d`)
- **Slow rendering**: Reduce mesh complexity for Polycam imports; Build123d BREP models are typically fast
