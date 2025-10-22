#!/usr/bin/env python3
"""
Dodge Like Naruto - Game Launcher
A fast-paced endless runner game where you control a ninja dodging projectiles!
"""

import sys
import subprocess
import os

def check_pygame():
    """Check if pygame is installed, install if not"""
    try:
        import pygame
        print("✅ Pygame is installed!")
        return True
    except ImportError:
        print("❌ Pygame not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("✅ Pygame installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pygame. Please install manually:")
            print("   pip install pygame")
            return False

def main():
    print("🥷 Welcome to Dodge Like Naruto!")
    print("=" * 50)
    
    # Check pygame installation
    if not check_pygame():
        return
    
    print("\n🎮 Starting the game...")
    print("Controls:")
    print("  • Arrow Keys: Move your ninja")
    print("  • Collect power-ups to gain abilities")
    print("  • Survive as long as possible!")
    print("\nPress Ctrl+C to quit the game")
    print("=" * 50)
    
    try:
        # Import and run the game
        from main import Game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error running game: {e}")
        print("Please make sure all files are in the same directory.")

if __name__ == "__main__":
    main()
