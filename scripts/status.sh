#!/bin/bash
# Quick status check for F1 Director pipeline
# Run anytime: ./scripts/status.sh

CONTEXT_DIR=".claude/context"

echo ""
echo "==========================================="
echo "  F1 MANAGER PIPELINE STATUS"
echo "==========================================="
echo ""

# Pipeline state from director context
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    STATE=$(grep "^Pipeline state:" "$CONTEXT_DIR/director-context.md" | head -1 | sed 's/Pipeline state: //')
    case "$STATE" in
        *WAITING_FOR_HUMAN*) echo "!! PAUSED - Human review needed" ;;
        *RUNNING*) echo ">> RUNNING - Work in progress" ;;
        *) echo "-- IDLE - Waiting for approved ideas" ;;
    esac
else
    echo "-- IDLE - No director context yet"
fi

echo ""

# Current work
echo "CURRENT WORK:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    WORK=$(sed -n '/^## Current Work/,/^## /p' "$CONTEXT_DIR/director-context.md" | grep -v "^##" | grep -v "^\[" | grep -v "^$" | head -3)
    if [ -n "$WORK" ]; then
        echo "$WORK" | sed 's/^/   /'
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Agent statuses
echo "AGENT STATUS:"
for agent in feature-planner feature-coder bug-fixer; do
    if [ -f "$CONTEXT_DIR/${agent}-context.md" ]; then
        STATUS=$(grep "^STATUS:" "$CONTEXT_DIR/${agent}-context.md" | head -1 | sed 's/STATUS: //')
        printf "   %-18s %s\n" "$agent:" "$STATUS"
    fi
done

echo ""

# Queued ideas (only show actual queued items, not template)
echo "QUEUED IDEAS:"
if [ -f "$CONTEXT_DIR/idea-designer-context.md" ]; then
    # Look for lines with "Status: QUEUED" and get the idea name from the line before
    QUEUED=$(grep -B2 "^Status: QUEUED" "$CONTEXT_DIR/idea-designer-context.md" 2>/dev/null | grep "^###\|^-" | sed 's/^### /   /' | sed 's/^- /   /')
    if [ -n "$QUEUED" ]; then
        echo "$QUEUED"
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Waiting for human
echo "WAITING FOR HUMAN:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    WAITING=$(sed -n '/^## Waiting For Human/,/^## /p' "$CONTEXT_DIR/director-context.md" | grep "^-" | head -5 | sed 's/^/   /')
    if [ -n "$WAITING" ]; then
        echo "$WAITING"
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Needs review
echo "NEEDS REVIEW:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    REVIEW=$(sed -n '/^## Needs Review/,/^## /p' "$CONTEXT_DIR/director-context.md" | grep "^-" | head -5 | sed 's/^/   /')
    if [ -n "$REVIEW" ]; then
        echo "$REVIEW"
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Recently completed
echo "COMPLETED THIS SESSION:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    COMPLETED=$(sed -n '/^## Completed This Session/,/^## /p' "$CONTEXT_DIR/director-context.md" | grep "^-\|^###" | head -5 | sed 's/^### /   /' | sed 's/^- /   /')
    if [ -n "$COMPLETED" ]; then
        echo "$COMPLETED"
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Blocked
echo "BLOCKED:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    BLOCKED=$(sed -n '/^## Blocked Items/,/^## /p' "$CONTEXT_DIR/director-context.md" | grep "^-" | head -5 | sed 's/^/   /')
    if [ -n "$BLOCKED" ]; then
        echo "$BLOCKED"
    else
        echo "   (none)"
    fi
else
    echo "   (none)"
fi

echo ""

# Git status
echo "GIT STATUS:"
if [ -d ".git" ]; then
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    LAST_COMMIT=$(git log -1 --format="%h %s" 2>/dev/null || echo "no commits")
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "no remote")

    echo "   Branch: $BRANCH"
    echo "   Uncommitted: $CHANGES files"
    echo "   Last commit: $LAST_COMMIT"
    echo "   Remote: $REMOTE"

    # Check if ahead/behind remote
    if git remote | grep -q "origin"; then
        AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
        BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
        if [ "$AHEAD" != "0" ] || [ "$BEHIND" != "0" ]; then
            echo "   Sync: $AHEAD ahead, $BEHIND behind"
        fi
    fi
else
    echo "   (not a git repository - run ./scripts/setup-git.sh)"
fi

echo ""

# Last activity
echo "LAST RUN:"
if [ -f "$CONTEXT_DIR/director-context.md" ]; then
    LAST_RUN=$(grep "^Last run:" "$CONTEXT_DIR/director-context.md" | head -1 | sed 's/Last run: /   /')
    echo "$LAST_RUN"
else
    echo "   (never)"
fi

echo ""
echo "==========================================="
echo ""
echo "Commands:"
echo "  ./scripts/run-director.sh        Start autonomous mode"
echo "  ./scripts/status.sh              This status view"
echo "  claude --agent f1-idea-designer  Add new ideas"
echo "  claude --agent f1-director \"run\" Run director once"
echo "  python main.py                   Test the game"
echo ""
