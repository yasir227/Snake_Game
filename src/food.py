import pygame
import random
from typing import Tuple, List

class Food:
    """
    Food class representing food items in the Snake game.
    
    This class handles food placement, collision detection with snake,
    and rendering. It ensures food doesn't spawn on the snake's body.
    """
    
    def __init__(self, cell_size: int, grid_width: int, grid_height: int):
        """
        Initialize food object.
        
        Args:
            cell_size (int): Size of each cell in pixels
            grid_width (int): Width of game grid in cells
            grid_height (int): Height of game grid in cells
        """
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (0, 0)
        self.foods_eaten = 0
        
        # Generate initial food position
        self.spawn_food([])
    
    def spawn_food(self, snake_body: List[Tuple[int, int]]) -> None:
        """
        Spawn food at random position not occupied by snake.
        
        Args:
            snake_body (List[Tuple[int, int]]): Current snake body positions
        """
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            potential_position = (x, y)
            
            if potential_position not in snake_body:
                self.position = potential_position
                break
                
            attempts += 1
        
        # Fallback: if we can't find empty space, place at (0,0)
        if attempts >= max_attempts:
            self.position = (0, 0)
    
    def check_collision(self, snake_head: Tuple[int, int]) -> bool:
        """
        Check if snake head collided with food.
        
        Args:
            snake_head (Tuple[int, int]): Position of snake's head
            
        Returns:
            bool: True if collision detected
        """
        if snake_head == self.position:
            self.foods_eaten += 1
            return True
        return False
    
    def get_position(self) -> Tuple[int, int]:
        """Get current food position."""
        return self.position
    
    def draw(self, surface: pygame.Surface, colors: dict) -> None:
        """
        Draw food on the game surface.
        
        Args:
            surface (pygame.Surface): Surface to draw on
            colors (dict): Color configuration
        """
        x, y = self.position
        rect = pygame.Rect(
            x * self.cell_size + 2,
            y * self.cell_size + 2,
            self.cell_size - 4,
            self.cell_size - 4
        )
        
        # Draw food as a circle
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        
        pygame.draw.circle(surface, colors['food'], (center_x, center_y), radius)
        pygame.draw.circle(surface, colors['text'], (center_x, center_y), radius, 2)
    
    def get_stats(self) -> dict:
        """
        Get food statistics.
        
        Returns:
            dict: Dictionary containing food-related metrics
        """
        return {
            'foods_eaten': self.foods_eaten,
            'current_position': self.position
        }