# SketchUp Ruby Scripts

These scripts were created during initial design exploration before the Build123d environment was set up. They remain useful for quick visualization in SketchUp Pro.

## Usage

1. Open SketchUp Pro (desktop version)
2. Open the Ruby Console: `Window > Ruby Console`
3. Paste the script contents
4. Press Enter to execute

## Scripts

### corner_post.rb

Calculates strip geometry for the 270° corner post and generates a 3D model.

- `CornerPost.calculate` — Prints a table of strip count options with resulting radii
- `CornerPost.build` — Builds the model with recommended configuration
- `CornerPost.build(9)` — Builds with a specific strip count

Includes reference walls at 50% opacity showing corner context.

### tile_cutting_jig.rb

Parametric model of the router-on-rails cutting jig.

- `TileCuttingJig.build` — Builds the full assembly
- All dimensions adjustable via constants at top of module
- Includes: frame, rails, carriage, router, angled bed, tile, fence

## Note

These scripts are for SketchUp's Ruby Console only. They use SketchUp-specific APIs (Sketchup module, Geom classes) and won't run in standard Ruby.

The primary modeling environment going forward is Build123d + OCP CAD Viewer in VS Code. See `cad/README.md`.
