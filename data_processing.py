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

def calculate_fantasy_points_with_weights(df, weights=None):
    """Calculate fantasy points using custom weights"""
    if weights is None:
        # Default weights
        weights = {
            'PTS': 1.0,
            'TRB': 1.25,
            'AST': 1.5,
            'STL': 2.0,
            'BLK': 2.0,
            'TOV': -1.0
        }
    
    return (
        df['PTS'] * weights['PTS'] +
        df['TRB'] * weights['TRB'] +
        df['AST'] * weights['AST'] +
        df['STL'] * weights['STL'] +
        df['BLK'] * weights['BLK'] +
        df['TOV'] * weights['TOV']
    )

def load_data():
    """Load and preprocess the NBA player data"""
    try:
        df = pd.read_excel('2024NBAplayerStats.xlsx')
        
        # Clean the data
        df = df.dropna(subset=['Player', 'PTS', 'TRB', 'AST'])
        
        # Handle duplicate players (players who played for multiple teams)
        df = handle_duplicate_players(df)
        
        # Calculate fantasy points (standard scoring)
        df['Fantasy_Points'] = calculate_fantasy_points_with_weights(df)
        
        # Calculate efficiency metrics
        df['PER'] = df['PTS'] + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] - df['TOV']
        df['Usage_Rate'] = (df['FGA'] + df['FTA'] * 0.44 + df['AST']) / df['MP'] * 100
        
        # Calculate advanced metrics with error handling
        # Note: eFG% already exists in the Excel file, so we don't need to calculate it
        
        # True Shooting Percentage (TS%) = Pts / (2 * (FGA + .475 * FTA))
        denominator_ts = 2 * (df['FGA'] + 0.475 * df['FTA'])
        df['TS%'] = np.where(denominator_ts > 0, df['PTS'] / denominator_ts, 0)
        
        # Free Throw Rate (FTR) = FT / FGA
        df['FTR'] = np.where(df['FGA'] > 0, df['FT'] / df['FGA'], 0)
        
        # Assist to Turnover ratio
        df['AST_TOV_Ratio'] = np.where(df['TOV'] > 0, df['AST'] / df['TOV'], df['AST'] / 0.1)
        
        # Hollinger Assist Ratio (hAST%) = AST / (FGA + .475 * FTA + AST + TOV)
        denominator_hast = df['FGA'] + 0.475 * df['FTA'] + df['AST'] + df['TOV']
        df['hAST%'] = np.where(denominator_hast > 0, df['AST'] / denominator_hast, 0)
        
        # Turnover Percentage (TOV%) = TOV / (FGA + .475*FTA + AST + TOV)
        denominator_tov = df['FGA'] + 0.475 * df['FTA'] + df['AST'] + df['TOV']
        df['TOV%'] = np.where(denominator_tov > 0, df['TOV'] / denominator_tov, 0)
        
        
        # Create player clusters for similar players
        df = create_player_clusters(df)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def handle_duplicate_players(df):
    """Handle players who played for multiple teams"""
    # Create a copy to work with
    processed_df = df.copy()
    
    # Find players with multiple entries
    player_counts = processed_df['Player'].value_counts()
    duplicate_players = player_counts[player_counts > 1].index.tolist()
    
    # For each duplicate player, keep only the 2TM/3TM row (combined stats)
    for player in duplicate_players:
        player_rows = processed_df[processed_df['Player'] == player]
        
        # Check if there's a 2TM/3TM row
        tm_rows = player_rows[player_rows['Team'].str.contains('TM', na=False)]
        
        if not tm_rows.empty:
            # Keep the 2TM/3TM row and remove individual team rows
            tm_row = tm_rows.iloc[0]
            
            # Extract the last team from the 2TM/3TM notation
            # For now, we'll keep the 2TM/3TM notation but could extract individual teams
            processed_df = processed_df[~((processed_df['Player'] == player) & 
                                        (~processed_df['Team'].str.contains('TM', na=False)))]
        else:
            # If no 2TM/3TM row, keep the row with highest points (simpler approach)
            best_row = player_rows.loc[player_rows['PTS'].idxmax()]
            processed_df = processed_df[~((processed_df['Player'] == player) & 
                                        (processed_df.index != best_row.name))]
    
    return processed_df


def create_player_clusters(df):
    """Create player types using rule-based classification for each position"""
    df['Player_Type'] = 'Other'  # Default type
    
    # Simple classification based on position
    df.loc[df['Pos'] == 'PG', 'Player_Type'] = 'Point Guard'
    df.loc[df['Pos'] == 'SG', 'Player_Type'] = 'Shooting Guard'
    df.loc[df['Pos'] == 'SF', 'Player_Type'] = 'Small Forward'
    df.loc[df['Pos'] == 'PF', 'Player_Type'] = 'Power Forward'
    df.loc[df['Pos'] == 'C', 'Player_Type'] = 'Center'
    
    return df

def apply_filters(df, position='All', team='All', age_range=(19, 40), min_games=20, ppg_range=(0.0, 50.0), fantasy_weights=None):
    """Apply filters to the dataset"""
    filtered_df = df.copy()
    
    if position != 'All':
        filtered_df = filtered_df[filtered_df['Pos'] == position]
    
    if team != 'All':
        filtered_df = filtered_df[filtered_df['Team'] == team]
    
    filtered_df = filtered_df[
        (filtered_df['Age'] >= age_range[0]) & 
        (filtered_df['Age'] <= age_range[1]) &
        (filtered_df['G'] >= min_games) &
        (filtered_df['PTS'] >= ppg_range[0]) &
        (filtered_df['PTS'] <= ppg_range[1])
    ]
    
    # Recalculate fantasy points with custom weights if provided
    if fantasy_weights is not None:
        filtered_df['Fantasy_Points'] = calculate_fantasy_points_with_weights(filtered_df, fantasy_weights)
    
    return filtered_df

def create_fantasy_ranking(df, min_games=20, fantasy_weights=None):
    """Create fantasy ranking based on fantasy points (primary) and other factors"""
    # Filter players with minimum games
    df_filtered = df[df['G'] >= min_games].copy()
    
    # Recalculate fantasy points with custom weights if provided
    if fantasy_weights is not None:
        df_filtered['Fantasy_Points'] = calculate_fantasy_points_with_weights(df_filtered, fantasy_weights)
    
    # Calculate weighted fantasy score
    df_filtered['Weighted_Fantasy_Score'] = (
        df_filtered['Fantasy_Points'] * 0.4 +
        df_filtered['PER'] * 0.3 +
        df_filtered['Usage_Rate'] * 0.2 +
        (df_filtered['FG%'] + df_filtered['3P%'] + df_filtered['FT%']) / 3 * 0.1
    )
    
    # Rank players by Fantasy Points ONLY (as requested)
    df_filtered = df_filtered.sort_values('Fantasy_Points', ascending=False)
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

