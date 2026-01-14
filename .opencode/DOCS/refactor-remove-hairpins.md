# Refactor: Remove Explicit Hairpin Generation

## Goal
Remove the explicit perturbation logic (Phase 2) in the track generator to prevent the generation of sharp, jagged hairpin features, resulting in smoother, more flowing tracks defined purely by the radial skeleton.

## Analysis
The current `track_generator.py` employs a procedural generation algorithm with three distinct phases.
**Phase 2: Perturbation** (lines 550-590) explicitly looks for long edges and inserts a displaced midpoint, creating sharp V-shapes or "hairpins". This logic needs to be removed to achieve the desired smoother track style.

## Specs
**File**: `tools/track_generator.py`
**Method**: `generate_procedural`

1.  **Remove Phase 2 (Perturbation)**:
    - Delete or comment out the entire code block (approx lines 556 to 589).
    - This block contains the logic: `if chaos > 0.3: ...` which performs the edge splitting and displacement.

2.  **Clean up Phase 1 Comments**:
    - Remove the comment at line 533: `# Hairpin logic: occasionally force a sequence of High -> Low -> High radius`.
    - This comment describes logic that is not implemented and is confusing.

## Impact Analysis
-   **Track Topology**: The track remains a valid closed loop. Phase 1 generates a sorted list of points around a center, ensuring a non-intersecting star-shaped polygon.
-   **Complexity**: Tracks will be less "jagged". The `chaos` parameter will still affect the *radius variance* in Phase 1, but it will no longer create sharp kinks.

## Next Steps
- [ ] Open `tools/track_generator.py`.
- [ ] Locate and remove the perturbation loop in `generate_procedural`.
- [ ] Remove the misleading comment in Phase 1.
- [ ] Verify track generation by running `python tools/track_generator.py` (or the editor).
