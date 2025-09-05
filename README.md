# 🏀 NBA Fantasy League Dashboard

A comprehensive Streamlit-based dashboard for NBA fantasy league analysis and player prediction. This dashboard helps fantasy basketball players make informed decisions by analyzing player statistics, predicting fantasy value, and providing detailed insights.

## ✨ Features

### 📊 **Overview Dashboard**
- League-wide statistics and key metrics
- Fantasy points distribution analysis
- Player type categorization (Scoring Guard, All-Around Forward, etc.)
- Interactive visualizations with Plotly

### 🎯 **Top Picks Analysis**
- AI-powered fantasy ranking system
- Top 20 recommended picks with detailed breakdowns
- Weighted scoring algorithm considering multiple factors
- Player comparison and efficiency analysis

### 📈 **Individual Player Analysis**
- Detailed player performance radar charts
- Similar player recommendations using clustering
- Comprehensive stat breakdowns
- Performance trend analysis

### 🔍 **Advanced Statistics**
- Statistical correlation analysis
- Position-based performance metrics
- Team analysis and comparisons
- Interactive data exploration

## 🏗️ **Modular Architecture**

The dashboard is built with a clean, modular architecture for better maintainability and scalability:

- **`data_processing.py`**: Handles data loading, cleaning, and preprocessing
- **`visualizations.py`**: Contains all chart and plot creation functions
- **`utils.py`**: Helper functions, calculations, and utility methods
- **`nba_fantasy_dashboard.py`**: Main Streamlit application that orchestrates everything

This modular design makes the code:
- ✅ **Easier to maintain** and debug
- ✅ **More testable** with isolated functions
- ✅ **Reusable** across different projects
- ✅ **Scalable** for future enhancements

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/NBA_FantasyDashboard.git
   cd NBA_FantasyDashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run nba_fantasy_dashboard.py
   ```

4. **Open your browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, copy the URL from the terminal

## 📁 Project Structure

```
NBA_FantasyDashboard/
├── nba_fantasy_dashboard.py    # Main Streamlit application
├── data_processing.py          # Data loading and preprocessing module
├── visualizations.py           # Chart and plot creation module
├── utils.py                    # Helper functions and utilities
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
├── 2024NBAplayerStats.xlsx    # NBA player statistics dataset
├── README.md                  # This file
├── DEPLOYMENT.md              # Deployment guide
├── .gitignore                 # Git ignore file
└── .streamlit/                # Streamlit configuration
    └── config.toml
```

## 🎮 How to Use

### 1. **Filter Players**
Use the sidebar filters to narrow down players by:
- Position (PG, SG, SF, PF, C)
- Team
- Age range
- Minimum games played

### 2. **Explore Top Picks**
- Navigate to the "🎯 Top Picks" tab
- Review the AI-ranked fantasy players
- Click on any player for detailed statistics
- Use the scatter plot to compare efficiency vs fantasy points

### 3. **Analyze Individual Players**
- Go to "📈 Player Analysis" tab
- Select a player from the dropdown
- View their performance radar chart
- Discover similar players for comparison

### 4. **Advanced Analytics**
- Check "🔍 Advanced Stats" for deeper insights
- Explore statistical correlations
- Compare team performances
- Analyze position-based trends

## 🧮 Fantasy Scoring System

The dashboard uses a comprehensive fantasy scoring system:

- **Points**: 1 point per point scored
- **Rebounds**: 1.2 points per rebound
- **Assists**: 1.5 points per assist
- **Steals**: 2 points per steal
- **Blocks**: 2 points per block
- **Turnovers**: -1 point per turnover

### Weighted Fantasy Score Formula
```
Weighted Score = (Fantasy Points × 0.4) + (PER × 0.3) + (Usage Rate × 0.2) + (Shooting % × 0.1)
```

## 🌐 Deploying to GitHub Pages

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial NBA Fantasy Dashboard"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `ezra-dese/NBA_FantasyDashboard`
   - Set main file path: `nba_fantasy_dashboard.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://ezra-dese-nba-fantasydashboard-app-xxxxx.streamlit.app/`

> 📖 **Detailed deployment instructions**: See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive setup guides.

### Option 2: Heroku Deployment

1. **Create a Procfile**
   ```bash
   echo "web: streamlit run nba_fantasy_dashboard.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Create setup.sh**
   ```bash
   echo "mkdir -p ~/.streamlit/
   echo \"[server]
   headless = true
   port = $PORT
   enableCORS = false
   \" > ~/.streamlit/config.toml" > setup.sh
   ```

3. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "nba_fantasy_dashboard.py", "--server.address", "0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t nba-fantasy-dashboard .
   docker run -p 8501:8501 nba-fantasy-dashboard
   ```

## 🔧 Configuration

### Streamlit Configuration
Create `.streamlit/config.toml` for custom settings:

```toml
[server]
headless = true
port = 8501
enableCORS = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 📊 Data Source

The dashboard uses 2024 NBA player statistics including:
- Basic stats (Points, Rebounds, Assists, etc.)
- Shooting percentages (FG%, 3P%, FT%)
- Advanced metrics (Usage Rate, Efficiency Rating)
- Player information (Team, Position, Age, Games Played)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NBA for providing player statistics
- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- The fantasy basketball community for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/NBA_FantasyDashboard/issues) page
2. Create a new issue with detailed description
3. Contact: [your-email@example.com]

---

**Happy Fantasy Basketball! 🏀**

*Built with ❤️ using Streamlit and Plotly*
