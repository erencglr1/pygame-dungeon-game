📘 Dungeon Adventure – Python RPG (Pygame + Flask Web Version)

Dungeon Adventure is a turn-based RPG game built with Python, featuring both a Pygame desktop edition and a fully playable Flask web version deployed on Railway.
The project demonstrates clean software architecture, object-oriented design, dependency management via uv, code quality enforcement using ruff, and automated testing with pytest.

This repository is structured as a complete, production-ready Python project suitable for academic submissions, portfolio use, and deployment demonstrations.

🎮 Features
🕹️ Desktop Version (Pygame)

Character progression (HP, ATK, DEF, Level, XP)

Multiple enemy types (Goblin, Skeleton, Wolf, Orc)

Turn-based combat system

Random room generation (battle, treasure, traps, shop)

Inventory & potion system

Attack animations

Modular code using dataclasses

🌐 Web Version (Flask – Railway Deployment)

Playable directly in the browser

Buttons for attack, healing, running, restarting

Persistent in-session game state

Clean UI built with basic HTML/CSS

Deployed publicly using Railway + Gunicorn

📁 Project Structure
project/
│── dungeon_game.py        # Pygame desktop game
│── game_logic.py          # Core logic shared by both versions
│── app.py                 # Flask web application
│── pyproject.toml         # uv, ruff, pytest configuration
│── requirements.txt       # (Optional) dependency list for Railway
│── templates/
│     └── index.html       # Web UI
│── assets/
│     ├── hero.png
│     ├── goblin.png
│     ├── skeleton.png
│     ├── wolf.png
│     ├── orc.png
│     ├── background.png
│     └── music.mp3
└── tests/
      └── test_game.py     # pytest unit tests

🧪 Testing

All unit tests are written using pytest, and executed through uv:

uv run pytest


The tests cover:

Level-up mechanics

Enemy stat scaling

Base logic verification

Test output example:

2 passed in 0.05s

🔍 Code Quality: ruff

ruff is used for linting and static analysis:

uv run ruff check .


Configured via pyproject.toml with:

Line length control

Error/formatting rules

Exclusions

Python target version

📦 Install & Run (Desktop Edition)

1. Install dependencies

Using uv:

uv sync


Or using pip:

pip install pygame


2. Run the Pygame version

uv run python dungeon_game.py

🌐 Run the Web Version Locally
uv run python app.py


Then open:

http://127.0.0.1:5000/

🚀 Deployment (Railway)

The web version is deployed using Flask + Gunicorn.

Required dependencies:
flask
gunicorn
pygame (for local dev only)

Railway Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

Public Networking:

Port: 8000 (or $PORT if Railway auto-detects)

Domain: Railway will auto-generate a public URL

Once deployed, your game is reachable from:

https://pygame-dungeon-game-production.up.railway.app

🏗️ Technologies Used

Python 3.12

Pygame (desktop)

Flask (web)

Gunicorn (production server)

uv (dependency management)

ruff (linting)

pytest (testing)

Railway (deployment)

HTML/CSS (web UI)

🎯 Why This Project Is Valuable

This repository demonstrates:

Full-stack Python: both desktop and web

Clean architecture with shared logic

Professional development workflow

Modern Python tooling

Real deployment to a cloud platform

Academic-level clarity and documentation

It is a strong project example for:

✔ University coursework
✔ Developer portfolio
✔ Cloud deployment demonstration
✔ Python/Pygame learning