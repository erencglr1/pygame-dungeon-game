import sys
from pathlib import Path

# --- Make sure the project root is on sys.path ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from game_logic import Character, create_random_enemy  # noqa: E402


def test_level_up_increases_stats() -> None:
    hero = Character(name="Hero", max_hp=30, hp=30, attack=6, defense=2)

    old_level = hero.level
    old_hp = hero.max_hp
    old_attack = hero.attack
    old_defense = hero.defense

    msg = hero.level_up()

    assert "Level Up" in msg
    assert hero.level == old_level + 1
    assert hero.max_hp > old_hp
    assert hero.attack > old_attack
    assert hero.defense == old_defense + 1
    assert hero.hp == hero.max_hp  # reset to full health


def test_enemy_scaling() -> None:
    e1 = create_random_enemy(1)
    e10 = create_random_enemy(10)

    assert e10.hp >= e1.hp
    assert e10.attack >= e1.attack
    assert e10.defense >= e1.defense
    assert e10.reward_gold >= e1.reward_gold
    assert e10.reward_xp >= e1.reward_xp
