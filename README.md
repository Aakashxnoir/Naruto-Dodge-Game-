# 🥷 Dodge Like Naruto - Enhanced Edition

A fast-paced endless runner game where you control a ninja dodging projectiles from all directions! This enhanced version includes numerous improvements, new features, and professional polish.

## 🎮 How to Play

### Controls
- **Arrow Keys**: Move your ninja around the screen
- **SPACE**: Dash (with cooldown)
- **X**: Special Attack (with cooldown)
- **P**: Pause game
- **ESC**: Quit/Return to menu
- **S**: Toggle sound effects
- **O**: Open settings menu
- **A**: View achievements

### Gameplay
- **Goal**: Survive as long as possible and achieve the highest score
- **Avoid**: Kunai, fireballs, shuriken, lightning, ice shards, and wind blades coming from all directions
- **Defeat**: Enemy ninjas, assassins, and bosses that chase you
- **Collect**: Power-ups to gain special abilities
- **Progressive Difficulty**: Game gets harder as your score increases with 5 different stages

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

## 🎯 Enhanced Features

### 🎨 Visual Enhancements
- **Larger Screen**: Increased resolution to 1000x700
- **Enhanced Graphics**: Better sprites, animations, and visual effects
- **Stage Themes**: 5 different visual themes with unique colors and atmospheres
- **Particle Systems**: Explosions, trails, and special effects
- **Animated Backgrounds**: Parallax scrolling star fields
- **Professional UI**: Clean menus, HUD, and status indicators

### 🎵 Audio System
- **Sound Effects**: Collect, hit, dash, level up, and game over sounds
- **Dynamic Audio**: Procedurally generated beep sounds
- **Audio Controls**: Toggle sound effects and background music
- **Volume Management**: Built-in audio settings

### ⚔️ Gameplay Mechanics
- **Enemy System**: 3 types of enemies (ninja, assassin, boss) with AI
- **Special Attacks**: Powerful area-of-effect attack with cooldown
- **Dash System**: Quick movement with cooldown management
- **Health System**: 3-hit health system with visual indicators
- **Power-up System**: 6 different power-ups with unique effects
- **Level Progression**: 5 stages with increasing difficulty

### 🏆 Power-ups & Abilities
- 🚀 **Speed Boost** (Cyan): 1.5x movement speed for 5 seconds
- 🛡️ **Shield** (Blue): Absorbs one hit for 10 seconds
- ⏰ **Slow Time** (Purple): Slows all projectiles for 5 seconds
- 💥 **Multi-Shot** (Yellow): Enhanced attack capabilities for 7.5 seconds
- ❤️ **Health** (Green): Restores one health point
- ✨ **Invincible** (Gold): Complete invincibility for 5 seconds

### 🎯 Projectile Types
- 🗡️ **Kunai** (Red/Blue/Gray): Throwing knives with detailed sprites
- 🔥 **Fireball** (Red/Orange/Yellow): Animated flame effects
- ⭐ **Shuriken** (Purple/Cyan/Green): Rotating throwing stars
- ⚡ **Lightning** (Yellow/White): Electric bolts with crackling effects
- ❄️ **Ice Shard** (Cyan/Blue/White): Crystalline projectiles with sparkles
- 🌪️ **Wind Blade** (Green/White/Gray): Slashing air attacks

### 🏅 Achievement System
- **First Game**: Play your first game
- **Score 1000**: Reach a score of 1000
- **Score 5000**: Reach a score of 5000
- **Score 10000**: Reach a score of 10000
- **Survive 60s**: Survive for 60 seconds
- **Collect 10 Power-ups**: Collect 10 power-ups in one game
- **Perfect Dash**: Use dash 20 times in one game
- **No Damage Run**: Reach 1000 points without taking damage

### 🎮 User Interface
- **Splash Screen**: Animated startup with progress bar
- **Main Menu**: Professional title screen with controls
- **Settings Menu**: Comprehensive options and controls
- **Achievements Screen**: Track your progress and unlocks
- **Pause Screen**: Quick pause with resume options
- **Game Over Screen**: Detailed statistics and restart options
- **Mini-map/Radar**: Real-time enemy and power-up tracking
- **FPS Counter**: Optional performance monitoring

### ⚙️ Settings & Options
- **Sound Effects**: Toggle on/off
- **Background Music**: Toggle on/off
- **Difficulty**: Easy, Normal, Hard
- **Particle Effects**: Toggle visual effects
- **FPS Display**: Show/hide frame rate counter
- **Persistent Settings**: All settings saved automatically

### 🎯 Stage System
- **Stage 1**: Blue theme - Basic projectiles and enemies
- **Stage 2**: Red theme - Added lightning projectiles and more enemies
- **Stage 3**: Green theme - Ice shards and enhanced enemy AI
- **Stage 4**: Purple theme - Wind blades and boss enemies
- **Stage 5**: Yellow theme - All projectile types and maximum difficulty

## 🎨 Visual Elements

