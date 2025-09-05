# 🚀 Deployment Guide

This guide will help you deploy the NBA Fantasy Dashboard to various platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for version control)
- GitHub account (for hosting)

## 🛠️ Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ezra-dese/NBA_FantasyDashboard.git
   cd NBA_FantasyDashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**
   ```bash
   streamlit run nba_fantasy_dashboard.py
   ```

## 🌐 GitHub Setup

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository"
3. Name it: `NBA_FantasyDashboard`
4. Make it public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Push Your Code

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial NBA Fantasy Dashboard"

# Add remote origin (replace with your GitHub username)
git remote add origin https://github.com/ezra-dese/NBA_FantasyDashboard.git

# Push to GitHub
git push -u origin main
```

## ☁️ Streamlit Cloud Deployment (Recommended)

### Step 1: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `ezra-dese/NBA_FantasyDashboard`
5. Set main file path: `nba_fantasy_dashboard.py`
6. Click "Deploy"

### Step 2: Configure App

Your app will be available at: `https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/`

## 🐳 Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "nba_fantasy_dashboard.py", "--server.address", "0.0.0.0"]
```

### Step 2: Build and Run

```bash
# Build image
docker build -t nba-fantasy-dashboard .

# Run container
docker run -p 8501:8501 nba-fantasy-dashboard
```

## 🚀 Heroku Deployment

### Step 1: Create Heroku Files

Create `Procfile`:
```
web: streamlit run nba_fantasy_dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### Step 2: Deploy to Heroku

```bash
# Install Heroku CLI
# Then run:
heroku create your-app-name
git push heroku main
```

## 🔧 Configuration

### Environment Variables

Create `.env` file for sensitive data:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Streamlit Configuration

The `.streamlit/config.toml` file is already configured for deployment.

## 📊 Performance Optimization

### For Large Datasets

1. **Enable caching**: Already implemented with `@st.cache_data`
2. **Optimize queries**: Use pandas operations efficiently
3. **Limit data**: Filter data early in the pipeline

### For High Traffic

1. **Use Streamlit Cloud Pro**: For better performance
2. **Implement rate limiting**: Add session state management
3. **Cache expensive operations**: Use `@st.cache_data` decorators

## 🔍 Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Data not loading**: Check file paths and permissions
3. **Charts not displaying**: Verify Plotly installation

### Debug Mode

Run with debug information:
```bash
streamlit run nba_fantasy_dashboard.py --logger.level=debug
```

## 📈 Monitoring

### Streamlit Cloud

- Monitor app usage in Streamlit Cloud dashboard
- Check logs for errors
- Monitor performance metrics

### Custom Monitoring

Add logging to track usage:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔄 Updates and Maintenance

### Updating the App

1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub
4. Streamlit Cloud will auto-deploy

### Data Updates

To update the NBA data:
1. Replace `2024NBAplayerStats.xlsx`
2. Commit and push changes
3. App will automatically use new data

## 📞 Support

If you encounter issues:

1. Check the [Issues](https://github.com/ezra-dese/NBA_FantasyDashboard/issues) page
2. Create a new issue with detailed description
3. Include error logs and system information

---

**Happy Deploying! 🚀**
