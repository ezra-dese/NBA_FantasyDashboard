# 🚀 Quick GitHub Setup Guide

## Step 1: Install Git (Required)

### Option A: Download Git for Windows (Recommended)
1. Go to: https://git-scm.com/download/win
2. Download the latest version
3. Run the installer with **default settings**
4. **Restart your PowerShell/terminal**

### Option B: Install via Package Manager
If you have Chocolatey:
```powershell
choco install git
```

If you have Winget:
```powershell
winget install --id Git.Git -e --source winget
```

## Step 2: Verify Git Installation
After installing, restart your terminal and run:
```bash
git --version
```
You should see something like: `git version 2.xx.x`

## Step 3: Run the Setup Script
Once Git is installed, run this command in your project folder:
```powershell
.\setup_github.ps1
```

This script will:
- Configure Git with your credentials (deseezra@gmail.com, ezra-dese)
- Initialize the repository
- Add all files
- Commit the changes

## Step 4: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `NBA_FantasyDashboard`
3. Description: `NBA Fantasy League Dashboard built with Streamlit and Plotly`
4. Make it **Public**
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

## Step 5: Connect and Push
After creating the repository, run these commands:
```bash
git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git
git branch -M main
git push -u origin main
```

## Step 6: Deploy to Streamlit Cloud
1. Go to: https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select repository: `ezra-dese/NBA_FantasyDashboard`
5. Main file path: `nba_fantasy_dashboard.py`
6. Click "Deploy"

Your dashboard will be live at: `https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/`

---

## 🆘 Need Help?

If you encounter any issues:
1. Make sure Git is properly installed and restarted your terminal
2. Check that you're in the correct directory: `C:\Users\Ezra\Desktop\NBA_FantasyDashboard`
3. Verify your GitHub username is correct: `ezra-dese`
4. Make sure your email is correct: `deseezra@gmail.com`

## 📁 Your Project Files Ready for Upload

✅ All files are ready:
- `nba_fantasy_dashboard.py` - Main dashboard
- `data_processing.py` - Data module
- `visualizations.py` - Charts module
- `utils.py` - Utilities module
- `ai_chatbot.py` - AI assistant
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `CHANGELOG.md` - Update log
- All configuration files

**Total**: 15+ files ready for GitHub! 🚀
