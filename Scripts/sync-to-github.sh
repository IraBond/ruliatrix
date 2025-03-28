#!/bin/bash
# Ensure this script is executable
chmod +x "$0"

# 🌐 Ruliatrix GitHub Sync Script
# Created by Marley for Brian Nachenberg

# 🔐 Token-authenticated remote setup (only once)
if [[ $(git remote get-url origin) != *github_pat_* ]]; then
  echo "🔑 Updating Git remote with token auth..."
  git remote set-url origin https://$GH_TOKEN_RULIATRIX@github.com/IraBond/ruliatrix.git
fi

# 💠 Symbolic timestamp commit message
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
commit_message="🧠 Ruliatrix Sync — Fractal state update @ $timestamp"

# 📊 Status check
echo 🔍 Checking for changes to commit...
git status

# ✅ Stage all modified files
git add .

# ✅ Commit with symbolic message
git commit -m "$commit_message"

# 🚀 Push to GitHub with upstream tracking
git push -u origin main

echo 🌈 GitHub sync complete!