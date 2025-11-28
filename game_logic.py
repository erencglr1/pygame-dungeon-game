from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class Character:
    name: str
    max_hp: int
    hp: int
    attack: int
    defense: int
    gold: int = 0
    potions: int = 2
    level: int = 1
    xp: int = 0

    def status_text(self) -> str:
        return (
            f"{self.name} | Lv {self.level} | "
            f"HP {self.hp}/{self.max_hp} | ATK {self.attack} | "
            f"DEF {self.defense} | Gold {self.gold} | Potions {self.potions}"
        )

    def attack_enemy(self, target: Enemy) -> str:
        damage = max(1, self.attack + random.randint(-2, 2) - target.defense)
        target.hp -= damage
        return f"You hit the {target.name} for {damage} damage."

    def heal(self) -> Optional[str]:
        if self.potions <= 0:
            return None
        self.potions -= 1
        amount = random.randint(8, 15)
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return f"You used a potion. HP: {old_hp} → {self.hp}"

    def level_up(self) -> str:
        self.level += 1
        hp_up = random.randint(4, 7)
        atk_up = random.randint(1, 2)
        self.max_hp += hp_up
        self.attack += atk_up
        self.defense += 1
        self.hp = self.max_hp
        return f"Level Up! +{hp_up} HP, +{atk_up} ATK, +1 DEF"


@dataclass
class Enemy:
    name: str
    hp: int
    attack: int
    defense: int
    reward_gold: int
    reward_xp: int


def create_random_enemy(player_level: int) -> Enemy:
    enemy_types = ["Goblin", "Skeleton", "Wolf", "Orc"]
    name = random.choice(enemy_types)
    hp = random.randint(12, 18) + player_level * 3
    atk = random.randint(4, 7) + player_level
    df = random.randint(1, 3) + player_level // 2
    gold = random.randint(5, 15) + player_level * 2
    xp = random.randint(8, 14) + player_level * 3
    return Enemy(name=name, hp=hp, attack=atk, defense=df, reward_gold=gold, reward_xp=xp)
