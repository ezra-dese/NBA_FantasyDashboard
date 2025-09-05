@echo off
echo 🏀 NBA Fantasy Dashboard - GitHub Push
echo =====================================

echo.
echo Step 1: Configuring Git with your credentials...
git config --global user.email "deseezra@gmail.com"
git config --global user.name "ezra-dese"

echo.
echo Step 2: Initializing Git repository...
git init

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Committing changes...
git commit -m "NBA Fantasy Dashboard v2.0 - Complete with AI Assistant, Player Tags, and Fixed Rankings"

echo.
echo ✅ Git setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name it: NBA_FantasyDashboard
echo    - Make it public
echo    - Don't initialize with README
echo.
echo 2. Add remote origin and push:
echo    git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy to Streamlit Cloud:
echo    - Go to https://share.streamlit.io
echo    - Sign in with GitHub
echo    - Click 'New app'
echo    - Select your repository
echo    - Set main file: nba_fantasy_dashboard.py
echo    - Click 'Deploy'
echo.
echo 🚀 Your dashboard will be live at: https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/
echo.
pause
