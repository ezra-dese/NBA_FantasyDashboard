# 🚀 Complete GitHub Setup Guide

## Step 1: Install Git

Since Git is not installed on your system, you need to install it first:

### Option A: Download Git for Windows
1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the latest version for Windows
3. Run the installer with default settings
4. Restart your terminal/PowerShell

### Option B: Install via Package Manager
If you have Chocolatey installed:
```powershell
choco install git
```

If you have Winget installed:
```powershell
winget install --id Git.Git -e --source winget
```

## Step 2: Configure Git with Your Credentials

After installing Git, run these commands in PowerShell:

```bash
git config --global user.email "deseezra@gmail.com"
git config --global user.name "ezra-dese"
```

## Step 3: Initialize and Push to GitHub

### 3.1: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial NBA Fantasy Dashboard with modular architecture"
```

### 3.2: Create GitHub Repository
1. Go to [https://github.com/new](https://github.com/new)
2. Repository name: `NBA_FantasyDashboard`
3. Description: `NBA Fantasy League Dashboard built with Streamlit and Plotly`
4. Make it **Public**
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 3.3: Connect and Push to GitHub
```bash
git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Streamlit Cloud

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select repository: `ezra-dese/NBA_FantasyDashboard`
5. Main file path: `nba_fantasy_dashboard.py`
6. App URL: `nba-fantasy-dashboard` (or any name you prefer)
7. Click "Deploy"

Your dashboard will be live at: `https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/`

## Alternative: Manual File Upload

If you prefer not to install Git right now, you can:

1. **Create the GitHub repository** manually at [https://github.com/new](https://github.com/new)
2. **Upload files directly** using GitHub's web interface:
   - Click "uploading an existing file"
   - Drag and drop all your project files
   - Commit with message: "Initial NBA Fantasy Dashboard"

## Troubleshooting

### If you get authentication errors:
```bash
git config --global credential.helper store
```

### If you need to update the remote URL:
```bash
git remote set-url origin https://github.com/ezra-dese/NBA_FantasyDashboard.git
```

### If you need to force push (be careful!):
```bash
git push -f origin main
```

## Your Project Files Ready for Upload:

✅ `nba_fantasy_dashboard.py` - Main dashboard
✅ `data_processing.py` - Data module  
✅ `visualizations.py` - Charts module
✅ `utils.py` - Utilities module
✅ `requirements.txt` - Dependencies
✅ `README.md` - Documentation
✅ `DEPLOYMENT.md` - Deployment guide
✅ `.streamlit/config.toml` - Streamlit config
✅ `.gitignore` - Git ignore file
✅ `2024NBAplayerStats.xlsx` - Your dataset

All files are ready to be pushed to GitHub! 🚀
