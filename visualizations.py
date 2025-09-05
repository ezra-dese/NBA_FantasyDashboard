"""
Visualization module for NBA Fantasy Dashboard
Handles all chart and plot creation using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_fantasy_distribution_chart(df):
    """Create fantasy points distribution histogram"""
    fig = px.histogram(df, x='Fantasy_Points', 
                      title="Fantasy Points Distribution",
                      nbins=30, color_discrete_sequence=['#1f77b4'])
    fig.update_layout(showlegend=False)
    return fig

def create_top_players_chart(df, top_n=10):
    """Create top players bar chart"""
    top_players = df.nlargest(top_n, 'Fantasy_Points')
    fig = px.bar(top_players, x='Fantasy_Points', y='Player',
                title=f"Top {top_n} Fantasy Players",
                orientation='h', color='Fantasy_Points',
                color_continuous_scale='Blues')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

def create_player_type_pie_chart(df):
    """Create player type distribution pie chart"""
    player_type_counts = df['Player_Type'].value_counts()
    fig = px.pie(values=player_type_counts.values, 
                names=player_type_counts.index,
                title="Player Type Distribution")
    return fig

def create_fantasy_vs_efficiency_scatter(df, top_n=50):
    """Create fantasy points vs efficiency scatter plot"""
    top_players = df.head(top_n)
    fig = px.scatter(top_players, 
                    x='Fantasy_Points', 
                    y='PER',
                    size='Usage_Rate',
                    color='Player_Type',
                    hover_data=['Player', 'Team', 'Pos'],
                    title=f"Fantasy Points vs Efficiency (Top {top_n} Players)")
    return fig

def create_player_radar_chart(player_data, player_name, df):
    """Create performance radar chart for individual player"""
    categories = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%']
    values = [player_data[cat] for cat in categories]
    
    # Normalize values for radar chart
    max_values = df[categories].max()
    normalized_values = [val / max_val * 100 for val, max_val in zip(values, max_values)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=categories,
        fill='toself',
        name=player_name,
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"{player_name} Performance Radar"
    )
    
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for statistical analysis"""
    numeric_cols = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%', 'Fantasy_Points']
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(corr_matrix, 
                   text_auto=True, 
                   aspect="auto",
                   title="Statistical Correlations",
                   color_continuous_scale='RdBu')
    return fig

def create_position_analysis_chart(position_stats):
    """Create position-based analysis bar chart"""
    fig = px.bar(position_stats, 
                title="Average Stats by Position",
                barmode='group')
    return fig

def create_team_analysis_chart(team_stats, chart_type='avg', top_n=15):
    """Create team analysis charts"""
    if chart_type == 'avg':
        data = team_stats.head(top_n)
        fig = px.bar(data, 
                    y=data.index,
                    x='Avg_Fantasy_Points',
                    title=f"Average Fantasy Points by Team (Top {top_n})",
                    orientation='h')
    elif chart_type == 'scatter':
        fig = px.scatter(team_stats, 
                        x='Player_Count', 
                        y='Avg_Fantasy_Points',
                        size='Total_Fantasy_Points',
                        hover_name=team_stats.index,
                        title="Team Size vs Average Fantasy Points")
    
    return fig

def create_metric_cards_data(df):
    """Prepare data for metric cards display"""
    metrics = {
        'total_players': len(df),
        'avg_fantasy': df['Fantasy_Points'].mean(),
        'top_scorer': df.loc[df['PTS'].idxmax(), 'Player'],
        'most_efficient': df.loc[df['PER'].idxmax(), 'Player']
    }
    return metrics

def create_player_comparison_chart(players_data):
    """Create comparison chart for multiple players"""
    if len(players_data) < 2:
        return None
    
    categories = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%']
    
    fig = go.Figure()
    
    for player_name, player_data in players_data.items():
        values = [player_data[cat] for cat in categories]
        max_values = [max([p[cat] for p in players_data.values()]) for cat in categories]
        normalized_values = [val / max_val * 100 for val, max_val in zip(values, max_values)]
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=categories,
            fill='toself',
            name=player_name
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Player Comparison"
    )
    
    return fig

def create_trend_analysis_chart(df, metric='Fantasy_Points', group_by='Pos'):
    """Create trend analysis chart"""
    if group_by == 'Pos':
        trend_data = df.groupby('Pos')[metric].mean().reset_index()
        fig = px.bar(trend_data, x='Pos', y=metric, title=f"Average {metric} by Position")
    elif group_by == 'Age':
        # Create age groups
        df['Age_Group'] = pd.cut(df['Age'], bins=[0, 22, 25, 28, 31, 100], 
                                labels=['21-22', '23-25', '26-28', '29-31', '32+'])
        trend_data = df.groupby('Age_Group')[metric].mean().reset_index()
        fig = px.bar(trend_data, x='Age_Group', y=metric, title=f"Average {metric} by Age Group")
    
    return fig
