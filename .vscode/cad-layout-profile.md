# CAD Work Layout Profile

Preferred VS Code layout for Build123d + OCP CAD Viewer work.

## Dual-Monitor Setup

**Left monitor**: VS Code (full screen)
- Claude Code chat panel — main working area (~70% width)
- Explorer/file tree — right sidebar
- Terminal — hidden or bottom panel when needed

**Right monitor**: OCP CAD Viewer (full screen, dedicated)
- Pop out viewer to separate window, maximize on right monitor
- Allows full 3D inspection while chatting/coding on left

## Font Sizes

Update these in `settings.json` to match your preferences:

- **Editor font size**: 14 (default)
- **Terminal font size**: 13 (default)

## To Restore This Layout

1. Open workspace: `/root/projects/myFireplace`
2. Ensure Claude Code panel is primary view (left monitor)
3. Open OCP CAD Viewer: `Ctrl+Shift+P` → "OCP CAD Viewer: Open Viewer"
4. **Pop out viewer**: Right-click viewer tab → "Move into New Window"
5. Drag new window to right monitor, maximize
6. Explorer sidebar on right of left monitor

## VS Code Keybindings (useful for CAD work)

- `Shift+Enter` — Run current cell/selection in Python
- `Ctrl+Shift+P` → "OCP CAD Viewer: Open Viewer" — Launch 3D viewer
- `` Ctrl+` `` — Toggle terminal
- `F5` — Run entire Python file

## tmux Session

CAD Python environment runs in tmux session `cad-setup`:
- Attach: `tmux attach -t cad-setup`
- Working dir: `/root/cad` or `/root/projects/myFireplace/cad`
- venv: `/root/cad/.venv` (already activated in session)
