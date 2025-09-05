# NBA Fantasy Dashboard - GitHub Setup Script
Write-Host "🏀 NBA Fantasy Dashboard - GitHub Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

Write-Host "`nStep 1: Configuring Git with your credentials..." -ForegroundColor Yellow
git config --global user.email "deseezra@gmail.com"
git config --global user.name "ezra-dese"

Write-Host "`nStep 2: Initializing Git repository..." -ForegroundColor Yellow
git init

Write-Host "`nStep 3: Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "`nStep 4: Committing changes..." -ForegroundColor Yellow
git commit -m "Initial NBA Fantasy Dashboard with modular architecture"

Write-Host "`n✅ Git setup completed successfully!" -ForegroundColor Green

Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   - Go to https://github.com/new" -ForegroundColor Gray
Write-Host "   - Name it: NBA_FantasyDashboard" -ForegroundColor Gray
Write-Host "   - Make it public" -ForegroundColor Gray
Write-Host "   - Don't initialize with README" -ForegroundColor Gray

Write-Host "`n2. Add remote origin and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray

Write-Host "`n3. Deploy to Streamlit Cloud:" -ForegroundColor White
Write-Host "   - Go to https://share.streamlit.io" -ForegroundColor Gray
Write-Host "   - Sign in with GitHub" -ForegroundColor Gray
Write-Host "   - Click 'New app'" -ForegroundColor Gray
Write-Host "   - Select your repository" -ForegroundColor Gray
Write-Host "   - Set main file: nba_fantasy_dashboard.py" -ForegroundColor Gray
Write-Host "   - Click 'Deploy'" -ForegroundColor Gray

Write-Host "`n🚀 Your dashboard will be live at: https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/" -ForegroundColor Green

Read-Host "`nPress Enter to continue..."
