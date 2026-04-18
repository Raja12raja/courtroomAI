# 🚀 Quick Start: Connect to GitHub in 3 Steps

## Step 1: Create GitHub Repository (2 minutes)

**Go to:** https://github.com/new

Fill in:
* **Repository name:** `courtroomai-app` (or your choice)
* **Description:** "AI-powered legal document analysis application"
* **Visibility:** ⚪ Public or 🔒 Private (your choice)
* **IMPORTANT:** ❌ Do NOT check these boxes:
  * ❌ Add a README file
  * ❌ Add .gitignore
  * ❌ Choose a license

Click **"Create repository"** button

**Copy the URL** shown (looks like: `https://github.com/YOUR_USERNAME/courtroomai-app.git`)

---

## Step 2: Get Personal Access Token (2 minutes)

**Go to:** https://github.com/settings/tokens

1. Click **"Generate new token"** → **"Generate new token (classic)"**
2. **Note:** Enter "Databricks CourtRoom AI"
3. **Expiration:** Choose "No expiration" or "90 days"
4. **Select scopes:** ☑️ Check **repo** (this checks all sub-items)
5. Scroll down, click **"Generate token"**
6. **COPY THE TOKEN NOW!** (You won't see it again)
   * It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Step 3: Push to GitHub (1 minute)

**Option A: Use the interactive script** (recommended)

```bash
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/
./connect_github.sh
```

Follow the prompts and paste your URL and token when asked.

**Option B: Manual commands**

```bash
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

# Replace YOUR_USERNAME and YOUR_REPO with your actual values
./git_helper.sh remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# This will prompt for username and password
# Username: Your GitHub username
# Password: Paste your Personal Access Token (NOT your GitHub password)
./git_helper.sh push -u origin main
```

---

## ✅ Success! Your Code is on GitHub

After pushing, go to your GitHub repository URL to see your code!

---

## 📝 Daily Workflow

After making changes to your code:

```bash
cd /Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/

# See what changed
./git_helper.sh status

# Stage all changes
./git_helper.sh add .

# Commit with a message
./git_helper.sh commit -m "Description of what you changed"

# Push to GitHub
./git_helper.sh push
```

---

## 🆘 Troubleshooting

**"Authentication failed"**
* Make sure you're using your Personal Access Token as the password, not your GitHub password

**"Repository already exists"**
* If the remote is already added: `./git_helper.sh remote remove origin`
* Then add it again

**"Permission denied"**
* Make sure your Personal Access Token has the `repo` scope checked
* Try generating a new token

**Need to update your token?**
```bash
# Remove old remote
./git_helper.sh remote remove origin

# Add with new URL
./git_helper.sh remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```
