import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import numpy as np

class GameDataVisualizer:
    """
    Data visualization class for Snake game analytics.
    
    This class creates various charts and graphs to analyze
    gameplay patterns, performance trends, and statistics.
    """
    
    def __init__(self, stats_file: str = "data/game_stats.json",
                 high_scores_file: str = "data/high_scores.json"):
        """
        Initialize the data visualizer.
        
        Args:
            stats_file (str): Path to game statistics file
            high_scores_file (str): Path to high scores file
        """
        self.stats_file = stats_file
        self.high_scores_file = high_scores_file
        
        # Set matplotlib style
        plt.style.use('dark_background')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def load_data(self) -> tuple:
        """
        Load game data from JSON files.
        
        Returns:
            tuple: (game_history_df, high_scores_df)
        """
        game_history = []
        high_scores = []
        
        # Load game history
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    game_history = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Load high scores
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    high_scores = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Convert to DataFrames
        game_df = pd.DataFrame(game_history) if game_history else pd.DataFrame()
        scores_df = pd.DataFrame(high_scores) if high_scores else pd.DataFrame()
        
        # Process datetime columns
        if not game_df.empty and 'start_time' in game_df.columns:
            game_df['start_time'] = pd.to_datetime(game_df['start_time'])
            game_df['date'] = game_df['start_time'].dt.date
        
        if not scores_df.empty and 'date' in scores_df.columns:
            scores_df['date'] = pd.to_datetime(scores_df['date'])
        
        return game_df, scores_df
    
    def create_performance_dashboard(self, output_file: str = "performance_dashboard.png") -> None:
        """
        Create a comprehensive performance dashboard.
        
        Args:
            output_file (str): Output filename for the dashboard
        """
        game_df, scores_df = self.load_data()
        
        if game_df.empty:
            print("No game data available for visualization.")
            return
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🐍 Snake Game Performance Dashboard', fontsize=20, y=0.98)
        
        # 1. Score progression over time
        if len(game_df) > 1:
            ax1.plot(range(len(game_df)), game_df['score'], 
                    color='#00FF00', marker='o', markersize=3, linewidth=2)
            ax1.set_title('Score Progression Over Games', fontsize=14, pad=15)
            ax1.set_xlabel('Game Number')
            ax1.set_ylabel('Score')
            ax1.grid(True, alpha=0.3)
            
            # Add trend line
            z = np.polyfit(range(len(game_df)), game_df['score'], 1)
            p = np.poly1d(z)
            ax1.plot(range(len(game_df)), p(range(len(game_df))), 
                    "--", alpha=0.8, color='#FFFF00', linewidth=2)
        
        # 2. Score distribution histogram
        if len(game_df) > 0:
            ax2.hist(game_df['score'], bins=min(20, len(game_df)), 
                    color='#00FF00', alpha=0.7, edgecolor='white')
            ax2.set_title('Score Distribution', fontsize=14, pad=15)
            ax2.set_xlabel('Score')
            ax2.set_ylabel('Frequency')
            ax2.axvline(game_df['score'].mean(), color='#FFFF00', 
                       linestyle='--', linewidth=2, label=f'Mean: {game_df["score"].mean():.1f}')
            ax2.legend()
        
        # 3. Game duration vs Score scatter plot
        if 'duration_seconds' in game_df.columns and len(game_df) > 0:
            scatter = ax3.scatter(game_df['duration_seconds'], game_df['score'], 
                                c=game_df['foods_eaten'], cmap='viridis', 
                                s=60, alpha=0.7, edgecolors='white')
            ax3.set_title('Game Duration vs Score', fontsize=14, pad=15)
            ax3.set_xlabel('Duration (seconds)')
            ax3.set_ylabel('Score')
            ax3.grid(True, alpha=0.3)
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax3)
            cbar.set_label('Foods Eaten')
        
        # 4. Performance metrics
        if len(game_df) > 0:
            metrics = ['max_length', 'foods_eaten', 'direction_changes', 'total_moves']
            available_metrics = [m for m in metrics if m in game_df.columns]
            
            if available_metrics:
                # Calculate correlation matrix
                corr_data = game_df[['score'] + available_metrics].corr()['score'][1:]
                
                colors = ['#FF6B6B' if x < 0 else '#4ECDC4' for x in corr_data.values]
                bars = ax4.barh(range(len(corr_data)), corr_data.values, color=colors, alpha=0.8)
                ax4.set_yticks(range(len(corr_data)))
                ax4.set_yticklabels([m.replace('_', ' ').title() for m in corr_data.index])
                ax4.set_title('Score Correlation with Game Metrics', fontsize=14, pad=15)
                ax4.set_xlabel('Correlation with Score')
                ax4.grid(True, alpha=0.3, axis='x')
                
                # Add value labels on bars
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax4.text(width + 0.01 if width >= 0 else width - 0.01, 
                            bar.get_y() + bar.get_height()/2, 
                            f'{width:.3f}', ha='left' if width >= 0 else 'right', 
                            va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.94)
        
        # Save the plot
        plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        print(f"Performance dashboard saved as {output_file}")
        
        # Also show the plot
        plt.show()
    
    def create_progress_report(self) -> Dict[str, Any]:
        """
        Create a detailed progress report.
        
        Returns:
            Dict[str, Any]: Progress report data
        """
        game_df, scores_df = self.load_data()
        
        if game_df.empty:
            return {"error": "No game data available"}
        
        # Calculate various statistics
        total_games = len(game_df)
        total_playtime = game_df['duration_seconds'].sum() if 'duration_seconds' in game_df.columns else 0
        
        report = {
            "summary": {
                "total_games": total_games,
                "total_playtime_hours": round(total_playtime / 3600, 2),
                "average_score": round(game_df['score'].mean(), 2),
                "best_score": int(game_df['score'].max()),
                "worst_score": int(game_df['score'].min()),
                "score_std": round(game_df['score'].std(), 2)
            },
            "recent_performance": {},
            "achievements": []
        }
        
        # Recent performance (last 10 games)
        if len(game_df) >= 10:
            recent_games = game_df.tail(10)
            earlier_games = game_df.iloc[:-10] if len(game_df) > 10 else game_df.head(0)
            
            if not earlier_games.empty:
                report["recent_performance"] = {
                    "recent_avg_score": round(recent_games['score'].mean(), 2),
                    "earlier_avg_score": round(earlier_games['score'].mean(), 2),
                    "improvement": round(recent_games['score'].mean() - earlier_games['score'].mean(), 2)
                }
        
        # Achievements
        if total_games >= 10:
            report["achievements"].append("🎮 Dedicated Player - Played 10+ games")
        if game_df['score'].max() >= 100:
            report["achievements"].append("💯 Century Club - Scored 100+ points")
        if total_playtime >= 3600:  # 1 hour
            report["achievements"].append("⏰ Time Master - 1+ hour of playtime")
        
        # Consistency check
        if len(game_df) >= 5:
            cv = game_df['score'].std() / game_df['score'].mean()
            if cv < 0.5:
                report["achievements"].append("📊 Consistent Player - Low score variation")
        
        return report
    
    def print_progress_report(self) -> None:
        """Print a formatted progress report to console."""
        report = self.create_progress_report()
        
        if "error" in report:
            print(f"❌ {report['error']}")
            return
        
        print("\n" + "="*60)
        print("🐍 SNAKE GAME PROGRESS REPORT 🐍")
        print("="*60)
        
        # Summary
        summary = report["summary"]
        print(f"\n📊 GAME SUMMARY:")
        print(f"   Total Games Played: {summary['total_games']}")
        print(f"   Total Playtime: {summary['total_playtime_hours']} hours")
        print(f"   Average Score: {summary['average_score']}")
        print(f"   Best Score: {summary['best_score']}")
        print(f"   Score Range: {summary['worst_score']} - {summary['best_score']}")
        print(f"   Score Consistency (σ): {summary['score_std']}")
        
        # Recent performance
        if report["recent_performance"]:
            perf = report["recent_performance"]
            print(f"\n📈 RECENT PERFORMANCE (Last 10 Games):")
            print(f"   Recent Average: {perf['recent_avg_score']}")
            print(f"   Earlier Average: {perf['earlier_avg_score']}")
            improvement = perf['improvement']
            if improvement > 0:
                print(f"   Improvement: +{improvement} points 📈")
            elif improvement < 0:
                print(f"   Change: {improvement} points 📉")
            else:
                print(f"   Change: No change ➡️")
        
        # Achievements
        if report["achievements"]:
            print(f"\n🏆 ACHIEVEMENTS:")
            for achievement in report["achievements"]:
                print(f"   {achievement}")
        
        print("\n" + "="*60)

def main():
    """Main function to demonstrate data visualization."""
    print("Snake Game Data Visualizer")
    print("=" * 40)
    
    visualizer = GameDataVisualizer()
    
    # Print progress report
    visualizer.print_progress_report()
    
    # Create performance dashboard
    try:
        visualizer.create_performance_dashboard()
    except Exception as e:
        print(f"Could not create dashboard: {e}")
        print("Make sure you have played some games first!")

if __name__ == "__main__":
    main()