# 🥷 Dodge Like Naruto

A fast-paced endless runner game where you control a ninja dodging projectiles from all directions! Features power-ups, particle effects, and a complete game experience.

## 🎮 How to Play

### Controls
- **Arrow Keys**: Move your ninja around the screen
- **SPACE**: Start game from main menu
- **R**: Restart after game over
- **M**: Return to main menu
- **ESC**: Quit game

### Gameplay
- **Goal**: Survive as long as possible and achieve the highest score
- **Avoid**: Kunai, fireballs, and shuriken coming from all directions
- **Collect**: Power-ups to gain special abilities
- **Progressive Difficulty**: Game gets harder as your score increases

## 🚀 Quick Start

### Easy Installation (Recommended)
```bash
python run_game.py
```
This script will automatically install pygame if needed and start the game!

### Manual Installation
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## 🎯 Game Features

### Core Gameplay
- **Smooth Movement**: Responsive arrow key controls with screen boundaries
- **Multiple Projectile Types**: 
  - 🗡️ **Kunai** (throwing knives) - Red/Blue
  - 🔥 **Fireballs** - Red/Orange/Yellow with flame effects
  - ⭐ **Shuriken** (throwing stars) - Purple/Cyan/Green with rotation
- **Progressive Difficulty**: Spawn rate increases over time
- **Collision Detection**: Game over when hit by projectiles

### Power-ups & Abilities
- 🚀 **Speed Boost** (Cyan): 1.5x movement speed for 5 seconds
- 🛡️ **Shield** (Blue): Absorbs one hit for 10 seconds
- ⏰ **Slow Time** (Purple): Slows all projectiles for 5 seconds

### Visual & Audio
- **Animated Character**: Bouncing ninja with head, eyes, and headband
- **Particle Effects**: Explosions and trails for visual polish
- **Rotating Projectiles**: Shuriken spin, fireballs have flame effects
- **Background**: Moving star field for atmosphere
- **Power-up Effects**: Visual indicators for active abilities

### Game Systems
- **High Score Persistence**: Saves your best score automatically
- **Main Menu**: Professional start screen with instructions
- **Game Over Screen**: Final score display with restart options
- **Real-time Status**: Shows active power-up timers
- **Progressive UI**: Instructions disappear as you learn

## 🎨 Visual Elements

- **Animated Ninja**: Detailed character with headband and bouncing animation
- **Colorful Projectiles**: Each type has unique visual style and behavior
- **Particle System**: Explosions and effects for power-ups and collisions
- **Professional UI**: Clean menus, score displays, and status indicators
- **Atmospheric Background**: Moving stars and visual effects

## 🔧 Technical Details

- **Built with**: Python 3.7+ and Pygame
- **Performance**: 60 FPS smooth gameplay
- **Architecture**: Object-oriented design with clean separation
- **Features**: 
  - State management (Menu/Playing/Game Over)
  - High score persistence with JSON
  - Particle system for visual effects
  - Power-up system with timers
  - Collision detection with shield mechanics

## 🎵 Game States

1. **Main Menu**: Title screen with high score and instructions
2. **Playing**: Active gameplay with all features
3. **Game Over**: Final score with restart/menu options

## 🏆 Scoring System

- Score increases over time (1 point per frame)
- High score is automatically saved and displayed
- New high score notifications
- Progressive difficulty scaling

## 🎮 Power-up System

| Power-up | Color | Effect | Duration |
|----------|-------|--------|----------|
| Speed Boost | Cyan | 1.5x movement speed | 5 seconds |
| Shield | Blue | Absorbs one hit | 10 seconds |
| Slow Time | Purple | Slows all projectiles | 5 seconds |

## 🚀 Advanced Features

- **Particle Effects**: Dynamic visual feedback for all interactions
- **State Management**: Professional game flow with menus
- **High Score Persistence**: Automatic saving and loading
- **Visual Polish**: Animated characters, rotating projectiles, effects
- **User Experience**: Clear instructions, status indicators, smooth controls

## 🎯 Tips for High Scores

1. **Collect Power-ups**: They're essential for survival at higher levels
2. **Use Shield Wisely**: Save it for when you're in tight spots
3. **Speed Boost Strategy**: Use for quick escapes or power-up collection
4. **Slow Time Timing**: Perfect for dense projectile areas
5. **Stay Mobile**: Keep moving to avoid getting trapped

## 🛠️ Development Features

- **Modular Design**: Easy to extend with new features
- **Clean Code**: Well-documented and organized
- **Error Handling**: Graceful fallbacks for missing files
- **Cross-platform**: Works on Windows, Mac, and Linux

Enjoy dodging like a true ninja! 🥷✨

---

**Made with ❤️ using Python and Pygame**
