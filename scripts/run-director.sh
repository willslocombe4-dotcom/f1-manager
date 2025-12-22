#!/bin/bash
# Runs the director in autonomous mode
# Human handles: idea-designer, tool-builder
# Director handles: planner -> coder -> bugfix loop
# Pipeline pauses on LOW confidence items

INTERVAL=${1:-30}  # seconds between runs, default 30
LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "=========================================="
echo "  F1 Director - Autonomous Mode"
echo "=========================================="
echo "Checking pipeline every ${INTERVAL}s"
echo "Log: $LOGDIR/director.log"
echo ""
echo "Pipeline pauses automatically when:"
echo "  - Any agent reports LOW confidence"
echo "  - Same bug appears 3+ times"
echo "  - Feature needs human judgment"
echo ""
echo "Check status: ./scripts/status.sh"
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] Running director check..."

    # Run director and capture output
    OUTPUT=$(claude --agent f1-director "Check pipeline and advance work. Report any confidence scores." 2>&1)

    # Log full output
    echo "[$TIMESTAMP]" >> "$LOGDIR/director.log"
    echo "$OUTPUT" >> "$LOGDIR/director.log"
    echo "---" >> "$LOGDIR/director.log"

    # Show summary in terminal
    if echo "$OUTPUT" | grep -q "WAITING_FOR_HUMAN"; then
        echo "[$TIMESTAMP] PAUSED - Human review needed"
        echo "[$TIMESTAMP] Run ./scripts/status.sh for details"
    elif echo "$OUTPUT" | grep -q "Pipeline idle"; then
        echo "[$TIMESTAMP] Idle - waiting for approved ideas"
    else
        echo "[$TIMESTAMP] Work in progress"
    fi

    # Show quick git info
    if [ -d ".git" ]; then
        UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        if [ "$UNCOMMITTED" != "0" ]; then
            echo "[$TIMESTAMP] Git: $UNCOMMITTED uncommitted files"
        fi
    fi

    echo "[$TIMESTAMP] Next check in ${INTERVAL}s..."
    echo ""
    sleep "$INTERVAL"
done
