#!/usr/bin/env python3
"""
GitHub Setup Helper Script for NBA Fantasy Dashboard
This script helps set up the GitHub repository
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if Git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🏀 NBA Fantasy Dashboard - GitHub Setup Helper")
    print("=" * 50)
    
    # Check if Git is installed
    if not check_git_installed():
        print("❌ Git is not installed or not in PATH")
        print("Please install Git from: https://git-scm.com/downloads")
        return
    
    print("✅ Git is installed")
    
    # Check if we're in a git repository
    if os.path.exists('.git'):
        print("✅ Git repository already initialized")
    else:
        if not run_command("git init", "Initializing Git repository"):
            return
    
    # Add all files
    if not run_command("git add .", "Adding files to Git"):
        return
    
    # Check if there are changes to commit
    try:
        result = subprocess.run("git diff --cached --quiet", shell=True, capture_output=True)
        if result.returncode == 0:
            print("ℹ️  No changes to commit")
            return
    except:
        pass
    
    # Commit changes
    if not run_command('git commit -m "Initial NBA Fantasy Dashboard with modular architecture"', "Committing changes"):
        return
    
    print("\n🎉 Git setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Name it: NBA_FantasyDashboard")
    print("   - Make it public")
    print("   - Don't initialize with README")
    print()
    print("2. Add remote origin and push:")
    print("   git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("3. Deploy to Streamlit Cloud:")
    print("   - Go to https://share.streamlit.io")
    print("   - Sign in with GitHub")
    print("   - Click 'New app'")
    print("   - Select your repository")
    print("   - Set main file: nba_fantasy_dashboard.py")
    print("   - Click 'Deploy'")
    print()
    print("🚀 Your dashboard will be live at: https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/")

if __name__ == "__main__":
    main()
