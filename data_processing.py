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

def load_bpm_coefficients():
    """Load Box Plus Minus coefficients from the interpolation table"""
    try:
        bpm_df = pd.read_excel('Interpolation table values.xlsx')
        
        # Create a dictionary mapping position to coefficients
        bpm_coefficients = {}
        
        for _, row in bpm_df.iterrows():
            position = row['Position']
            # Extract position number and convert to standard position names
            if 'PG' in position:
                pos_key = 'PG'
            elif 'SG' in position:
                pos_key = 'SG'
            elif 'SF' in position:
                pos_key = 'SF'
            elif 'PF' in position:
                pos_key = 'PF'
            elif 'C' in position:
                pos_key = 'C'
            else:
                continue
                
            bpm_coefficients[pos_key] = {
                'PTS': row['PTS'],
                '3P': row['3P'],
                'AST': row['AST'],
                'TOV': row['TOV'],
                'ORB': row['ORB'],
                'DRB': row['DRB'],
                'STL': row['STL'],
                'BLK': row['BLK'],
                'PF': row['PF'],
                'FGA': row['FGA'],
                'FTA': row['FTA']
            }
        
        return bpm_coefficients
    except Exception as e:
        print(f"Error loading BPM coefficients: {e}")
        # Return default coefficients if file can't be loaded
        return {
            'PG': {'PTS': 0.86, '3P': 0.389, 'AST': 0.580, 'TOV': -0.964, 'ORB': 0.613, 'DRB': 0.116, 'STL': 1.369, 'BLK': 1.327, 'PF': -0.367, 'FGA': -0.560, 'FTA': -0.246},
            'SG': {'PTS': 0.86, '3P': 0.389, 'AST': 0.694, 'TOV': -0.964, 'ORB': 0.505, 'DRB': 0.132, 'STL': 1.279, 'BLK': 1.171, 'PF': -0.367, 'FGA': -0.615, 'FTA': -0.270},
            'SF': {'PTS': 0.86, '3P': 0.389, 'AST': 0.807, 'TOV': -0.964, 'ORB': 0.397, 'DRB': 0.149, 'STL': 1.189, 'BLK': 1.015, 'PF': -0.367, 'FGA': -0.670, 'FTA': -0.295},
            'PF': {'PTS': 0.86, '3P': 0.389, 'AST': 0.921, 'TOV': -0.964, 'ORB': 0.289, 'DRB': 0.165, 'STL': 1.098, 'BLK': 0.859, 'PF': -0.367, 'FGA': -0.725, 'FTA': -0.319},
            'C': {'PTS': 0.86, '3P': 0.389, 'AST': 1.034, 'TOV': -0.964, 'ORB': 0.181, 'DRB': 0.181, 'STL': 1.008, 'BLK': 0.703, 'PF': -0.367, 'FGA': -0.780, 'FTA': -0.343}
        }

def calculate_box_plus_minus(df, bpm_coefficients):
    """Calculate Box Plus Minus for each player based on their position"""
    bpm_values = []
    
    for _, player in df.iterrows():
        position = player['Pos']
        
        # Get coefficients for the player's position
        if position in bpm_coefficients:
            coeffs = bpm_coefficients[position]
        else:
            # Default to PG coefficients if position not found
            coeffs = bpm_coefficients['PG']
        
        # Calculate BPM using the formula: sum of (stat * coefficient)
        bpm = (
            player['PTS'] * coeffs['PTS'] +
            player['3P'] * coeffs['3P'] +
            player['AST'] * coeffs['AST'] +
            player['TOV'] * coeffs['TOV'] +
            player['ORB'] * coeffs['ORB'] +
            player['DRB'] * coeffs['DRB'] +
            player['STL'] * coeffs['STL'] +
            player['BLK'] * coeffs['BLK'] +
            player['PF'] * coeffs['PF'] +
            player['FGA'] * coeffs['FGA'] +
            player['FTA'] * coeffs['FTA']
        )
        
        bpm_values.append(bpm)
    
    return np.array(bpm_values)

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
        
        # Game Score per game = PTS + 0.4*FG – 0.7*FGA – 0.4*(FTA – FT) + 0.7*ORB + 0.3*DRB + STL + 0.7*AST + 0.7*BLK – 0.4*PF – TOV
        df['Game_Score'] = (
            df['PTS'] + 
            0.4 * df['FG'] - 
            0.7 * df['FGA'] - 
            0.4 * (df['FTA'] - df['FT']) + 
            0.7 * df['ORB'] + 
            0.3 * df['DRB'] + 
            df['STL'] + 
            0.7 * df['AST'] + 
            0.7 * df['BLK'] - 
            0.4 * df['PF'] - 
            df['TOV']
        )
        
        # Load Box Plus Minus coefficients
        bpm_coefficients = load_bpm_coefficients()
        
        # Calculate Box Plus Minus for each player based on their position
        df['BPM'] = calculate_box_plus_minus(df, bpm_coefficients)
        
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

