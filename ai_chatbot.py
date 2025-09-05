"""
AI Chatbot module for NBA Fantasy Dashboard
Provides intelligent responses about players, stats, and fantasy recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import re

class NBAFantasyChatbot:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.context = {
            'current_player': None,
            'current_team': None,
            'current_position': None
        }
    
    def process_query(self, query: str) -> str:
        """Process user query and return appropriate response"""
        query_lower = query.lower().strip()
        
        # Player search queries
        if any(word in query_lower for word in ['who is', 'tell me about', 'show me', 'player']):
            return self._handle_player_query(query)
        
        # Statistical queries
        elif any(word in query_lower for word in ['top', 'best', 'highest', 'most', 'leader']):
            return self._handle_statistical_query(query)
        
        # Fantasy recommendation queries
        elif any(word in query_lower for word in ['pick', 'recommend', 'should i', 'fantasy', 'draft']):
            return self._handle_fantasy_query(query)
        
        # Comparison queries
        elif any(word in query_lower for word in ['compare', 'vs', 'versus', 'better']):
            return self._handle_comparison_query(query)
        
        # Team queries
        elif any(word in query_lower for word in ['team', 'roster', 'players on']):
            return self._handle_team_query(query)
        
        # Position queries
        elif any(word in query_lower for word in ['position', 'pg', 'sg', 'sf', 'pf', 'c', 'guard', 'forward', 'center']):
            return self._handle_position_query(query)
        
        # General help
        elif any(word in query_lower for word in ['help', 'what can', 'how to', 'explain']):
            return self._handle_help_query()
        
        else:
            return self._handle_general_query(query)
    
    def _handle_player_query(self, query: str) -> str:
        """Handle queries about specific players"""
        # Extract player name from query
        player_name = self._extract_player_name(query)
        
        if not player_name:
            return "I couldn't find a player name in your query. Try asking about a specific player like 'Tell me about LeBron James' or 'Who is Stephen Curry?'"
        
        # Find player in dataset (handle special characters and partial matches)
        # Try multiple matching strategies
        player_data = pd.DataFrame()
        
        # Strategy 1: Direct contains match
        player_data = self.df[self.df['Player'].str.contains(player_name, case=False, na=False, regex=False)]
        
        # Strategy 2: If no match, try partial matching with word parts
        if player_data.empty:
            search_parts = player_name.lower().split()
            for _, row in self.df.iterrows():
                player_name_lower = row['Player'].lower()
                if all(part in player_name_lower for part in search_parts):
                    player_data = self.df[self.df['Player'] == row['Player']]
                    break
        
        # Strategy 3: If still no match, try fuzzy matching for common names
        if player_data.empty:
            # Handle common name variations
            name_variations = {
                'jokic': 'jokić',
                'doncic': 'dončić',
                'lebron': 'lebron james',
                'curry': 'stephen curry',
                'durant': 'kevin durant',
                'giannis': 'antetokounmpo',
                'luka': 'dončić',
                'nikola': 'jokić'
            }
            
            for variation, full_name in name_variations.items():
                if variation in player_name.lower():
                    player_data = self.df[self.df['Player'].str.contains(full_name, case=False, na=False, regex=False)]
                    if not player_data.empty:
                        break
        
        if player_data.empty:
            return f"I couldn't find a player named '{player_name}' in the 2024 NBA season data. Please check the spelling and try again."
        
        player = player_data.iloc[0]
        self.context['current_player'] = player['Player']
        
        # Generate player summary
        response = f"**{player['Player']}** ({player['Team']}) - {player['Pos']}\n\n"
        response += f"**Key Stats:**\n"
        response += f"• Points: {player['PTS']:.1f} PPG\n"
        response += f"• Rebounds: {player['TRB']:.1f} RPG\n"
        response += f"• Assists: {player['AST']:.1f} APG\n"
        response += f"• Fantasy Points: {player['Fantasy_Points']:.1f}\n"
        response += f"• Player Type: {player['Player_Type']}\n"
        
        if player.get('Tags'):
            response += f"• Tags: {player['Tags']}\n"
        
        # Add insights
        if player['Fantasy_Points'] > 40:
            response += f"\n🔥 **Fantasy Impact:** Elite fantasy player with {player['Fantasy_Points']:.1f} fantasy points per game!"
        elif player['Fantasy_Points'] > 30:
            response += f"\n⭐ **Fantasy Impact:** Strong fantasy contributor with {player['Fantasy_Points']:.1f} fantasy points per game."
        else:
            response += f"\n📊 **Fantasy Impact:** Solid role player with {player['Fantasy_Points']:.1f} fantasy points per game."
        
        return response
    
    def _handle_statistical_query(self, query: str) -> str:
        """Handle queries about top performers and statistics"""
        query_lower = query.lower()
        
        # Top fantasy players
        if 'fantasy' in query_lower:
            top_players = self.df.nlargest(5, 'Fantasy_Points')
            response = "**Top 5 Fantasy Players:**\n\n"
            for i, (_, player) in enumerate(top_players.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
            return response
        
        # Top scorers
        elif 'point' in query_lower or 'score' in query_lower:
            top_scorers = self.df.nlargest(5, 'PTS')
            response = "**Top 5 Scorers:**\n\n"
            for i, (_, player) in enumerate(top_scorers.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['PTS']:.1f} PPG\n"
            return response
        
        # Top rebounders
        elif 'rebound' in query_lower:
            top_rebounders = self.df.nlargest(5, 'TRB')
            response = "**Top 5 Rebounders:**\n\n"
            for i, (_, player) in enumerate(top_rebounders.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['TRB']:.1f} RPG\n"
            return response
        
        # Top assist leaders
        elif 'assist' in query_lower:
            top_assists = self.df.nlargest(5, 'AST')
            response = "**Top 5 Assist Leaders:**\n\n"
            for i, (_, player) in enumerate(top_assists.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['AST']:.1f} APG\n"
            return response
        
        else:
            return "I can help you find top performers! Try asking about 'top fantasy players', 'top scorers', 'top rebounders', or 'top assist leaders'."
    
    def _handle_fantasy_query(self, query: str) -> str:
        """Handle fantasy-related queries and recommendations"""
        query_lower = query.lower()
        
        # Draft recommendations
        if any(word in query_lower for word in ['draft', 'pick', 'first round']):
            top_picks = self.df.nlargest(10, 'Fantasy_Points')
            response = "**Top 10 Draft Picks for Fantasy:**\n\n"
            for i, (_, player) in enumerate(top_picks.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
            response += "\n💡 **Tip:** These players provide the most consistent fantasy value!"
            return response
        
        # Sleepers/undervalued players
        elif 'sleeper' in query_lower or 'undervalued' in query_lower:
            # Find players with good fantasy points but lower recognition
            sleepers = self.df[
                (self.df['Fantasy_Points'] > 25) & 
                (self.df['Fantasy_Points'] < 35)
            ].nlargest(5, 'Fantasy_Points')
            
            response = "**Fantasy Sleepers (Undervalued Players):**\n\n"
            for i, (_, player) in enumerate(sleepers.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
            response += "\n💡 **Tip:** These players offer great value in later rounds!"
            return response
        
        # Position-specific recommendations
        elif any(pos in query_lower for pos in ['point guard', 'pg', 'guard']):
            pg_players = self.df[self.df['Pos'] == 'PG'].nlargest(5, 'Fantasy_Points')
            response = "**Top Point Guards for Fantasy:**\n\n"
            for i, (_, player) in enumerate(pg_players.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
            return response
        
        else:
            return "I can help with fantasy recommendations! Try asking about 'draft picks', 'sleepers', or position-specific players like 'point guards'."
    
    def _handle_comparison_query(self, query: str) -> str:
        """Handle player comparison queries"""
        # Extract player names
        players = self._extract_multiple_player_names(query)
        
        if len(players) < 2:
            return "I need at least two player names to make a comparison. Try asking 'Compare LeBron James vs Stephen Curry' or 'Who is better: Luka Doncic or Nikola Jokic?'"
        
        # Find players in dataset
        player_data = []
        for player_name in players:
            found_player = self.df[self.df['Player'].str.contains(player_name, case=False, na=False)]
            if not found_player.empty:
                player_data.append(found_player.iloc[0])
        
        if len(player_data) < 2:
            return "I couldn't find enough players for comparison. Please check the spelling of the player names."
        
        # Generate comparison
        response = "**Player Comparison:**\n\n"
        for player in player_data:
            response += f"**{player['Player']}** ({player['Team']}):\n"
            response += f"• Fantasy Points: {player['Fantasy_Points']:.1f}\n"
            response += f"• Points: {player['PTS']:.1f} | Rebounds: {player['TRB']:.1f} | Assists: {player['AST']:.1f}\n"
            response += f"• Player Type: {player['Player_Type']}\n\n"
        
        # Determine winner
        best_player = max(player_data, key=lambda x: x['Fantasy_Points'])
        response += f"🏆 **Fantasy Winner:** {best_player['Player']} with {best_player['Fantasy_Points']:.1f} fantasy points!"
        
        return response
    
    def _handle_team_query(self, query: str) -> str:
        """Handle team-related queries"""
        # Extract team name
        team_name = self._extract_team_name(query)
        
        if not team_name:
            return "I couldn't identify a team name. Try asking 'Show me Lakers players' or 'Who plays for the Warriors?'"
        
        # Find team players
        team_players = self.df[self.df['Team'].str.contains(team_name, case=False, na=False)]
        
        if team_players.empty:
            return f"I couldn't find players for the {team_name}. Please check the team name and try again."
        
        # Show top players from team
        top_team_players = team_players.nlargest(5, 'Fantasy_Points')
        response = f"**Top {team_name} Players:**\n\n"
        for i, (_, player) in enumerate(top_team_players.iterrows(), 1):
            response += f"{i}. **{player['Player']}** ({player['Pos']}) - {player['Fantasy_Points']:.1f} FP\n"
        
        return response
    
    def _handle_position_query(self, query: str) -> str:
        """Handle position-specific queries"""
        query_lower = query.lower()
        
        # Determine position
        if any(word in query_lower for word in ['point guard', 'pg']):
            position = 'PG'
            pos_name = 'Point Guards'
        elif any(word in query_lower for word in ['shooting guard', 'sg']):
            position = 'SG'
            pos_name = 'Shooting Guards'
        elif any(word in query_lower for word in ['small forward', 'sf']):
            position = 'SF'
            pos_name = 'Small Forwards'
        elif any(word in query_lower for word in ['power forward', 'pf']):
            position = 'PF'
            pos_name = 'Power Forwards'
        elif any(word in query_lower for word in ['center', 'c']):
            position = 'C'
            pos_name = 'Centers'
        else:
            return "I can help with position-specific queries! Try asking about 'point guards', 'centers', 'forwards', etc."
        
        # Get top players at position
        pos_players = self.df[self.df['Pos'] == position].nlargest(5, 'Fantasy_Points')
        response = f"**Top {pos_name}:**\n\n"
        for i, (_, player) in enumerate(pos_players.iterrows(), 1):
            response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
        
        return response
    
    def _handle_help_query(self) -> str:
        """Handle help queries"""
        return """
