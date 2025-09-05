import streamlit as st
import pandas as pd
import numpy as np

# Import custom modules
from data_processing import (
    load_data, apply_filters, create_fantasy_ranking, 
    get_similar_players, get_team_stats, get_position_stats
)
from visualizations import (
    create_fantasy_distribution_chart, create_top_players_chart,
    create_player_type_pie_chart, create_fantasy_vs_efficiency_scatter,
    create_player_radar_chart, create_correlation_heatmap,
    create_position_analysis_chart, create_team_analysis_chart,
    create_metric_cards_data
)
from utils import (
    get_filter_options, validate_filters, get_player_summary,
    format_percentage, format_stat, calculate_league_averages
)

# Page configuration
st.set_page_config(
    page_title="NBA Fantasy League Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .player-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_cached_data():
    """Get cached data using the data processing module"""
    return load_data()

def main():
    # Header
    st.markdown('<h1 class="main-header">🏀 NBA Fantasy League Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = get_cached_data()
    
    if df.empty:
        st.error("Failed to load data. Please check if the Excel file exists.")
        return
    
    # Get filter options
    filter_options = get_filter_options(df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Position filter
    selected_pos = st.sidebar.selectbox("Position", filter_options['positions'])
    
    # Team filter
    selected_team = st.sidebar.selectbox("Team", filter_options['teams'])
    
    # Age range
    age_range = st.sidebar.slider("Age Range", 
                                 filter_options['age_range'][0], 
                                 filter_options['age_range'][1], 
                                 filter_options['age_range'])
    
    # Minimum games played
    min_games = st.sidebar.slider("Minimum Games Played", 
                                 filter_options['games_range'][0], 
                                 filter_options['games_range'][1], 
                                 20)
    
    # Validate filters
    if not validate_filters(selected_pos, selected_team, age_range, min_games):
        st.error("Invalid filter settings. Please check your selections.")
        return
    
    # Apply filters
    filtered_df = apply_filters(df, selected_pos, selected_team, age_range, min_games)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Top Picks", "📈 Player Analysis", "🔍 Advanced Stats"])
    
    with tab1:
        st.header("📊 League Overview")
        
        # Get metrics data
        metrics = create_metric_cards_data(filtered_df)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Players", metrics['total_players'])
        
        with col2:
            st.metric("Avg Fantasy Points", format_stat(metrics['avg_fantasy']))
        
        with col3:
            st.metric("Top Scorer", metrics['top_scorer'])
        
        with col4:
            st.metric("Most Efficient", metrics['most_efficient'])
        
        # Fantasy points distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_fantasy_distribution_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_top_players_chart(filtered_df, 10)
            st.plotly_chart(fig, use_container_width=True)
        
        # Player type distribution
        fig = create_player_type_pie_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("🎯 Top Fantasy Picks")
        
        # Create fantasy ranking
        ranked_df = create_fantasy_ranking(filtered_df, min_games)
        
        # Display top picks
        st.subheader("🏆 Top 20 Fantasy Picks")
        
        top_20 = ranked_df.head(20)
        
        for idx, player in top_20.iterrows():
            player_summary = get_player_summary(player)
            with st.expander(f"#{player['Fantasy_Rank']} {player_summary['name']} ({player_summary['team']}) - {player_summary['position']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Fantasy Points", format_stat(player_summary['fantasy_points']))
                    st.metric("Points", format_stat(player_summary['points']))
                    st.metric("Rebounds", format_stat(player_summary['rebounds']))
                
                with col2:
                    st.metric("Assists", format_stat(player_summary['assists']))
                    st.metric("Steals", format_stat(player_summary['steals']))
                    st.metric("Blocks", format_stat(player_summary['blocks']))
                
                with col3:
                    st.metric("FG%", format_percentage(player_summary['fg_percentage']))
                    st.metric("3P%", format_percentage(player_summary['three_p_percentage']))
                    st.metric("FT%", format_percentage(player_summary['ft_percentage']))
                
                st.write(f"**Player Type:** {player_summary['player_type']}")
                st.write(f"**Games Played:** {player_summary['games']}")
                st.write(f"**Minutes per Game:** {format_stat(player_summary['minutes'])}")
        
        # Fantasy points vs efficiency scatter plot
        fig = create_fantasy_vs_efficiency_scatter(ranked_df, 50)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📈 Player Analysis")
        
        # Player search
        player_search = st.selectbox("Select a player to analyze:", 
                                   [''] + sorted(filtered_df['Player'].unique().tolist()))
        
        if player_search:
            player_data = filtered_df[filtered_df['Player'] == player_search].iloc[0]
            player_summary = get_player_summary(player_data)
            
            st.subheader(f"📊 {player_search} Analysis")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("Team", player_summary['team'])
                st.metric("Position", player_summary['position'])
                st.metric("Age", player_summary['age'])
                st.metric("Games Played", player_summary['games'])
                st.metric("Player Type", player_summary['player_type'])
            
            with col2:
                # Performance radar chart
                fig = create_player_radar_chart(player_data, player_search, filtered_df)
                st.plotly_chart(fig, use_container_width=True)
            
            # Similar players
            st.subheader("🔍 Similar Players")
            similar_players = get_similar_players(filtered_df, player_search, player_data['Player_Type'], 5)
            
            for idx, similar in similar_players.iterrows():
                st.write(f"• **{similar['Player']}** ({similar['Team']}) - {format_stat(similar['Fantasy_Points'])} fantasy points")
    
    with tab4:
        st.header("🔍 Advanced Statistics")
        
        # Statistical analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlation heatmap
            fig = create_correlation_heatmap(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Position analysis
            position_stats = get_position_stats(filtered_df)
            fig = create_position_analysis_chart(position_stats)
            st.plotly_chart(fig, use_container_width=True)
        
        # Team analysis
        st.subheader("🏀 Team Analysis")
        
        team_stats = get_team_stats(filtered_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_team_analysis_chart(team_stats, 'avg', 15)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_team_analysis_chart(team_stats, 'scatter')
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏀 NBA Fantasy League Dashboard | Built with Streamlit & Plotly</p>
        <p>Data: 2024 NBA Player Statistics | Fantasy scoring: PTS(1) + TRB(1.2) + AST(1.5) + STL(2) + BLK(2) - TOV(1)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
