import json
import os
from datetime import datetime
from typing import Dict, List, Any

class GameStats:
    """
    GameStats class for tracking and persisting game statistics.
    
    This class handles recording game sessions, calculating performance
    metrics, maintaining high scores, and saving data to JSON files.
    """
    
    def __init__(self, stats_file: str = "data/game_stats.json", 
                 high_scores_file: str = "data/high_scores.json"):
        """
        Initialize GameStats object.
        
        Args:
            stats_file (str): Path to game statistics file
            high_scores_file (str): Path to high scores file
        """
        self.stats_file = stats_file
        self.high_scores_file = high_scores_file
        
        # Current game session data
        self.current_session = {
            'start_time': None,
            'end_time': None,
            'score': 0,
            'max_length': 0,
            'duration_seconds': 0,
            'total_moves': 0,
            'direction_changes': 0,
            'foods_eaten': 0
        }
        
        # Ensure data directory exists
        self._ensure_data_directory()
        
        # Load existing data
        self.game_history = self._load_game_history()
        self.high_scores = self._load_high_scores()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        data_dir = os.path.dirname(self.stats_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_game_history(self) -> List[Dict[str, Any]]:
        """Load game history from file."""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []
    
    def _load_high_scores(self) -> List[Dict[str, Any]]:
        """Load high scores from file."""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []
    
    def start_new_game(self) -> None:
        """Start tracking a new game session."""
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'score': 0,
            'max_length': 1,  # Snake starts with length 1
            'duration_seconds': 0,
            'total_moves': 0,
            'direction_changes': 0,
            'foods_eaten': 0
        }
    
    def update_game_stats(self, snake_data: dict, food_data: dict, score: int) -> None:
        """
        Update current game statistics.
        
        Args:
            snake_data (dict): Snake analytics data
            food_data (dict): Food statistics data  
            score (int): Current game score
        """
        self.current_session.update({
            'score': score,
            'max_length': max(self.current_session['max_length'], snake_data['length']),
            'total_moves': snake_data['total_moves'],
            'direction_changes': snake_data['direction_changes'],
            'foods_eaten': food_data['foods_eaten']
        })
    
    def end_game(self) -> None:
        """End current game session and save statistics."""
        if self.current_session['start_time']:
            # Calculate game duration
            start_time = datetime.fromisoformat(self.current_session['start_time'])
            end_time = datetime.now()
            self.current_session['end_time'] = end_time.isoformat()
            self.current_session['duration_seconds'] = (end_time - start_time).total_seconds()
            
            # Add to game history
            self.game_history.append(self.current_session.copy())
            
            # Update high scores
            self._update_high_scores()
            
            # Save data
            self._save_data()
    
    def _update_high_scores(self) -> None:
        """Update high scores list with current game."""
        high_score_entry = {
            'score': self.current_session['score'],
            'max_length': self.current_session['max_length'],
            'duration_seconds': self.current_session['duration_seconds'],
            'foods_eaten': self.current_session['foods_eaten'],
            'date': self.current_session['start_time'],
            'efficiency': self.current_session['max_length'] / max(self.current_session['total_moves'], 1)
        }
        
        self.high_scores.append(high_score_entry)
        
        # Sort by score (descending) and keep top 10
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]
    
    def _save_data(self) -> None:
        """Save game statistics to files."""
        try:
            # Save game history (keep last 1000 games)
            with open(self.stats_file, 'w') as f:
                json.dump(self.game_history[-1000:], f, indent=2)
            
            # Save high scores
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except IOError as e:
            print(f"Error saving game data: {e}")
    
    def get_current_stats(self) -> dict:
        """Get current game session statistics."""
        return self.current_session.copy()
    
    def get_high_scores(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top high scores.
        
        Args:
            limit (int): Maximum number of scores to return
            
        Returns:
            List[Dict[str, Any]]: List of high score entries
        """
        return self.high_scores[:limit]
    
    def get_game_summary(self) -> dict:
        """
        Get overall game statistics summary.
        
        Returns:
            dict: Summary statistics across all games
        """
        if not self.game_history:
            return {
                'total_games': 0,
                'total_playtime': 0,
                'average_score': 0,
                'best_score': 0,
                'total_foods_eaten': 0
            }
        
        total_games = len(self.game_history)
        total_playtime = sum(game.get('duration_seconds', 0) for game in self.game_history)
        total_score = sum(game.get('score', 0) for game in self.game_history)
        best_score = max(game.get('score', 0) for game in self.game_history)
        total_foods = sum(game.get('foods_eaten', 0) for game in self.game_history)
        
        return {
            'total_games': total_games,
            'total_playtime': round(total_playtime, 2),
            'average_score': round(total_score / total_games, 2),
            'best_score': best_score,
            'total_foods_eaten': total_foods,
            'average_game_duration': round(total_playtime / total_games, 2)
        }