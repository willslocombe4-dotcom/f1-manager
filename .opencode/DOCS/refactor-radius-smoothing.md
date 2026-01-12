# Refactor: Procedural Track Radius Smoothing

## Goal
Reduce high-frequency noise in procedural track generation to prevent self-intersecting loops and "balloon" corners caused by sharp spikes in control point radii. The current "Angular Sort" algorithm produces "star-shaped" polygons that result in physically impossible track geometry when smoothed via Catmull-Rom splines.

## Scope
- **File**: `tools/track_generator.py`
- **Class**: `TrackGenerator`
- **Function**: `generate_procedural`

## Implementation Details

### 1. Data Structure Separation
Currently, the code generates radius `r` and immediately converts it to `(x, y)` coordinates.
**Change**: Store generated `radii` and `angles` in separate lists first to allow for intermediate processing.

### 2. New Phase: Radius Smoothing
Insert a smoothing loop between radius generation and Cartesian conversion.

**Logic**:
- Accept a `radius_smooth_passes` parameter (default: 2).
- For each pass:
  - Iterate through all radii.
  - Calculate average of neighbors: `new_r = (prev_r + curr_r + next_r) / 3`.
  - Handle wrapping (index -1 is the last element).
  - Update `radii` list.

### 3. Integration
Use the *smoothed* radii to generate the final `points` list for the spline generator.

### Pseudocode Reference
```python
# ... existing angle generation ...

# Generate initial radii
radii = []
for _ in range(num_points):
    r = random.uniform(MIN_RADIUS, MAX_RADIUS)
    # ... existing chaos logic ...
    radii.append(r)

# Phase 2: Radius Smoothing (NEW)
for _ in range(radius_smooth_passes):
    new_radii = []
    count = len(radii)
    for i in range(count):
        prev_r = radii[i-1]
        curr_r = radii[i]
        next_r = radii[(i+1) % count]
        new_radii.append((prev_r + curr_r + next_r) / 3)
    radii = new_radii

# Convert to Cartesian
points = []
for i, angle in enumerate(angles):
    r = radii[i]
    x = CENTER[0] + r * math.cos(angle)
    y = CENTER[1] + r * math.sin(angle)
    points.append((x, y))

# ... existing spline logic ...
```

## Next Steps
- [ ] Open `tools/track_generator.py`.
- [ ] Locate `generate_procedural` method.
- [ ] Refactor the generation loop to separate radius calculation from coordinate conversion.
- [ ] Implement the neighbor-averaging smoothing loop.
- [ ] Verify that `radius_smooth_passes` defaults to 2.
- [ ] Test generation to ensure loops/intersections are reduced.
