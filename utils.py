"""
Utility functions for NBA Fantasy Dashboard
Helper functions and calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

def calculate_fantasy_points(row: pd.Series) -> float:
    """Calculate fantasy points for a single player"""
    return (
        row['PTS'] * 1 +           # Points
        row['TRB'] * 1.2 +         # Rebounds
        row['AST'] * 1.5 +         # Assists
        row['STL'] * 2 +           # Steals
        row['BLK'] * 2 +           # Blocks
        row['TOV'] * -1            # Turnovers (negative)
    )

def calculate_per(row: pd.Series) -> float:
    """Calculate Player Efficiency Rating"""
    return row['PTS'] + row['TRB'] + row['AST'] + row['STL'] + row['BLK'] - row['TOV']

def calculate_usage_rate(row: pd.Series) -> float:
    """Calculate usage rate"""
    if row['MP'] == 0:
        return 0
    return (row['FGA'] + row['FTA'] * 0.44 + row['AST']) / row['MP'] * 100

def calculate_weighted_fantasy_score(row: pd.Series) -> float:
    """Calculate weighted fantasy score considering multiple factors"""
    shooting_avg = (row['FG%'] + row['3P%'] + row['FT%']) / 3
    return (
        row['Fantasy_Points'] * 0.4 +
        row['PER'] * 0.3 +
        row['Usage_Rate'] * 0.2 +
        shooting_avg * 0.1
    )

def get_player_summary(player_data: pd.Series) -> Dict:
    """Get summary statistics for a player"""
    return {
        'name': player_data['Player'],
        'team': player_data['Team'],
        'position': player_data['Pos'],
        'age': player_data['Age'],
        'games': player_data['G'],
        'fantasy_points': player_data['Fantasy_Points'],
        'points': player_data['PTS'],
        'rebounds': player_data['TRB'],
        'assists': player_data['AST'],
        'steals': player_data['STL'],
        'blocks': player_data['BLK'],
        'fg_percentage': player_data['FG%'],
        'three_p_percentage': player_data['3P%'],
        'ft_percentage': player_data['FT%'],
        'player_type': player_data['Player_Type'],
        'minutes': player_data['MP']
    }

def format_percentage(value: float) -> str:
    """Format percentage values"""
    return f"{value:.1%}"

def format_stat(value: float, decimals: int = 1) -> str:
    """Format statistical values"""
    return f"{value:.{decimals}f}"

def get_filter_options(df: pd.DataFrame) -> Dict[str, List]:
    """Get available filter options from the dataset"""
    return {
        'positions': ['All'] + sorted(df['Pos'].unique().tolist()),
        'teams': ['All'] + sorted(df['Team'].unique().tolist()),
        'age_range': (int(df['Age'].min()), int(df['Age'].max())),
        'games_range': (1, int(df['G'].max()))
    }

def validate_filters(position: str, team: str, age_range: Tuple[int, int], min_games: int) -> bool:
    """Validate filter inputs"""
    if not isinstance(age_range, tuple) or len(age_range) != 2:
        return False
    if age_range[0] > age_range[1]:
        return False
    if min_games < 0:
        return False
    return True

def get_top_performers(df: pd.DataFrame, metric: str, top_n: int = 10) -> pd.DataFrame:
    """Get top performers for a specific metric"""
    return df.nlargest(top_n, metric)

def get_bottom_performers(df: pd.DataFrame, metric: str, bottom_n: int = 10) -> pd.DataFrame:
    """Get bottom performers for a specific metric"""
    return df.nsmallest(bottom_n, metric)

def calculate_team_efficiency(team_data: pd.DataFrame) -> Dict:
    """Calculate team efficiency metrics"""
    return {
        'avg_fantasy_points': team_data['Fantasy_Points'].mean(),
        'total_fantasy_points': team_data['Fantasy_Points'].sum(),
        'player_count': len(team_data),
        'avg_age': team_data['Age'].mean(),
        'avg_games': team_data['G'].mean()
    }

def get_position_rankings(df: pd.DataFrame, position: str) -> pd.DataFrame:
    """Get rankings for players in a specific position"""
    position_players = df[df['Pos'] == position].copy()
    position_players = position_players.sort_values('Fantasy_Points', ascending=False)
    position_players['Position_Rank'] = range(1, len(position_players) + 1)
    return position_players

def calculate_consistency_score(player_data: pd.Series) -> float:
    """Calculate consistency score based on shooting percentages"""
    shooting_stats = [player_data['FG%'], player_data['3P%'], player_data['FT%']]
    # Higher consistency = less variance in shooting percentages
    consistency = 1 - np.std(shooting_stats)
    return max(0, consistency)  # Ensure non-negative

def get_player_archetype(player_data: pd.Series) -> str:
    """Determine player archetype based on stats"""
    if player_data['AST'] > 7:
        return "Playmaker"
    elif player_data['TRB'] > 10:
        return "Rebounder"
    elif player_data['PTS'] > 25:
        return "Scorer"
    elif player_data['STL'] + player_data['BLK'] > 3:
        return "Defender"
    else:
        return "Role Player"

def format_player_display_name(player_data: pd.Series) -> str:
    """Format player name for display"""
    return f"{player_data['Player']} ({player_data['Team']}) - {player_data['Pos']}"

def get_stat_categories() -> Dict[str, List[str]]:
    """Get predefined stat categories"""
    return {
        'scoring': ['PTS', 'FG%', '3P%', 'FT%'],
        'rebounding': ['TRB', 'ORB', 'DRB'],
        'playmaking': ['AST', 'TOV'],
        'defense': ['STL', 'BLK'],
        'efficiency': ['eFG%', 'PER', 'Usage_Rate'],
        'advanced': ['Fantasy_Points', 'Weighted_Fantasy_Score']
    }

def calculate_league_averages(df: pd.DataFrame) -> Dict:
    """Calculate league-wide averages"""
    return {
        'avg_fantasy_points': df['Fantasy_Points'].mean(),
        'avg_points': df['PTS'].mean(),
        'avg_rebounds': df['TRB'].mean(),
        'avg_assists': df['AST'].mean(),
        'avg_steals': df['STL'].mean(),
        'avg_blocks': df['BLK'].mean(),
        'avg_fg_percentage': df['FG%'].mean(),
        'avg_three_p_percentage': df['3P%'].mean(),
        'avg_ft_percentage': df['FT%'].mean()
    }

def get_percentile_rank(value: float, data: pd.Series) -> float:
    """Calculate percentile rank of a value in a dataset"""
    return (data < value).mean() * 100

def create_player_rating(player_data: pd.Series, league_averages: Dict) -> Dict:
    """Create overall player rating based on league averages"""
    ratings = {}
    
    for stat, avg in league_averages.items():
        if stat in player_data.index:
            percentile = get_percentile_rank(player_data[stat], pd.Series([avg]))
            ratings[stat] = {
                'value': player_data[stat],
                'league_avg': avg,
                'percentile': percentile
            }
    
    return ratings
