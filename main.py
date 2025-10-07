#!/usr/bin/env python3
"""
Snake Game - Portfolio Project
==============================

A classic Snake game implementation with modern features:
- Object-oriented design
- Statistics tracking and data persistence
- Configurable gameplay settings
- Professional code structure

Controls:
- Arrow Keys or WASD: Move snake
- SPACE: Pause/Resume
- R: Restart (when game over)
- ESC: Quit

Author: Your Name
GitHub: https://github.com/formertriton
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game import SnakeGame

def main():
    """Main entry point for the Snake game."""
    try:
        print("=" * 50)
        print("🐍 SNAKE GAME - PORTFOLIO PROJECT 🐍")
        print("=" * 50)
        print()
        
        # Create and run the game
        game = SnakeGame()
        game.run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install pygame pandas matplotlib numpy")
    finally:
        print("\nThanks for playing!")

if __name__ == "__main__":
    main()