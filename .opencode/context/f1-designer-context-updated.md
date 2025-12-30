# F1 Designer Context

**Last Updated:** 2025-12-28

---

## Feature Backlog

Ideas saved for later implementation:

| # | Feature | Priority | Complexity | Added | Status | Depends On |
|---|---------|----------|------------|-------|--------|------------|
| 1 | Phase 1: Foundation | HIGH | LARGE | 2025-12-22 | ✅ DONE | — |
| 2 | Phase 2: Advanced Tire System | HIGH | MEDIUM | 2025-12-22 | Pending | #1 |
| 3 | Phase 3: Proximity Racing | HIGH | LARGE | 2025-12-22 | Pending | #1 |
| 4 | Phase 4: Drama & Chaos | MEDIUM | LARGE | 2025-12-22 | Pending | #1 |
| 5 | Tire Wear Bar on Timing Screen | LOW | SMALL | 2025-12-24 | Pending | #1 |
| 6 | Main Menu + Settings System | HIGH | HIGH | 2025-12-24 | ✅ DONE | — |
| 7 | Career Mode - Core Systems | HIGH | LARGE | 2025-12-27 | Pending | — |
| 8 | Smart Track Boundaries (Kerb Fix) | HIGH | MEDIUM | 2025-12-25 | ✅ DONE | — |
| 9 | Qualifying Weekend Mode | HIGH | LARGE | 2025-12-27 | Pending | #1 |
| 10 | Dynamic Pit Strategy Manager | HIGH | MEDIUM | 2025-12-27 | Pending | #1 |
| 11 | Tire Performance Graph | HIGH | SMALL | 2025-12-27 | Pending | #1 |
| 12 | Race Strategy Timeline | HIGH | MEDIUM | 2025-12-27 | Pending | #1 |
| 13 | Team Radio Commands (Simplified) | MEDIUM | MEDIUM | 2025-12-27 | Pending | #1 |
| 14 | Pit Window Strategy Overlay | MEDIUM | SMALL | 2025-12-27 | Pending | #1 |
| 15 | Sector Indicators (Refined) | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 16 | Race Start Lights (Refined) | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 17 | Live Position Mini-Map | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 18 | Display Settings & Menu Rename | HIGH | SMALL | 2025-12-28 | Pending | — |

**Status Legend:**
- ✅ DONE - Fully implemented and working
- 🔧 PARTIAL - Started but not complete
- Pending - Not started

**Total:** 18 features (3 complete, 0 partial, 15 pending)

---

## What's Actually In The Game

### ✅ Fully Implemented:
1. **Phase 1: Foundation**
   - 2025 F1 grid (all 10 teams, 20 drivers)
   - Team performance tiers (S/A/B/C/D)
   - Car characteristics (balance, cornering, traction)
   - Driver attributes (skill, consistency, racecraft, style, rookie status)
   - Driver-car synergy system
   - Fuel load effects (heavy → light)
   - AI-controlled pit stops
   - Tire degradation with cliff effect
   - Basic race simulation with timing tower
   - Results screen with scrolling

2. **Main Menu + Settings System**
   - Main menu with all options
   - Track selection screen (working)
   - Settings menu with categories
   - Runtime config system
   - Settings persistence (save/load)
   - Most gameplay settings implemented
   - Teams/Drivers settings are placeholders

3. **Smart Track Boundaries**
   - Fixed kerb rendering at hairpins
   - Bevel-join system for corners
   - No more visual glitches

### ❌ Not Implemented:
- Advanced tire thermal model
- Proximity racing (dirty air, DRS, slipstream)
- Drama systems (errors, safety cars, failures)
- Career mode (entire system)
- Strategic features (manual pit stops, radio commands, etc.)
- Display/resolution settings

---

## Feature Details

### #18: Display Settings & Menu Rename
**Priority:** HIGH | **Complexity:** SMALL | **Added:** 2025-12-28 | **Status:** Pending

