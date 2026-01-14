# Tool: Track Validation Tool

## Goal
Create a command-line tool (`tools/validate_tracks.py`) to automatically audit generated track JSON files for geometric validity and quality.

## Architecture & Scope
- **Type**: Standalone CLI Tool.
- **Input**: Scans `tools/tracks/*.json`.
- **Output**: Console report (PASS/FAIL) and exit code.

## Validation Logic

### A. Self-Intersection (The "Figure-8" Check)
- **Logic**: Iterate through every line segment. Check if it intersects with any other non-adjacent segment.
- **Failure Condition**: "Track intersects itself at indices [i] and [j]."

### B. Minimum Angle (The "Spike" Check)
- **Logic**: For every triplet of points, calculate the interior angle.
- **Threshold**: Angle must be > 45°.
- **Failure Condition**: "Sharp spike detected at index [i] (Angle: X deg)."

### C. Segment Length Consistency (The "Bunching" Check)
- **Logic**: Calculate the length of every segment.
- **Thresholds**:
  - `L_min > 0.2 * L_median`
  - `L_max < 3.0 * L_median`
- **Failure Condition**: "Segment [i] length (X) is inconsistent with median (Y)."

### D. Curvature Continuity (The "Kink" Check)
- **Logic**: Measure the *change* in direction between consecutive segments.
- **Threshold**: Direction change < 90° per step.
- **Failure Condition**: "Abrupt turn at index [i] (Turn angle: X deg)."

## Implementation Plan
- [ ] Create `tools/validate_tracks.py`.
- [ ] Implement `check_intersection` function.
- [ ] Implement `check_angles` function.
- [ ] Implement `check_spacing` function.
- [ ] Implement `check_curvature` function.
- [ ] Add main loop to iterate over `tools/tracks/*.json` and report results.