**🤖 NBA Fantasy AI Assistant Help**

I can help you with:

**🔍 Player Information:**
- "Tell me about LeBron James"
- "Who is Stephen Curry?"
- "Show me Nikola Jokic stats"

**📊 Statistical Queries:**
- "Top fantasy players"
- "Best scorers"
- "Top rebounders"
- "Assist leaders"

**🎯 Fantasy Recommendations:**
- "Draft picks"
- "Fantasy sleepers"
- "Best point guards"
- "Who should I pick?"

**⚖️ Player Comparisons:**
- "Compare LeBron vs Curry"
- "Luka vs Jokic who is better?"

**🏀 Team Information:**
- "Lakers players"
- "Show me Warriors roster"

**📍 Position Analysis:**
- "Best centers"
- "Top point guards"
- "Power forwards"

Just ask me anything about NBA players and fantasy basketball! 🏀
        """
    
    def _handle_general_query(self, query: str) -> str:
        """Handle general queries"""
        return f"I'm not sure how to help with '{query}'. Try asking about specific players, stats, or fantasy recommendations. Type 'help' to see what I can do!"
    
    def _extract_player_name(self, query: str) -> Optional[str]:
        """Extract player name from query"""
        # Common patterns for player queries
        patterns = [
            r'tell me about (.+)',
            r'who is (.+)',
            r'show me (.+)',
            r'player (.+)',
            r'(.+) stats',
            r'(.+) information'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                name = match.group(1).strip()
                # Clean up common suffixes
                name = re.sub(r'\s+(stats?|information|data)$', '', name)
                return name
        
        # If no pattern matches, try to find a player name in the query
        # Look for common player name patterns
        words = query.split()
        for i, word in enumerate(words):
            # Check if this word or combination of words matches a player
            for j in range(i, min(i + 3, len(words))):
                potential_name = ' '.join(words[i:j+1])
                if len(potential_name) > 2:  # At least 3 characters
                    # Check if this matches any player name
                    matches = self.df[self.df['Player'].str.contains(potential_name, case=False, na=False, regex=False)]
                    if not matches.empty:
                        return potential_name
        
        return None
    
    def _extract_multiple_player_names(self, query: str) -> List[str]:
        """Extract multiple player names from comparison queries"""
        # Look for vs, versus, compare patterns
        if ' vs ' in query.lower():
            parts = query.lower().split(' vs ')
            return [part.strip() for part in parts if part.strip()]
        elif ' versus ' in query.lower():
            parts = query.lower().split(' versus ')
            return [part.strip() for part in parts if part.strip()]
        elif 'compare' in query.lower():
            # Extract names after "compare"
            match = re.search(r'compare (.+)', query.lower())
            if match:
                names_text = match.group(1)
                # Split by common separators
                names = re.split(r'[,\s]+(?:and|&|\+)\s*', names_text)
                return [name.strip() for name in names if name.strip()]
        
        return []
    
    def _extract_team_name(self, query: str) -> Optional[str]:
        """Extract team name from query"""
        # Common team patterns
        patterns = [
            r'(.+) players',
            r'players on (.+)',
            r'(.+) roster',
            r'who plays for (.+)',
            r'show me (.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1).strip()
        
        return None
