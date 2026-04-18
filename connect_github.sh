#!/bin/bash
# Interactive GitHub Connection Script

# Set safe directory
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0="safe.directory"
export GIT_CONFIG_VALUE_0="/Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app"

cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

echo "======================================"
echo "GitHub Repository Connection Setup"
echo "======================================"
echo ""

# Check if remote already exists
if git remote get-url origin 2>/dev/null; then
    echo "✓ GitHub remote already configured:"
    git remote get-url origin
    echo ""
    read -p "Do you want to update it? (y/n): " update_remote
    if [ "$update_remote" = "y" ]; then
        git remote remove origin
        echo "✓ Removed existing remote"
    else
        echo "Keeping existing remote"
        exit 0
    fi
fi

echo "First, create your GitHub repository:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: courtroomai-app (or your choice)"
echo "3. Set to Public or Private"
echo "4. DO NOT initialize with README, .gitignore, or license"
echo "5. Click 'Create repository'"
echo ""

read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "Error: Repository URL cannot be empty"
    exit 1
fi

# Add remote
git remote add origin "$repo_url"
echo "✓ Added GitHub remote: $repo_url"
echo ""

echo "Now we'll push your code to GitHub"
echo ""
echo "You'll need a Personal Access Token (not your password):"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Name: Databricks CourtRoom AI"
echo "4. Select scope: ☑ repo"
echo "5. Click 'Generate token'"
echo "6. Copy the token (you won't see it again!)"
echo ""

read -p "Have you created your Personal Access Token? (y/n): " token_ready

if [ "$token_ready" != "y" ]; then
    echo "Please create your token first, then run this script again"
    exit 0
fi

echo ""
echo "Pushing to GitHub..."
echo "When prompted:"
echo "  Username: Your GitHub username"
echo "  Password: Paste your Personal Access Token"
echo ""

# Push to GitHub
if git push -u origin main; then
    echo ""
    echo "======================================"
    echo "✅ SUCCESS!"
    echo "======================================"
    echo ""
    echo "Your code is now on GitHub!"
    echo "View it at: $repo_url"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "1. Invalid Personal Access Token"
    echo "2. Wrong repository URL"
    echo "3. Repository already has content"
    echo ""
    echo "Try running this script again after fixing the issue"
    exit 1
fi
