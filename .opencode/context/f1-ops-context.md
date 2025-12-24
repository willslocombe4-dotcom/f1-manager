# F1 Ops Context

**Last Updated:** 2025-12-23

---

## Git History

### Recent Commits
| Date | Type | Message | Files |
|------|------|---------|-------|
| - | - | No commits yet via pipeline | - |

---

## Tracks Imported

| Date | Source | Waypoints | Notes |
|------|--------|-----------|-------|
| - | - | - | No imports yet |

---

## Track Backups

Previous track data before imports (for rollback):

### Current Track
```python
# Backed up before any import
# Will be populated on first import
```

---

## Commit Types Reference

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `style` | Formatting |
| `docs` | Documentation |
| `chore` | Maintenance |
| `tool` | New/updated tool |

---

## Repository Info

**Remote:** origin → https://github.com/willslocombe4-dotcom/f1-manager.git
**Branch:** master

---

## Learnings

### Git Gotchas
<!-- Commands that behaved unexpectedly -->
- [2025-12-24] **Gotcha:** New files not staged with `git add -u` | **Solution:** Use `git add -A` or explicitly add new files

### Track Import Issues
<!-- Format problems, waypoint issues -->

### Commit Patterns
<!-- Message formats that work well -->
- [2025-12-24] **Pattern:** Use `feat:` for new features, `fix:` for bugs | **Benefit:** Clear history, easy to find changes
- [2025-12-24] **Pattern:** List files changed in commit body | **Benefit:** Easy to review without git show

### Workflow Wins
<!-- Sequences of commands that work reliably -->
- [2025-12-24] **Workflow:** `git status` → `git diff` → `git add` → `git commit` → `git push` | **Benefit:** Catches issues before commit
