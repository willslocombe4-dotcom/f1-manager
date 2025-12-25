# Feature Proposal: Tire Wear Visuals

Based on your request, I checked the backlog. **"Tire System" is currently planned for Phase 2** of the Race Simulation Overhaul, which includes "degradation curves" and "wear interactions".

However, we can design the **visual component** specifically now to make it concrete.

### How It Works
We'll add a visual wear indicator to the Timing Screen so you can see tire life dropping in real-time, not just the lap age.

### Visual Concept
In `ui/timing_screen.py`, we'll update the tire column:

```
[Current]      [Proposed]
TIRE           TIRE
(S) 12         (S) 12  [====--] 70%
(M) 5          (M) 5   [======] 95%
(H) 22         (H) 22  [==----] 30%
```

### Technical Changes
1.  **`race/car.py`**: Add `self.tire_wear` (0-100%) property.
    *   Decrease it per lap based on compound (Softs degrade faster).
2.  **`ui/timing_screen.py`**: Add a small progress bar next to the tire age.
    *   Green (>70%), Yellow (40-70%), Red (<40%).

### Complexity: Low
This is a straightforward addition that prepares the ground for the deeper tire physics in Phase 2.

---

**Do you want to:**
1.  **Build this now?** (I'll hand off to @f1-director)
2.  **Save this design** to the backlog (refining the Phase 2 entry)?