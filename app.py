from __future__ import annotations

from typing import List, Optional

from flask import Flask, redirect, render_template, request, url_for

from game_logic import Character, Enemy, create_random_enemy

app = Flask(__name__)

# ---- Very simple global state (ok for single-player demo) ----
player: Optional[Character] = None
enemy: Optional[Enemy] = None
room: int = 0
messages: List[str] = []


def add_message(text: str) -> None:
    messages.append(text)
    if len(messages) > 6:
        messages.pop(0)


@app.route("/", methods=["GET", "POST"])
def index():
    global player, enemy, room

    if player is None:
        # first visit / restart
        player = Character(name="Hero", max_hp=30, hp=30, attack=6, defense=2)
        enemy = None
        room = 0
        messages.clear()
        add_message("Welcome to the web version of Dungeon Adventure!")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "next_room":
            room += 1
            enemy = create_random_enemy(player.level)
            messages.clear()
            add_message(f"You enter room {room}. A {enemy.name} appears!")

        elif action == "attack" and enemy:
            add_message(player.attack_enemy(enemy))
            if enemy.hp <= 0:
                add_message(f"You defeated the {enemy.name}!")
                player.gold += enemy.reward_gold
                player.xp += enemy.reward_xp
                add_message(
                    f"+{enemy.reward_gold} gold, +{enemy.reward_xp} XP gained."
                )

                xp_needed = player.level * 20
                while player.xp >= xp_needed:
                    player.xp -= xp_needed
                    add_message(player.level_up())
                    xp_needed = player.level * 20

                enemy = None
            else:
                dmg = max(1, enemy.attack - player.defense)
                player.hp -= dmg
                add_message(f"{enemy.name} hits you back for {dmg} damage.")
                if player.hp <= 0:
                    add_message("You died... Game over.")

        elif action == "heal":
            msg = player.heal()
            if msg is None:
                add_message("You have no potions left.")
            else:
                add_message(msg)

        elif action == "run":
            enemy = None
            add_message("You ran away from the battle.")

        elif action == "restart":
            player = None
            enemy = None
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        player=player,
        enemy=enemy,
        room=room,
        messages=messages,
    )


if __name__ == "__main__":
    app.run(debug=True)
