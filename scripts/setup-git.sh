#!/bin/bash
# One-time setup for GitHub integration
# Creates repo, initializes git, pushes first commit

set -e

echo "=========================================="
echo "  F1 Manager - Git & GitHub Setup"
echo "=========================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) not installed."
    echo ""
    echo "Install it from: https://cli.github.com/"
    echo ""
    echo "Windows:   winget install GitHub.cli"
    echo "Mac:       brew install gh"
    echo "Linux:     sudo apt install gh"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "GitHub CLI found"

# Check if authenticated
if ! gh auth status &> /dev/null 2>&1; then
    echo ""
    echo "Not logged into GitHub. Starting authentication..."
    echo ""
    gh auth login
fi

echo "GitHub authenticated"
echo ""

# Git user config
if [ -z "$(git config user.name)" ]; then
    echo "Git user not configured."
    read -p "Enter your name for commits: " GIT_NAME
    git config user.name "$GIT_NAME"
fi

if [ -z "$(git config user.email)" ]; then
    read -p "Enter your email for commits: " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

echo "Git user: $(git config user.name) <$(git config user.email)>"
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "Git initialized"
else
    echo "Git already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Game specific
logs/
*.log

# Temp files
*.tmp
*.bak
EOF
    echo ".gitignore created"
fi

# Initial commit if needed
if [ -z "$(git log --oneline -1 2>/dev/null)" ]; then
    echo "Creating initial commit..."
    git add -A
    git commit -m "Initial commit: F1 Manager game with agent pipeline"
    echo "Initial commit created"
else
    echo "Commits exist"
fi

# Create GitHub repo if no remote
if ! git remote | grep -q "origin"; then
    echo ""
    echo "Creating GitHub repository..."
    echo ""

    # Ask for repo visibility
    echo "Repository visibility:"
    echo "  1. Private (only you can see)"
    echo "  2. Public (anyone can see)"
    read -p "Choose [1/2]: " VISIBILITY

    if [ "$VISIBILITY" = "2" ]; then
        VIS_FLAG="--public"
    else
        VIS_FLAG="--private"
    fi

    # Create repo
    gh repo create f1-manager $VIS_FLAG --source=. --remote=origin --push

    echo ""
    echo "Repository created and pushed!"
else
    echo "Remote already configured"

    # Push if there are unpushed commits
    if ! git push origin main 2>/dev/null; then
        echo "  Pushing to remote..."
        git push -u origin main
    fi
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'local only')"
echo "Branch: $(git branch --show-current)"
echo "Commits: $(git rev-list --count HEAD)"
echo ""
echo "View on GitHub:"
gh repo view --web 2>/dev/null || echo "  (run 'gh repo view --web' to open)"
echo ""
echo "The pipeline will now auto-commit completed features."
echo "=========================================="
