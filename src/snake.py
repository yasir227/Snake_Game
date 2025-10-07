import pygame
from enum import Enum
from typing import List, Tuple

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    """
    Snake class representing the player-controlled snake in the game.
    
    This class handles snake movement, growth, collision detection,
    and rendering. It maintains the snake's body as a list of segments.
    """
    
    def __init__(self, start_x: int, start_y: int, cell_size: int):
        """
        Initialize the snake at starting position.
        
        Args:
            start_x (int): Starting x coordinate (in grid units)
            start_y (int): Starting y coordinate (in grid units)
            cell_size (int): Size of each cell in pixels
        """
        self.cell_size = cell_size
        self.body = [(start_x, start_y)]
        self.direction = Direction.RIGHT
        self.grow_flag = False
        
        # Track movement history for analytics
        self.total_moves = 0
        self.direction_changes = 0
        
    def move(self) -> None:
        """Move the snake in its current direction."""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction.value
        
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
            
        self.total_moves += 1
    
    def change_direction(self, new_direction: Direction) -> bool:
        """
        Change snake's direction if valid.
        
        Args:
            new_direction (Direction): New direction to move
            
        Returns:
            bool: True if direction was changed, False if invalid
        """
        # Prevent 180-degree turns
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            if new_direction != self.direction:
                self.direction_changes += 1
            self.direction = new_direction
            return True
        return False
    
    def grow(self) -> None:
        """Mark snake to grow on next move."""
        self.grow_flag = True
    
    def check_wall_collision(self, width: int, height: int) -> bool:
        """
        Check if snake collided with walls.
        
        Args:
            width (int): Game width in grid units
            height (int): Game height in grid units
            
        Returns:
            bool: True if collision detected
        """
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= width or 
                head_y < 0 or head_y >= height)
    
    def check_self_collision(self) -> bool:
        """
        Check if snake collided with itself.
        
        Returns:
            bool: True if self-collision detected
        """
        head = self.body[0]
        return head in self.body[1:]
    
    def get_head_position(self) -> Tuple[int, int]:
        """Get the position of snake's head."""
        return self.body[0]
    
    def get_length(self) -> int:
        """Get current length of snake."""
        return len(self.body)
    
    def draw(self, surface: pygame.Surface, colors: dict) -> None:
        """
        Draw the snake on the game surface.
        
        Args:
            surface (pygame.Surface): Surface to draw on
            colors (dict): Color configuration
        """
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(
                x * self.cell_size, 
                y * self.cell_size, 
                self.cell_size, 
                self.cell_size
            )
            
            # Draw head in different color
            if i == 0:
                pygame.draw.rect(surface, colors['snake_head'], rect)
                pygame.draw.rect(surface, colors['text'], rect, 2)
            else:
                pygame.draw.rect(surface, colors['snake'], rect)
                pygame.draw.rect(surface, colors['background'], rect, 1)
    
    def get_analytics_data(self) -> dict:
        """
        Get analytics data about snake performance.
        
        Returns:
            dict: Dictionary containing various metrics
        """
        return {
            'length': self.get_length(),
            'total_moves': self.total_moves,
            'direction_changes': self.direction_changes,
            'efficiency_ratio': self.get_length() / max(self.total_moves, 1)
        }