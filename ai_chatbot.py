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
        
        # League insights and analysis
        elif any(word in query_lower for word in ['league', 'average', 'insights', 'analysis', 'trends']):
            return self._handle_league_insights_query(query)
        
        # Draft strategy and team building
        elif any(word in query_lower for word in ['strategy', 'team building', 'roster', 'draft strategy']):
            return self._handle_draft_strategy_query(query)
        
        # Trade and value analysis
        elif any(word in query_lower for word in ['trade', 'value', 'worth', 'overvalued', 'undervalued']):
            return self._handle_trade_analysis_query(query)
        
        # Waiver wire and streaming
        elif any(word in query_lower for word in ['waiver', 'streaming', 'pickup', 'add', 'drop']):
            return self._handle_waiver_wire_query(query)
        
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
        
        # Advanced statistics queries
        elif 'game score' in query_lower:
            top_game_score = self.df.nlargest(5, 'Game_Score')
            response = "**Top 5 Game Score Leaders:**\n\n"
            for i, (_, player) in enumerate(top_game_score.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Game_Score']:.1f} Game Score\n"
            response += "\n💡 **Game Score** measures overall game impact using box score statistics."
            return response
        
        elif 'bpm' in query_lower or 'box plus minus' in query_lower:
            top_bpm = self.df.nlargest(5, 'BPM')
            response = "**Top 5 Box Plus Minus Leaders:**\n\n"
            for i, (_, player) in enumerate(top_bpm.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['BPM']:.1f} BPM\n"
            response += "\n💡 **BPM** measures player's contribution per 100 possessions relative to league average."
            return response
        
        elif 'efficiency' in query_lower:
            top_efficiency = self.df.nlargest(5, 'TS%')
            response = "**Top 5 Most Efficient Scorers (True Shooting %):**\n\n"
            for i, (_, player) in enumerate(top_efficiency.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['TS%']:.1f}% TS\n"
            response += "\n💡 **True Shooting %** accounts for 2-pointers, 3-pointers, and free throws."
            return response
        
        elif 'steals' in query_lower:
            top_steals = self.df.nlargest(5, 'STL')
            response = "**Top 5 Steal Leaders:**\n\n"
            for i, (_, player) in enumerate(top_steals.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['STL']:.1f} SPG\n"
            return response
        
        elif 'blocks' in query_lower:
            top_blocks = self.df.nlargest(5, 'BLK')
            response = "**Top 5 Block Leaders:**\n\n"
            for i, (_, player) in enumerate(top_blocks.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['BLK']:.1f} BPG\n"
            return response
        
        else:
            return "I can help you find top performers! Try asking about 'top fantasy players', 'top scorers', 'top rebounders', 'top assist leaders', 'game score leaders', 'BPM leaders', or 'most efficient scorers'."
    
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
        
        # Generate detailed comparison
        response = "**📊 Detailed Player Comparison:**\n\n"
        
        # Create comparison table
        response += "| Player | Team | Pos | Fantasy | PTS | REB | AST | STL | BLK | Type |\n"
        response += "|--------|------|-----|---------|-----|-----|-----|-----|-----|------|\n"
        
        for player in player_data:
            response += f"| {player['Player']} | {player['Team']} | {player['Pos']} | {player['Fantasy_Points']:.1f} | {player['PTS']:.1f} | {player['TRB']:.1f} | {player['AST']:.1f} | {player['STL']:.1f} | {player['BLK']:.1f} | {player['Player_Type']} |\n"
        
        response += "\n**🔍 Advanced Statistics:**\n\n"
        
        # Add advanced stats if available
        for player in player_data:
            response += f"**{player['Player']}:**\n"
            if 'AST_TOV_Ratio' in player:
                response += f"• AST/TOV Ratio: {player['AST_TOV_Ratio']:.2f}\n"
            if 'TS%' in player:
                response += f"• True Shooting %: {player['TS%']:.1f}%\n"
            if 'eFG%' in player:
                response += f"• Effective FG %: {player['eFG%']:.1f}%\n"
            response += "\n"
        
        # Determine winners by category
        response += "**🏆 Category Winners:**\n"
        categories = {
            'Fantasy Points': 'Fantasy_Points',
            'Scoring': 'PTS',
            'Rebounding': 'TRB',
            'Assists': 'AST',
            'Steals': 'STL',
            'Blocks': 'BLK'
        }
        
        for category, stat in categories.items():
            best_player = max(player_data, key=lambda x: x[stat])
            response += f"• **{category}:** {best_player['Player']} ({best_player[stat]:.1f})\n"
        
        # Overall fantasy winner
        best_fantasy = max(player_data, key=lambda x: x['Fantasy_Points'])
        response += f"\n🎯 **Overall Fantasy Winner:** {best_fantasy['Player']} with {best_fantasy['Fantasy_Points']:.1f} fantasy points!"
        
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
- "Game score leaders"
- "BPM leaders"
- "Most efficient scorers"
- "Top steals/blocks"

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

**📈 League Insights:**
- "League averages"
- "Position distribution"
- "Elite players analysis"
- "Best teams"

**🎯 Draft Strategy:**
- "Draft strategy"
- "Position scarcity"
- "Team building"

**💰 Trade Analysis:**
- "Overvalued players"
- "Undervalued players"
- "Trade value"

**📋 Waiver Wire:**
- "Waiver wire targets"
- "Streaming strategy"
- "Add/drop advice"

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
    
    def _handle_league_insights_query(self, query: str) -> str:
        """Handle league-wide insights and analysis queries"""
        query_lower = query.lower()
        
        # League averages
        if 'average' in query_lower or 'league average' in query_lower:
            avg_fantasy = self.df['Fantasy_Points'].mean()
            avg_points = self.df['PTS'].mean()
            avg_rebounds = self.df['TRB'].mean()
            avg_assists = self.df['AST'].mean()
            avg_steals = self.df['STL'].mean()
            avg_blocks = self.df['BLK'].mean()
            
            response = "**📊 2024 NBA League Averages:**\n\n"
            response += f"• **Fantasy Points:** {avg_fantasy:.1f} per game\n"
            response += f"• **Points:** {avg_points:.1f} PPG\n"
            response += f"• **Rebounds:** {avg_rebounds:.1f} RPG\n"
            response += f"• **Assists:** {avg_assists:.1f} APG\n"
            response += f"• **Steals:** {avg_steals:.1f} SPG\n"
            response += f"• **Blocks:** {avg_blocks:.1f} BPG\n\n"
            response += f"**Total Players Analyzed:** {len(self.df)}"
            return response
        
        # Position distribution
        elif 'position' in query_lower and 'distribution' in query_lower:
            pos_counts = self.df['Pos'].value_counts()
            response = "**🏀 Position Distribution in NBA:**\n\n"
            for pos, count in pos_counts.items():
                percentage = (count / len(self.df)) * 100
                response += f"• **{pos}:** {count} players ({percentage:.1f}%)\n"
            return response
        
        # Elite players analysis
        elif 'elite' in query_lower or 'superstars' in query_lower:
            elite_threshold = self.df['Fantasy_Points'].quantile(0.9)  # Top 10%
            elite_players = self.df[self.df['Fantasy_Points'] >= elite_threshold]
            
            response = f"**⭐ Elite Players Analysis (Top 10% - {elite_threshold:.1f}+ FP):**\n\n"
            response += f"**Total Elite Players:** {len(elite_players)}\n\n"
            
            # Position breakdown of elite players
            elite_pos = elite_players['Pos'].value_counts()
            response += "**Position Breakdown:**\n"
            for pos, count in elite_pos.items():
                response += f"• **{pos}:** {count} players\n"
            
            # Top 5 elite players
            top_elite = elite_players.nlargest(5, 'Fantasy_Points')
            response += "\n**Top 5 Elite Players:**\n"
            for i, (_, player) in enumerate(top_elite.iterrows(), 1):
                response += f"{i}. **{player['Player']}** - {player['Fantasy_Points']:.1f} FP\n"
            
            return response
        
        # Team analysis
        elif 'team' in query_lower and ('best' in query_lower or 'strongest' in query_lower):
            team_avg_fantasy = self.df.groupby('Team')['Fantasy_Points'].mean().sort_values(ascending=False)
            response = "**🏆 Teams Ranked by Average Fantasy Points:**\n\n"
            for i, (team, avg_fp) in enumerate(team_avg_fantasy.head(10).items(), 1):
                response += f"{i}. **{team}:** {avg_fp:.1f} avg FP\n"
            return response
        
        else:
            return "I can provide league insights! Try asking about 'league averages', 'position distribution', 'elite players', or 'best teams'."
    
    def _handle_draft_strategy_query(self, query: str) -> str:
        """Handle draft strategy and team building queries"""
        query_lower = query.lower()
        
        # Draft strategy
        if 'draft strategy' in query_lower or 'draft order' in query_lower:
            response = "**🎯 Fantasy Draft Strategy Guide:**\n\n"
            response += "**Round 1-2: Build Your Foundation**\n"
            response += "• Target elite fantasy players (35+ FP)\n"
            response += "• Prioritize players with high usage rates\n"
            response += "• Consider position scarcity\n\n"
            
            response += "**Round 3-5: Fill Key Positions**\n"
            response += "• Draft your starting lineup positions\n"
            response += "• Look for consistent performers (25-35 FP)\n"
            response += "• Balance scoring and defensive stats\n\n"
            
            response += "**Round 6-10: Depth and Value**\n"
            response += "• Target sleepers and undervalued players\n"
            response += "• Fill bench positions\n"
            response += "• Consider streaming options\n\n"
            
            response += "**Round 11+: High-Upside Picks**\n"
            response += "• Take calculated risks on young players\n"
            response += "• Handcuff your stars\n"
            response += "• Prepare for waiver wire moves"
            return response
        
        # Position scarcity
        elif 'position scarcity' in query_lower or 'scarcity' in query_lower:
            pos_avg_fantasy = self.df.groupby('Pos')['Fantasy_Points'].mean().sort_values(ascending=False)
            response = "**📊 Position Scarcity Analysis:**\n\n"
            response += "**Average Fantasy Points by Position:**\n"
            for pos, avg_fp in pos_avg_fantasy.items():
                response += f"• **{pos}:** {avg_fp:.1f} avg FP\n"
            
            response += "\n**💡 Draft Strategy:**\n"
            response += "• **Centers** are typically the scarcest position\n"
            response += "• **Point Guards** provide the most assists\n"
            response += "• **Forwards** offer the best balance of stats\n"
            response += "• Consider drafting elite players at scarce positions early"
            return response
        
        # Team building
        elif 'team building' in query_lower or 'roster construction' in query_lower:
            response = "**🏗️ Fantasy Team Building Guide:**\n\n"
            response += "**Ideal Roster Construction:**\n"
            response += "• **2 Point Guards** (assists, steals)\n"
            response += "• **2 Shooting Guards** (scoring, 3-pointers)\n"
            response += "• **2 Small Forwards** (versatile stats)\n"
            response += "• **2 Power Forwards** (rebounds, blocks)\n"
            response += "• **2 Centers** (rebounds, blocks, FG%)\n"
            response += "• **3 Utility/Bench** (flexibility)\n\n"
            
            response += "**Key Principles:**\n"
            response += "• Balance scoring and defensive categories\n"
            response += "• Don't punt categories early in the draft\n"
            response += "• Build depth for injury protection\n"
            response += "• Keep roster spots flexible for streaming"
            return response
        
        else:
            return "I can help with draft strategy! Try asking about 'draft strategy', 'position scarcity', or 'team building'."
    
    def _handle_trade_analysis_query(self, query: str) -> str:
        """Handle trade and value analysis queries"""
        query_lower = query.lower()
        
        # Overvalued players
        if 'overvalued' in query_lower:
            # Find players with high fantasy points but poor efficiency
            overvalued = self.df[
                (self.df['Fantasy_Points'] > 25) & 
                (self.df['TS%'] < 0.5) & 
                (self.df['TOV'] > 3)
            ].nlargest(5, 'Fantasy_Points')
            
            response = "**⚠️ Potentially Overvalued Players:**\n\n"
            response += "These players have good fantasy points but poor efficiency:\n\n"
            for i, (_, player) in enumerate(overvalued.iterrows(), 1):
                response += f"{i}. **{player['Player']}** - {player['Fantasy_Points']:.1f} FP, {player['TS%']:.1%} TS, {player['TOV']:.1f} TOV\n"
            response += "\n💡 **Consider trading these players** while their value is high."
            return response
        
        # Undervalued players
        elif 'undervalued' in query_lower:
            # Find players with good efficiency but lower fantasy points
            undervalued = self.df[
                (self.df['Fantasy_Points'] < 30) & 
                (self.df['TS%'] > 0.6) & 
                (self.df['AST_TOV_Ratio'] > 2)
            ].nlargest(5, 'TS%')
            
            response = "**💎 Undervalued Players (Buy Low):**\n\n"
            response += "These players have great efficiency but lower fantasy points:\n\n"
            for i, (_, player) in enumerate(undervalued.iterrows(), 1):
                response += f"{i}. **{player['Player']}** - {player['Fantasy_Points']:.1f} FP, {player['TS%']:.1%} TS, {player['AST_TOV_Ratio']:.1f} A/T\n"
            response += "\n💡 **Target these players** in trades for better value."
            return response
        
        # Trade value analysis
        elif 'trade value' in query_lower or 'worth' in query_lower:
            response = "**💰 Trade Value Analysis:**\n\n"
            response += "**High Trade Value Players:**\n"
            response += "• Elite fantasy producers (35+ FP)\n"
            response += "• Players at scarce positions (C, PG)\n"
            response += "• Consistent performers with low injury risk\n\n"
            
            response += "**Trade Value Factors:**\n"
            response += "• **Fantasy Points** - Primary value indicator\n"
            response += "• **Position Scarcity** - Centers and PGs are valuable\n"
            response += "• **Consistency** - Low variance in performance\n"
            response += "• **Injury Risk** - Games played and minutes\n"
            response += "• **Age** - Younger players have more upside"
            return response
        
        else:
            return "I can help with trade analysis! Try asking about 'overvalued players', 'undervalued players', or 'trade value'."
    
    def _handle_waiver_wire_query(self, query: str) -> str:
        """Handle waiver wire and streaming queries"""
        query_lower = query.lower()
        
        # Waiver wire targets
        if 'waiver wire' in query_lower or 'pickup' in query_lower:
            # Find players with decent fantasy points but lower recognition
            waiver_targets = self.df[
                (self.df['Fantasy_Points'] > 20) & 
                (self.df['Fantasy_Points'] < 30) &
                (self.df['G'] > 50)  # Played most games
            ].nlargest(10, 'Fantasy_Points')
            
            response = "**📋 Waiver Wire Targets:**\n\n"
            response += "Players with solid fantasy value who might be available:\n\n"
            for i, (_, player) in enumerate(waiver_targets.iterrows(), 1):
                response += f"{i}. **{player['Player']}** ({player['Team']}) - {player['Fantasy_Points']:.1f} FP\n"
            response += "\n💡 **Streaming Strategy:** Pick up players based on matchups and schedule."
            return response
        
        # Streaming options
        elif 'streaming' in query_lower:
            response = "**🔄 Streaming Strategy Guide:**\n\n"
            response += "**What is Streaming?**\n"
            response += "• Adding/dropping players based on schedule\n"
            response += "• Maximizing games played in a week\n"
            response += "• Targeting specific categories\n\n"
            
            response += "**Best Streaming Positions:**\n"
            response += "• **Point Guards** - High assist potential\n"
            response += "• **Centers** - Rebound and block specialists\n"
            response += "• **3-Point Specialists** - SG/SF with high 3P%\n\n"
            
            response += "**Streaming Tips:**\n"
            response += "• Check team schedules (back-to-backs)\n"
            response += "• Target players in fast-paced games\n"
            response += "• Consider opponent defensive rankings\n"
            response += "• Don't stream your core players"
            return response
        
        # Add/drop advice
        elif 'add' in query_lower or 'drop' in query_lower:
            response = "**➕➖ Add/Drop Advice:**\n\n"
            response += "**Players to ADD:**\n"
            response += "• High-usage players on good teams\n"
            response += "• Players returning from injury\n"
            response += "• Rookies with increasing minutes\n"
            response += "• Players in favorable matchups\n\n"
            
            response += "**Players to DROP:**\n"
            response += "• Injured players with no return timeline\n"
            response += "• Players losing minutes/role\n"
            response += "• Inefficient players with poor shooting\n"
            response += "• Players on tanking teams"
            return response
        
        else:
            return "I can help with waiver wire strategy! Try asking about 'waiver wire targets', 'streaming strategy', or 'add/drop advice'."