Rename current "Settings" to "Config" and add new "Settings" for display options.

**Changes:**
1. **Main Menu rename:**
   - "SETTINGS" → "CONFIG" (for gameplay configuration)
   - Add new "SETTINGS" option (for display/video settings)

2. **New Settings Screen features:**
   - Fullscreen mode (always on)
   - Resolution display (auto-detected, e.g., 3840x2160)
   - UI scaling (automatic based on resolution)
   - Future: UI scale slider, performance options

**Implementation:**
- Auto-detect native screen resolution on startup
- Calculate scale factor from base 1600x900
- Scale all UI elements proportionally (track, cars, fonts, spacing)
- Game always launches in fullscreen at native resolution
- Settings screen shows current resolution for reference

**Why needed:**
- Current 1600x900 window is too small on 4K displays
- Fullscreen provides better immersion
- Auto-scaling ensures UI is readable at any resolution

---

## Learnings

### User Preferences
<!-- What they like, what they reject, their style -->
- [2025-12-24] **Preference:** User wants agents to learn and improve over time | **Lesson:** Build learning systems into agent workflows
- [2025-12-27] **Preference:** User likes using multiple agents in parallel for brainstorming | **Lesson:** Kick off 10 agents to explore different angles of complex features
- [2025-12-28] **Preference:** User has 4K display (3840x2160) and wants fullscreen | **Lesson:** Consider high-res displays in UI design

### Conversation Wins
<!-- Approaches that led to good designs -->
- [2025-12-24] **Win:** Ask 1-2 questions per exchange, not 5+ | **Lesson:** Keeps conversation flowing naturally
- [2025-12-27] **Win:** Parallel agent exploration for complex features | **Lesson:** 10 agents exploring different aspects (UI, mechanics, AI, etc.) produces comprehensive designs quickly
- [2025-12-28] **Win:** Quick clarification on naming confusion | **Lesson:** Verify understanding before assuming intent

### Codebase Constraints
<!-- Technical limits that affect design -->
- [2025-12-24] **Constraint:** Settings system uses RuntimeConfig singleton | **Lesson:** New features with config must integrate with it
- [2025-12-24] **Constraint:** UI screens cache values at creation | **Lesson:** Designs must account for cache invalidation
- [2025-12-28] **Constraint:** Game hardcoded to 1600x900 resolution | **Lesson:** Need dynamic sizing for different displays

### Design Revisions
<!-- Designs that needed changes, why -->
- [2025-12-24] **Revision:** Track selection initially started race on select | **Lesson:** Confirm UX flow with user before finalizing

---

### ⚠️ Build Order Note
Career Mode can now be built since Main Menu exists.

### 📋 Career Mode Design
**Full design document saved at:** `.opencode/context/f1-career-mode-design.md`
- Streamlined from 23 phases to 8 core systems
- Ready for implementation by @f1-director

---

## Session History

### 2025-12-22 - Race Simulation Brainstorm
- **Duration:** Extended session
- **Outcome:** Complete 4-phase design saved to backlog
- **Notes:** Very productive session, user engaged with all aspects

