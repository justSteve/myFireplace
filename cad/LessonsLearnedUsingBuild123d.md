# Build123d Lessons Learned

Hard-won knowledge from developing CAD models with Build123d. Future agents: read this before writing Build123d code.

## 1. Build123d CENTERS geometry automatically

**Problem**: When you create a shape specifying coordinates from 0, Build123d centers the result around the origin.

```python
# You write this:
Polygon([
    (-WIDTH/2, 0),
    (WIDTH/2, 0),
    (WIDTH/2, HEIGHT),
    (-WIDTH/2, HEIGHT)
])
# Expecting Y from 0 to HEIGHT

# But Build123d produces Y from -HEIGHT/2 to +HEIGHT/2
```

**Fix**: After creating geometry, shift it by half the dimension:
```python
part = part.move(Location((0, HEIGHT/2, 0)))
```

## 2. Axis rotation with off-origin pivots is unreliable

**Problem**: `Axis((point), (direction))` creates an axis, but rotation behavior around off-origin points may not work as expected.

**Fix**: Use the translate-rotate-translate pattern:
```python
# To rotate around pivot point (pivot_x, 0, 0):
part = part.move(Location((-pivot_x, 0, 0)))  # Move pivot to origin
part = part.rotate(Axis.Y, angle)              # Rotate around origin
part = part.move(Location((pivot_x, 0, 0)))    # Move back
```

## 3. Build in Plane.XY, then rotate to final orientation

**Problem**: Using `Plane.YZ` or `Plane.XZ` directly leads to confusion about which sketch coordinate maps to which 3D axis.

**Fix**: Build everything in XY (the default/intuitive plane), then rotate to vertical:
```python
# Build flat in XY
with BuildSketch(Plane.XY):
    # X = width, Y = length in sketch
    ...
extrude(amount=THICKNESS)

# Then rotate to final orientation
part = part.rotate(Axis.X, 90)  # Y becomes Z
part = part.rotate(Axis.Z, 90)  # Reorient as needed
```

## 4. Debug with bounding boxes

**Problem**: Geometry ends up in unexpected locations, hard to diagnose.

**Fix**: Print bounding boxes at each transformation step:
```python
bb = part.bounding_box()
print(f"X: {bb.min.X:.1f} to {bb.max.X:.1f}")
print(f"Y: {bb.min.Y:.1f} to {bb.max.Y:.1f}")
print(f"Z: {bb.min.Z:.1f} to {bb.max.Z:.1f}")
```

## 5. Revolve around Axis.Z coordinate mapping

When revolving a sketch in Plane.XZ around Axis.Z:
- Sketch X coordinate becomes **radial distance** from Z axis
- Sketch Z coordinate becomes **3D Z coordinate**
- Revolve arc starts at +X and goes CCW (looking down -Z)

```python
with BuildSketch(Plane.XZ):
    with Locations((radius, z_height)):
        Rectangle(width, height)
revolve(axis=Axis.Z, revolution_arc=90)
# Creates arc from +X toward +Y
```

## 6. Centering revolved arcs

After revolve, the arc starts at angle 0 (+X direction). To center it on +X:
```python
part = part.rotate(Axis.Z, -arc_degrees/2)
```

## 7. Units

Build123d works in mm internally. Define a constant for inches:
```python
IN = 25.4
RAIL_SIZE = 0.5 * IN  # 0.5 inches = 12.7mm
```

## General Strategy

1. **Start simple** - Build basic shapes at origin in Plane.XY
2. **Transform step by step** - One rotation/translation at a time
3. **Print bounding boxes** - Verify position after each transform
4. **Use the viewer** - OCP CAD Viewer shows exactly what you've built
5. **Don't fight the centering** - Accept it and compensate with moves
