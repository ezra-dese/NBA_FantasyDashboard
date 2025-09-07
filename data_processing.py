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
        
        # Handle duplicate players (players who played for multiple teams)
        df = handle_duplicate_players(df)
        
        # Calculate fantasy points (standard scoring)
        df['Fantasy_Points'] = (
            df['PTS'] * 1 +           # Points
            df['TRB'] * 1.25 +         # Rebounds
            df['AST'] * 1.5 +         # Assists
            df['STL'] * 2 +           # Steals
            df['BLK'] * 2 +           # Blocks
            df['TOV'] * -1            # Turnovers (negative)
        )
        
        # Calculate efficiency metrics
        df['PER'] = df['PTS'] + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] - df['TOV']
        df['Usage_Rate'] = (df['FGA'] + df['FTA'] * 0.44 + df['AST']) / df['MP'] * 100
        
        # Calculate advanced metrics
        # Effective Field Goal Percentage (eFG%) = (FG + .5 * 3P) / FGA
        df['eFG%'] = (df['FG'] + 0.5 * df['3P']) / df['FGA']
        
        # True Shooting Percentage (TS%) = Pts / (2 * (FGA + .475 * FTA))
        df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.475 * df['FTA']))
        
        # Free Throw Rate (FTR) = FT / FGA
        df['FTR'] = df['FT'] / df['FGA']
        
        # Assist to Turnover ratio
        df['AST_TOV_Ratio'] = df['AST'] / df['TOV'].replace(0, 0.1)  # Avoid division by zero
        
        # Hollinger Assist Ratio (hAST%) = AST / (FGA + .475 * FTA + AST + TOV)
        df['hAST%'] = df['AST'] / (df['FGA'] + 0.475 * df['FTA'] + df['AST'] + df['TOV'])
        
        # Turnover Percentage (TOV%) = TOV / (FGA + .475*FTA + AST + TOV)
        df['TOV%'] = df['TOV'] / (df['FGA'] + 0.475 * df['FTA'] + df['AST'] + df['TOV'])
        
        
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
            # If no 2TM/3TM row, keep the row with highest fantasy points
            # Calculate fantasy points for comparison
            player_rows_copy = player_rows.copy()
            player_rows_copy['temp_fantasy'] = (
                player_rows_copy['PTS'] * 1 + 
                player_rows_copy['TRB'] * 1.2 + 
                player_rows_copy['AST'] * 1.5 + 
                player_rows_copy['STL'] * 2 + 
                player_rows_copy['BLK'] * 2 - 
                player_rows_copy['TOV']
            )
            
            # Keep the row with highest fantasy points
            best_row = player_rows_copy.loc[player_rows_copy['temp_fantasy'].idxmax()]
            processed_df = processed_df[~((processed_df['Player'] == player) & 
                                        (processed_df.index != best_row.name))]
    
    return processed_df


def create_player_clusters(df):
    """Create player types using rule-based classification for each position"""
    df['Player_Type'] = 'Other'  # Default type
    
    # Point Guards (PG) - Rule-based classification
    pg_mask = df['Pos'] == 'PG'
    if pg_mask.sum() > 0:
        pg_data = df[pg_mask].copy()
        
        # Apply rules with priority order
        playmaking_pg = (pg_data['AST'] > 5)
        defensive_pg = (pg_data['STL'] > 1) & (~playmaking_pg)  # Only if not already playmaking
        scoring_pg = ~(playmaking_pg | defensive_pg)  # Everyone else
        
        df.loc[pg_mask & playmaking_pg, 'Player_Type'] = 'Playmaking Guard'
        df.loc[pg_mask & defensive_pg, 'Player_Type'] = 'Defensive Guard'
        df.loc[pg_mask & scoring_pg, 'Player_Type'] = 'Scoring Guard'
    
    # Shooting Guards (SG) - Rule-based classification
    sg_mask = df['Pos'] == 'SG'
    if sg_mask.sum() > 0:
        sg_data = df[sg_mask].copy()
        
        # Apply rules with priority order
        playmaking_sg = (sg_data['AST'] > 5)
        defensive_sg = (sg_data['STL'] > 1) & (~playmaking_sg)  # Only if not already playmaking
        scoring_sg = ~(playmaking_sg | defensive_sg)  # Everyone else
        
        df.loc[sg_mask & playmaking_sg, 'Player_Type'] = 'Playmaking Guard'
        df.loc[sg_mask & defensive_sg, 'Player_Type'] = 'Defensive Guard'
        df.loc[sg_mask & scoring_sg, 'Player_Type'] = 'Scoring Guard'
    
    # Small Forwards (SF) - Rule-based classification
    sf_mask = df['Pos'] == 'SF'
    if sf_mask.sum() > 0:
        sf_data = df[sf_mask].copy()
        
        # Apply rules with priority order
        wing_defender = (sf_data['STL'] > 1)
        wing_scorer = (sf_data['PTS'] > 10) & (~wing_defender)  # Only if not already defender
        three_d_player = ~(wing_defender | wing_scorer)  # Everyone else
        
        df.loc[sf_mask & wing_defender, 'Player_Type'] = 'Wing Defender'
        df.loc[sf_mask & wing_scorer, 'Player_Type'] = 'Wing Scorer'
        df.loc[sf_mask & three_d_player, 'Player_Type'] = '3&D Player'
    
    # Power Forwards (PF) - Rule-based classification
    pf_mask = df['Pos'] == 'PF'
    if pf_mask.sum() > 0:
        pf_data = df[pf_mask].copy()
        
        # Apply rules with priority order
        playmaking_big = (pf_data['AST'] > 3)
        rim_protector = (pf_data['BLK'] > 1) & (~playmaking_big)  # Only if not already playmaking
        glass_cleaner = ~(playmaking_big | rim_protector)  # Everyone else
        
        df.loc[pf_mask & playmaking_big, 'Player_Type'] = 'Playmaking Big'
        df.loc[pf_mask & rim_protector, 'Player_Type'] = 'Rim Protector'
        df.loc[pf_mask & glass_cleaner, 'Player_Type'] = 'Glass Cleaner'
    
    # Centers (C) - Rule-based classification
    c_mask = df['Pos'] == 'C'
    if c_mask.sum() > 0:
        c_data = df[c_mask].copy()
        
        # Apply rules with priority order
        playmaking_big = (c_data['AST'] > 3)
        rim_protector = (c_data['BLK'] > 1) & (~playmaking_big)  # Only if not already playmaking
        glass_cleaner = ~(playmaking_big | rim_protector)  # Everyone else
        
        df.loc[c_mask & playmaking_big, 'Player_Type'] = 'Playmaking Big'
        df.loc[c_mask & rim_protector, 'Player_Type'] = 'Rim Protector'
        df.loc[c_mask & glass_cleaner, 'Player_Type'] = 'Glass Cleaner'
    
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
    """Create fantasy ranking based on fantasy points (primary) and other factors"""
    # Filter players with minimum games
    df_filtered = df[df['G'] >= min_games].copy()
    
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

