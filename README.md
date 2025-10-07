# 🐍 Snake Game - Data-Driven Portfolio Project

A modern implementation of the classic Snake game with advanced data analytics and visualization features. Built to showcase Python programming skills, object-oriented design, and data engineering capabilities.

<img width="801" height="631" alt="Screenshot 2025-08-06 122356" src="https://github.com/user-attachments/assets/d2f12599-ab17-4c71-8a4f-c2426d9faa33" />

<img width="795" height="621" alt="Screenshot 2025-08-06 122406" src="https://github.com/user-attachments/assets/c6feb752-81c8-4f62-bf75-9379753c5c11" />


# 🎮 Features

# Core Gameplay

Classic Snake mechanics with smooth controls
Configurable game settings via JSON configuration
Multiple control schemes (Arrow keys + WASD)
Pause/Resume functionality
Game over handling with restart option

# Data Analytics & Visualization

Comprehensive statistics tracking for each game session
Performance analytics including efficiency metrics
Data persistence with JSON file storage
Interactive data visualization with matplotlib
Progress reports and achievement system
High scores leaderboard



# Technical Features

Object-oriented architecture with clean separation of concerns
Modular design for easy extension and maintenance
Configuration management system
Professional code structure following Python best practices
Error handling and logging
Cross-platform compatibility


# 🚀 Quick Start


# Prerequisites

Python 3.8 or higher

- pip package manager


# Installation
1. Clone the repository

```
git clone https://github.com/formertriton/snake-game-portfolio.git
cd snake-game-portfolio
```



2. Install dependencies
```
pip install -r requirements.txt
```



3. Run the game

```
python main.py
```

That's it! The game will start immediately.

# 🎯 How to Play

| Control | Action |

|---------|--------|

| ↑ ↓ ← → or WASD | Move snake |

| SPACE | Pause/Resume |

| R | Restart (when game over) |

| ESC | Quit game |


# Objective

- Control the snake to eat food (red circles)
- Grow longer with each food consumed
- Avoid hitting walls or your own tail
- Achieve the highest score possible!


# 📊 Data Analytics Features



# Game Statistics Tracked

- Score and game length
- Game duration and efficiency metrics
- Movement patterns and direction changes
- Food consumption rate
- Performance trends over time

# Visualizations Available

Run the data visualizer to see your gaming analytics:
```
python src/data_visualizer.py

```

Generated Charts:

- Score progression over time with trend analysis
- Score distribution histogram
- Game duration vs performance correlation
- Performance metrics correlation matrix


# Sample Analytics Output

```

🐍 SNAKE GAME PROGRESS REPORT 🐍

================================

📊 GAME SUMMARY:

Total Games Played: 25

Total Playtime: 0.75 hours

Average Score: 85.6

Best Score: 180

Score Consistency (σ): 32.4



🏆 ACHIEVEMENTS:

🎮 Dedicated Player - Played 10+ games

💯 Century Club - Scored 100+ points

📊 Consistent Player - Low score variation

```



## 🏗️ Project Structure



```
snake-game-portfolio/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── main.py                   # Main game runner
├── config/
│   └── settings.json        # Game configuration
├── src/                     # Source code
│   ├── game.py              # Main game logic
│   ├── snake.py             # Snake class
│   ├── food.py              # Food class
│   ├── game_stats.py        # Statistics tracking
│   └── data_visualizer.py   # Data visualization
├── data/                    # Generated data files
│   ├── game_stats.json      # Game history
│   └── high_scores.json     # High scores
└── tests/                   # Unit tests (future)
```

# ⚙️ Configuration


Customize your game experience by editing `config/settings.json`:

```json
{
   "game": {
       "width": 800,
       "height": 600,
       "cell_size": 20,
       "initial_speed": 150,
       "colors": {
           "background": "#000000",
           "snake": "#00FF00",
           "food": "#FF0000"
       }
   }
}
```


# 🧪 Technical Implementation



# Object-Oriented Design

- Snake class: Handles movement, collision detection, and rendering
- Food class: Manages food placement and collision detection
- GameStats class: Tracks and persists game statistics
- SnakeGame class: Main game orchestrator
- GameDataVisualizer class: Analytics and visualization engine


# Data Engineering Features

- JSON-based data persistence for game statistics
- Pandas integration for data analysis
- Efficient data structures for game state management
- Real-time statistics calculation and tracking
- Data validation and error handling

# Performance Optimizations

- Efficient collision detection algorithms
- Optimized rendering with pygame
- Memory-efficient data structures
- Configurable frame rate control

# 📈 Skills Demonstrated

This project showcases proficiency in:

- Python Programming: Advanced OOP concepts and design patterns
- Game Development: pygame library and game loop architecture
- Data Engineering: Data collection, storage, and processing
- Data Visualization: matplotlib and statistical analysis
- Software Architecture: Modular design and separation of concerns
- Configuration Management: JSON-based configuration systems
- Error Handling: Robust error management and logging
- Documentation: Comprehensive project documentation
- Git Workflow: Professional version control practices


# 🔮 Future Enhancements



-Multiplayer support with networking
-Advanced AI opponents with different difficulty levels
-Power-ups and special items
-Sound effects and background music
-Web deployment with Flask/FastAPI
-Database integration (PostgreSQL/MongoDB)
-Machine learning for gameplay pattern analysis
-Real-time dashboard with live statistics
-Mobile responsive web version
-Tournament mode with brackets


# 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


# 📫 Contact

Angelo R - (https://github.com/formertriton)

Project Link: (https://github.com/formertriton/snake-game-portfolio)

---

⭐ Star this repository if you found it helpful!

<img width="1919" height="1030" alt="Screenshot 2025-08-06 122733" src="https://github.com/user-attachments/assets/01c8dd9d-cebf-4758-bcee-6bac810ca5c1" />


Built with ❤️ and Python

<img width="559" height="1017" alt="Screenshot 2025-08-06 123353" src="https://github.com/user-attachments/assets/698ce9f0-a460-4f37-9e7a-db4f95145df3" />