### 2025-12-25 - Track Boundary Bug Fix Design
- **Duration:** Short session
- **Outcome:** Smart Track Boundaries (#8) saved to backlog
- **Notes:** User wanted long-term fix for all tracks. Researched Shapely's offset_curve for prior art. Chose arc interpolation over miter/bevel for smoother kerb appearance. User deferred to my recommendation when unsure.

### 2025-12-27 - Qualifying Weekend Mode Design
- **Duration:** Extended session (10+ agents used)
- **Outcome:** Complete qualifying weekend design (#9) saved to backlog
- **Notes:** User requested 10 agents to explore the idea. Covered: practice simulation, driver feedback, setup system, tire allocation, Q1/Q2/Q3 format, traffic mechanics, AI behavior, UI design, state machine. User confirmed: no crew conflict (both drivers can go out), 6 soft tire sets, simulated practice with driver feedback.

### 2025-12-27 - Strategic Features Brainstorm & Refinement
- **Duration:** Extended session (5 evaluation agents + 3 refinement agents)
- **Outcome:** Added 8 refined features (#10-17) to backlog
- **Notes:** User noticed initial brainstorm didn't consider codebase constraints. Re-ran agents with proper context about 2D pygame game. Evaluated 12 features for authenticity, feasibility, and fit. Kept 5, modified 3, removed 4. Final features focus on strategic depth while maintaining "watching races unfold" philosophy.

### 2025-12-27 - Career Mode 23 Phases Deep Dive
- **Duration:** Extended session (23 parallel agents)
- **Outcome:** Explored all 23 phases of Career Mode with detailed ideas
- **Progress:** Completed refining Phases 1-4 (Team Selection, Season Calendar, Driver Management, Contract Negotiations)
- **Key Refinements:** 
  - Phase 1: Removed video pitches and negotiation mini-game, added AI-first design with simple scoring
  - Phase 2: Integrated fatigue with development days, removed regional bonuses
  - Phase 3: Added AI personality types for driver management
  - Phase 4: Added dynamic demands based on performance, "selling the project" system
- **Next Session:** Continue from Phase 5 (Car Development)
- **User Preferences:** Wants AI to be competitive, systems must work for both player and AI, no fake bonuses or penalties

### 2025-12-27 - Career Mode Streamlined to Core Systems
- **Duration:** Extended session (continuation of above)
- **Outcome:** Streamlined 23 phases down to 8 core systems
- **Final Design:** Saved to `.opencode/context/f1-career-mode-design.md`
- **Core Systems:**
  1. Team Selection (already refined)
  2. Season Calendar (already refined)
  3. Driver Management (already refined)
  4. Contract Negotiations (already refined)
  5. Car Development (money-driven upgrades)
  6. Financial System (sponsors + prize money)
  7. Staff & Facilities (2 staff, 2 facilities)
  8. Save/Load System
- **Key Decisions:**
  - Money is the universal resource (no abstract points)
  - Everything interconnects through financial flow
  - Built with expansion hooks for future features
  - AI teams use exact same systems as player
- **Ready for:** Implementation by @f1-director

### 2025-12-28 - Backlog Reality Check & Display Settings
- **Duration:** Short session
- **Outcome:** Updated backlog to reflect actual implementation status from GitHub commits
- **Key Findings:**
  - Phase 1 is fully implemented ✅
  - Main Menu + Settings are fully implemented ✅
  - Track boundaries fixed ✅
  - Career Mode still pending
- **New Feature:** Display Settings & Menu Rename (#18)
  - Rename "Settings" to "Config" for gameplay settings
  - Add new "Settings" for display/video options
  - Fullscreen mode with auto-scaling for 4K displays
- **User Setup:** Has 3840x2160 (4K) display, needs fullscreen support

---

## User Preferences Summary

### What They Like
- Drama and emergent stories
- Simcade feel (deep but accessible)
- Driver skill should matter
- Last lap battles, safety cars, mechanical failures
- Using multiple agents in parallel for complex designs
- AI teams that compete fairly (no fake bonuses)
- Fullscreen gaming experience

### Visual Preferences
- ASCII mockups work well
- Appreciates detailed specifications
- Needs UI scaling for 4K displays

---

## Design Patterns

### What Works
- Start with proposal, refine through conversation
- Ground designs in existing codebase
- Be honest about complexity
- Kick off 10+ agents for complex features
- Check implementation status before assuming
- Quick back-and-forth to clarify intent

---

## Next Steps

### Immediate Priorities:
1. **Display Settings & Menu Rename (#18)** - Quick win for better UX
2. **Career Mode (#7)** - Full design ready, transforms the game
3. **Phase 2: Advanced Tire System (#2)** - Build on existing system

### Future Features:
- Proximity racing (#3)
- Strategic features (#10-17)
- Drama & chaos (#4)