- **Animated Ninja**: Detailed character with headband, bouncing animation, and expressions
- **Colorful Projectiles**: Each type has unique visual style and behavior
- **Particle System**: Dynamic visual feedback for all interactions
- **Professional UI**: Clean menus, score displays, and status indicators
- **Atmospheric Backgrounds**: Stage-specific themes with parallax scrolling
- **Special Effects**: Dash trails, special attack auras, and power-up glows

## 🔧 Technical Details

- **Built with**: Python 3.7+ and Pygame
- **Performance**: 60 FPS smooth gameplay with FPS counter
- **Architecture**: Object-oriented design with clean separation
- **Features**: 
  - State management (Splash/Menu/Playing/Paused/Settings/Achievements/Game Over)
  - High score persistence with JSON
  - Achievement system with progress tracking
  - Particle system for visual effects
  - Power-up system with timers
  - Enemy AI with pathfinding
  - Collision detection with shield mechanics
  - Sound system with procedural audio
  - Settings persistence
  - Performance monitoring

## 🎵 Game States

1. **Splash Screen**: Animated startup with loading progress
2. **Main Menu**: Title screen with high score and navigation
3. **Settings**: Comprehensive options and controls
4. **Achievements**: Progress tracking and unlocks
5. **Playing**: Active gameplay with all features
6. **Paused**: Quick pause with resume options
7. **Game Over**: Final score with detailed statistics

## 🏆 Scoring System

- Score increases over time (1 point per frame)
- Bonus points for defeating enemies (100 points each)
- High score is automatically saved and displayed
- New high score notifications
- Progressive difficulty scaling
- Stage progression every 1000 points

## 🎮 Advanced Features

- **Particle Effects**: Dynamic visual feedback for all interactions
- **State Management**: Professional game flow with multiple screens
- **High Score Persistence**: Automatic saving and loading
- **Visual Polish**: Animated characters, rotating projectiles, effects
- **User Experience**: Clear instructions, status indicators, smooth controls
- **Performance Optimization**: FPS monitoring and efficient rendering
- **Audio System**: Procedural sound effects and music controls
- **Achievement System**: Progress tracking and unlock notifications

## 🎯 Tips for High Scores

1. **Collect Power-ups**: They're essential for survival at higher levels
2. **Use Shield Wisely**: Save it for when you're in tight spots
3. **Master Dash Timing**: Use for quick escapes or power-up collection
4. **Special Attack Strategy**: Perfect for clearing dense enemy areas
5. **Stay Mobile**: Keep moving to avoid getting trapped
6. **Watch the Radar**: Use the mini-map to plan your movements
7. **Learn Enemy Patterns**: Different enemies have different behaviors
8. **Stage Awareness**: Each stage has unique challenges and opportunities

## 🛠️ Development Features

- **Modular Design**: Easy to extend with new features
- **Clean Code**: Well-documented and organized
- **Error Handling**: Graceful fallbacks for missing files
- **Cross-platform**: Works on Windows, Mac, and Linux
- **Performance Monitoring**: Built-in FPS counter and optimization
- **Settings Management**: Persistent user preferences
- **Achievement System**: Comprehensive progress tracking

## 🎮 Controls Summary

| Key | Action |
|-----|--------|
| Arrow Keys | Move ninja |
| SPACE | Dash |
| X | Special Attack |
| P | Pause |
| ESC | Quit/Return to menu |
| S | Toggle sound |
| O | Settings |
| A | Achievements |
| M | Toggle music (in settings) |
| D | Change difficulty (in settings) |
| F | Toggle FPS display (in settings) |

## 🚀 Installation Requirements

- Python 3.7 or higher
- Pygame 2.5.2 or higher
- 100MB free disk space
- 512MB RAM minimum
- Any modern operating system (Windows, Mac, Linux)

## 📁 File Structure

```
Dodge Like Naruto/
├── main.py              # Main game code
├── run_game.py          # Auto-installer and launcher
├── requirements.txt     # Dependencies
├── README.md           # This file
├── game_info.txt       # Game information
├── high_score.json     # High score data
├── achievements.json   # Achievement progress
└── settings.json       # User settings
```

## 🎉 What's New in Enhanced Edition

- ✅ **6x Larger Screen** (1000x700 vs 800x600)
- ✅ **5 Visual Stages** with unique themes
- ✅ **3 Enemy Types** with AI and different behaviors
- ✅ **6 Power-up Types** with enhanced effects
- ✅ **6 Projectile Types** with unique visuals
- ✅ **Special Attack System** with cooldown management
- ✅ **Dash System** with strategic movement
- ✅ **Health System** with visual indicators
- ✅ **Achievement System** with 8 achievements
- ✅ **Settings Menu** with comprehensive options
- ✅ **Sound System** with procedural audio
- ✅ **Mini-map/Radar** for tactical awareness
- ✅ **FPS Counter** for performance monitoring
- ✅ **Splash Screen** with loading animation
- ✅ **Enhanced UI** with professional polish
- ✅ **Particle Effects** for visual feedback
- ✅ **Progressive Difficulty** with stage scaling
- ✅ **Performance Optimization** for smooth gameplay

Enjoy dodging like a true ninja! 🥷✨

---

**Made with ❤️ using Python and Pygame**

*Enhanced Edition - All features completed and polished!*