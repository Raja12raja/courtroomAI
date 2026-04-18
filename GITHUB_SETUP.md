# GitHub Setup Instructions

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "courtroomai-app")
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL (e.g., `https://github.com/yourusername/courtroomai-app.git`)

## Step 2: Connect Your Local Repo to GitHub

Run these commands from Databricks:

```bash
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

# Add your GitHub repository as remote (replace with your actual repo URL)
./git_helper.sh remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
./git_helper.sh push -u origin main
```

When prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (NOT your GitHub password)

## Step 3: Generate GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Databricks CourtRoom AI")
4. Select scopes:
   - ✅ **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

## Step 4: Daily Workflow

After making changes:

```bash
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

# Check what changed
./git_helper.sh status

# Add changes
./git_helper.sh add .

# Commit
./git_helper.sh commit -m "Your commit message here"

# Push to GitHub
./git_helper.sh push
```

## Quick Commands Reference

```bash
# Status
./git_helper.sh status

# View changes
./git_helper.sh diff

# Commit history
./git_helper.sh log --oneline

# Push changes
./git_helper.sh push

# Pull updates
./git_helper.sh pull
```

## Note on .env File

Your `.env` file is automatically excluded from Git (it's in `.gitignore`).
This keeps your API keys and secrets safe!
