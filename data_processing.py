"""
Data processing module for NBA Fantasy Dashboard
Handles data loading, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load and preprocess the NBA player data"""
    try:
        df = pd.read_excel('2024NBAplayerStats.xlsx')
        
        # Clean the data
        df = df.dropna(subset=['Player', 'PTS', 'TRB', 'AST'])
        
        # Calculate fantasy points (standard scoring)
        df['Fantasy_Points'] = (
            df['PTS'] * 1 +           # Points
            df['TRB'] * 1.2 +         # Rebounds
            df['AST'] * 1.5 +         # Assists
            df['STL'] * 2 +           # Steals
            df['BLK'] * 2 +           # Blocks
            df['TOV'] * -1            # Turnovers (negative)
        )
        
        # Calculate efficiency metrics
        df['PER'] = df['PTS'] + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] - df['TOV']
        df['Usage_Rate'] = (df['FGA'] + df['FTA'] * 0.44 + df['AST']) / df['MP'] * 100
        
        # Create player clusters for similar players
        df = create_player_clusters(df)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def create_player_clusters(df):
    """Create player clusters for similar players using K-means"""
    features_for_clustering = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%']
    clustering_data = df[features_for_clustering].fillna(0)
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['Player_Type'] = kmeans.fit_predict(scaled_data)
    
    # Map cluster numbers to player types
    cluster_mapping = {
        0: 'Scoring Guard',
        1: 'All-Around Forward',
        2: 'Defensive Specialist',
        3: 'Playmaking Guard',
        4: 'Big Man'
    }
    df['Player_Type'] = df['Player_Type'].map(cluster_mapping)
    
    return df

def apply_filters(df, position='All', team='All', age_range=(19, 40), min_games=20):
    """Apply filters to the dataset"""
    filtered_df = df.copy()
    
    if position != 'All':
        filtered_df = filtered_df[filtered_df['Pos'] == position]
    
    if team != 'All':
        filtered_df = filtered_df[filtered_df['Team'] == team]
    
    filtered_df = filtered_df[
        (filtered_df['Age'] >= age_range[0]) & 
        (filtered_df['Age'] <= age_range[1]) &
        (filtered_df['G'] >= min_games)
    ]
    
    return filtered_df

def create_fantasy_ranking(df, min_games=20):
    """Create fantasy ranking based on multiple factors"""
    # Filter players with minimum games
    df_filtered = df[df['G'] >= min_games].copy()
    
    # Calculate weighted fantasy score
    df_filtered['Weighted_Fantasy_Score'] = (
        df_filtered['Fantasy_Points'] * 0.4 +
        df_filtered['PER'] * 0.3 +
        df_filtered['Usage_Rate'] * 0.2 +
        (df_filtered['FG%'] + df_filtered['3P%'] + df_filtered['FT%']) / 3 * 0.1
    )
    
    # Rank players
    df_filtered = df_filtered.sort_values('Weighted_Fantasy_Score', ascending=False)
    df_filtered['Fantasy_Rank'] = range(1, len(df_filtered) + 1)
    
    return df_filtered

def get_similar_players(df, player_name, player_type, top_n=5):
    """Get similar players based on player type and fantasy points"""
    similar_players = df[
        (df['Player_Type'] == player_type) &
        (df['Player'] != player_name)
    ].nlargest(top_n, 'Fantasy_Points')
    
    return similar_players

def get_team_stats(df):
    """Calculate team statistics"""
    team_stats = df.groupby('Team').agg({
        'Fantasy_Points': ['mean', 'sum'],
        'Player': 'count'
    }).round(1)
    
    team_stats.columns = ['Avg_Fantasy_Points', 'Total_Fantasy_Points', 'Player_Count']
    team_stats = team_stats.sort_values('Avg_Fantasy_Points', ascending=False)
    
    return team_stats

def get_position_stats(df):
    """Calculate position-based statistics"""
    position_stats = df.groupby('Pos').agg({
        'Fantasy_Points': 'mean',
        'PTS': 'mean',
        'TRB': 'mean',
        'AST': 'mean'
    }).round(1)
    
    return position_stats
