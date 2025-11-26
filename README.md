# Dungeon Adventure – Pygame Project

Dungeon Adventure is a turn-based RPG mini-game built with **Python** and **Pygame**.  
The project includes character combat, items, level progression, enemies with unique stats,  
a shop system, and background music.  
This game was created as part of a software development assignment.

---

## 🎮 Features

- Hero with Health, Attack, Defense, Gold, and Experience
- Multiple enemy types:
  - Goblin
  - Skeleton
  - Wolf
  - Orc
- Each enemy has unique stats and its own image
- Turn-based combat system (Fight / Defend / Run)
- Shop system:
  - Buy potions
  - Upgrade sword
  - Upgrade armor
- Leveling system (XP → Level up → Stronger character)
- Background music (automatically disabled in cloud environments)
- Fully image-based UI using Pygame

---

## 📁 Project Structure
pygame-dungeon-game/
│
├── dungeon_game.py # Main game file
├── requirements.txt # Dependencies
├── README.md # Project documentation
│
└── assets/ # Game images & audio
├── background.png
├── hero.png
├── goblin.png
├── skeleton.png
├── wolf.png
├── orc.png
└── music.mp3

💡 Notes for Cloud Environments (GitHub Codespaces)

GitHub Codespaces does not support:
-Pygame graphics window
-Audio devices
Because of this:
-Background music will be automatically disabled
-The game window will not open in the browser
To test the game visually, run it on a local machine with Python installed.

Medium link:
https://medium.com/@erencglr3113/building-a-turn-based-dungeon-game-with-python-pygame-33e6e984b2e3?postPublishedType=initial