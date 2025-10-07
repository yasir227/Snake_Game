import pygame
import json
import sys
import os
from typing import Dict, Any
from src.snake import Snake, Direction
from src.food import Food
from src.game_stats import GameStats

class SnakeGame:
    """
    Main Snake Game class that orchestrates the entire game.
    
    This class manages the game loop, handles user input, updates game state,
    renders graphics, and integrates with statistics tracking.
    """
    
    def __init__(self, config_path: str = "config/settings.json"):
        """
        Initialize the Snake game.
        
        Args:
            config_path (str): Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Snake Game - Portfolio Project")
        
        # Game settings
        self.width = self.config['game']['width']
        self.height = self.config['game']['height']
        self.cell_size = self.config['game']['cell_size']
        self.colors = self.config['game']['colors']
        
        # Calculate grid dimensions
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size
        
        # Create game surface
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self._init_game_objects()
        
        # Game state
        self.running = True
        self.game_over = False
        self.paused = False
        self.score = 0
        self.game_speed = self.config['game']['initial_speed']
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        print("Snake Game initialized successfully!")
        print(f"Grid size: {self.grid_width}x{self.grid_height}")
        print("Controls: Arrow Keys to move, SPACE to pause, ESC to quit")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load game configuration from JSON file.
        
        Args:
            config_path (str): Path to configuration file
            
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            # Return default configuration
            return {
                "game": {
                    "width": 800,
                    "height": 600,
                    "cell_size": 20,
                    "initial_speed": 150,
                    "speed_increase": 5,
                    "colors": {
                        "background": "#000000",
                        "snake": "#00FF00",
                        "snake_head": "#FFFF00",
                        "food": "#FF0000",
                        "text": "#FFFFFF",
                        "grid": "#333333"
                    }
                },
                "data": {
                    "save_game_history": True,
                    "stats_file": "data/game_stats.json",
                    "high_scores_file": "data/high_scores.json"
                },
                "features": {
                    "show_grid": True,
                    "show_score": True
                }
            }
    
    def _init_game_objects(self) -> None:
        """Initialize game objects for a new game."""
        # Create snake in center of grid
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = Snake(start_x, start_y, self.cell_size)
        
        # Create food
        self.food = Food(self.cell_size, self.grid_width, self.grid_height)
        
        # Create stats tracker
        stats_file = self.config['data']['stats_file']
        high_scores_file = self.config['data']['high_scores_file']
        self.stats = GameStats(stats_file, high_scores_file)
        self.stats.start_new_game()
    
    def handle_input(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.paused = not self.paused
                
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                
                elif not self.paused and not self.game_over:
                    # Movement controls
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)
    
    def update_game(self) -> None:
        """Update game state."""
        if self.paused or self.game_over:
            return
        
        # Move snake
        self.snake.move()
        
        # Check wall collision
        if self.snake.check_wall_collision(self.grid_width, self.grid_height):
            self.end_game()
            return
        
        # Check self collision
        if self.snake.check_self_collision():
            self.end_game()
            return
        
        # Check food collision
        if self.food.check_collision(self.snake.get_head_position()):
            self.snake.grow()
            self.score += 10
            
            # Increase speed slightly
            if self.game_speed > 50:
                self.game_speed -= self.config['game']['speed_increase']
            
            # Spawn new food
            self.food.spawn_food(self.snake.body)
        
        # Update statistics
        snake_data = self.snake.get_analytics_data()
        food_data = self.food.get_stats()
        self.stats.update_game_stats(snake_data, food_data, self.score)
    
    def draw_grid(self) -> None:
        """Draw background grid."""
        if not self.config['features']['show_grid']:
            return
        
        grid_color = pygame.Color(self.colors['grid'])
        
        # Draw vertical lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.height))
        
        # Draw horizontal lines
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.width, y))
    
    def draw_ui(self) -> None:
        """Draw user interface elements."""
        if not self.config['features']['show_score']:
            return
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, 
                                     pygame.Color(self.colors['text']))
        self.screen.blit(score_text, (10, 10))
        
        # Length
        length_text = self.small_font.render(f"Length: {self.snake.get_length()}", True,
                                           pygame.Color(self.colors['text']))
        self.screen.blit(length_text, (10, 50))
        
        # High score
        high_scores = self.stats.get_high_scores(1)
        if high_scores:
            high_score_text = self.small_font.render(f"Best: {high_scores[0]['score']}", True,
                                                   pygame.Color(self.colors['text']))
            self.screen.blit(high_score_text, (10, 75))
    
    def draw_game_over(self) -> None:
        """Draw game over screen."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, 
                                         pygame.Color(self.colors['text']))
        text_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True,
                                     pygame.Color(self.colors['text']))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True,
                                            pygame.Color(self.colors['text']))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self) -> None:
        """Draw pause screen."""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, pygame.Color(self.colors['text']))
        text_rect = pause_text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(pause_text, text_rect)
        
        continue_text = self.small_font.render("Press SPACE to continue", True,
                                             pygame.Color(self.colors['text']))
        continue_rect = continue_text.get_rect(center=(self.width//2, self.height//2 + 30))
        self.screen.blit(continue_text, continue_rect)
    
    def render(self) -> None:
        """Render the game."""
        # Clear screen
        self.screen.fill(pygame.Color(self.colors['background']))
        
        # Draw grid
        self.draw_grid()
        
        # Draw game objects
        self.food.draw(self.screen, self.colors)
        self.snake.draw(self.screen, self.colors)
        
        # Draw UI
        self.draw_ui()
        
        # Draw overlays
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
        
        # Update display
        pygame.display.flip()
    
    def end_game(self) -> None:
        """End the current game."""
        self.game_over = True
        self.stats.end_game()
        print(f"Game Over! Final Score: {self.score}")
        
        # Print some stats
        summary = self.stats.get_game_summary()
        print(f"Best Score: {summary['best_score']}")
        print(f"Games Played: {summary['total_games']}")
    
    def restart_game(self) -> None:
        """Restart the game."""
        self.game_over = False
        self.paused = False
        self.score = 0
        self.game_speed = self.config['game']['initial_speed']
        self._init_game_objects()
        print("Game restarted!")
    
    def run(self) -> None:
        """Main game loop."""
        print("Starting Snake Game...")
        
        while self.running:
            # Handle input
            self.handle_input()
            
            # Update game
            self.update_game()
            
            # Render
            self.render()
            
            # Control frame rate
            self.clock.tick(1000 // self.game_speed if self.game_speed > 0 else 60)
        
        # Cleanup
        pygame.quit()
        print("Game ended. Thanks for playing!")

def main():
    """Main function to run the game."""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()