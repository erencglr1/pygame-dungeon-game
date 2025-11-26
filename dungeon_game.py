import pygame
import random
import sys


# =====================================================
#                   GAME SETTINGS
# =====================================================

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
BLUE = (0, 120, 220)
YELLOW = (230, 200, 0)


# =====================================================
#                   CHARACTER CLASS
# =====================================================

class Character:
    def __init__(self, name, hp, attack, defense, gold=0, potions=2):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = gold
        self.potions = potions
        self.level = 1
        self.xp = 0

    def status_text(self):
        return f"{self.name} | Lv: {self.level} | HP: {self.hp}/{self.max_hp} | ATK: {self.attack} | DEF: {self.defense} | Gold: {self.gold} | Potions: {self.potions}"

    def attack_enemy(self, target):
        dmg = max(1, self.attack + random.randint(-2, 2) - target.defense)
        target.hp -= dmg
        return f"You hit {target.name} for {dmg} damage!"

    def heal(self):
        if self.potions <= 0:
            return None
        self.potions -= 1
        amount = random.randint(8, 15)
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return f"You used a potion. HP: {before} → {self.hp}"

    def level_up(self):
        self.level += 1
        hp_up = random.randint(4, 8)
        atk_up = random.randint(1, 2)

        self.max_hp += hp_up
        self.attack += atk_up
        self.defense += 1
        self.hp = self.max_hp

        return f"LEVEL UP! HP +{hp_up}, ATK +{atk_up}, DEF +1"


# =====================================================
#                   ENEMY CLASS
# =====================================================

class Enemy:
    def __init__(self, name, hp, attack, defense, reward_gold, reward_xp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp

    def attack_player(self, target):
        dmg = max(1, self.attack + random.randint(-2, 2) - target.defense)
        target.hp -= dmg
        return f"{self.name} hits you for {dmg} damage!"


def random_enemy(player_level):
    types = ["Goblin", "Skeleton", "Wolf", "Orc"]
    t = random.choice(types)

    hp = random.randint(12, 18) + player_level * 3
    atk = random.randint(4, 7) + player_level
    df = random.randint(1, 3) + (player_level // 2)
    gold = random.randint(5, 15) + player_level * 2
    xp = random.randint(8, 14) + player_level * 3

    return Enemy(t, hp, atk, df, gold, xp)


# =====================================================
#                     UTILITIES
# =====================================================

def add_message(msg_list, msg):
    if msg:
        msg_list.append(msg)
        if len(msg_list) > 7:
            msg_list.pop(0)


def draw_text(surface, text, x, y, font, color=WHITE):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def create_buttons(labels, y_start, x_center):
    buttons = []
    w, h = 220, 40
    margin = 10
    y = y_start

    for text, action in labels:
        rect = pygame.Rect(x_center - w // 2, y, w, h)
        buttons.append({"rect": rect, "text": text, "action": action})
        y += h + margin

    return buttons


def draw_buttons(surface, buttons, font):
    for b in buttons:
        pygame.draw.rect(surface, LIGHT_GRAY, b["rect"], border_radius=8)
        pygame.draw.rect(surface, WHITE, b["rect"], 2, border_radius=8)
        txt = font.render(b["text"], True, WHITE)
        surface.blit(txt, txt.get_rect(center=b["rect"].center))


# =====================================================
#                     MAIN GAME
# =====================================================

def main():
    pygame.init()
    pygame.mixer.init()

    # Background music
    try:
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Music could not be loaded.")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dungeon Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 20)
    big_font = pygame.font.SysFont("consolas", 28)

    # Load Images
    background = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))
    hero_img = pygame.transform.scale(pygame.image.load("assets/hero.png"), (150, 150))

    enemy_images = {
        "Goblin": pygame.transform.scale(pygame.image.load("assets/goblin.png"), (150, 150)),
        "Skeleton": pygame.transform.scale(pygame.image.load("assets/skeleton.png"), (150, 150)),
        "Wolf": pygame.transform.scale(pygame.image.load("assets/wolf.png"), (150, 150)),
        "Orc": pygame.transform.scale(pygame.image.load("assets/orc.png"), (150, 150)),
    }

    # Game State
    player = Character("Hero", 30, 6, 2)
    current_enemy = None
    room = 0
    state = "decision"
    title = "Welcome!"
    messages = []
    pending_action = None

    # Attack animation
    hero_offset = 0
    enemy_offset = 0
    hero_anim = 0
    enemy_anim = 0
    ANIM_FRAMES = 8

    running = True

    while running:
        clock.tick(FPS)

        # Update animations
        if hero_anim > 0:
            hero_anim -= 1
            hero_offset = 20 if hero_anim > ANIM_FRAMES // 2 else 0

        if enemy_anim > 0:
            enemy_anim -= 1
            enemy_offset = -20 if enemy_anim > ANIM_FRAMES // 2 else 0

        # UI buttons
        if state == "decision":
            labels = [("Enter Next Room", "next"), ("Quit", "quit")]

        elif state == "battle":
            labels = [("Attack", "attack"), ("Heal", "heal"), ("Run", "run"), ("Give Up", "giveup")]

        elif state == "shop":
            labels = [
                ("Buy Potion (10g)", "buy"),
                ("Upgrade Sword (20g)", "atk"),
                ("Upgrade Armor (20g)", "def"),
                ("Leave", "leave"),
            ]

        elif state == "message":
            labels = [("OK", "ok"), ("Quit", "quit")]

        elif state == "gameover":
            labels = [("Restart", "restart"), ("Quit", "quit")]

        buttons = create_buttons(labels, 360, WIDTH // 2)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    if b["rect"].collidepoint(event.pos):
                        pending_action = b["action"]

        # Process actions
        if pending_action:
            action = pending_action
            pending_action = None

            # ==================== DECISION ====================
            if state == "decision":
                if action == "next":
                    room += 1
                    r = random.choice(["enemy", "treasure", "trap", "shop"])

                    if r == "enemy":
                        current_enemy = random_enemy(player.level)
                        add_message(messages, f"A {current_enemy.name} appeared!")
                        title = f"Room {room}"
                        state = "battle"

                    elif r == "treasure":
                        g = random.randint(5, 25)
                        player.gold += g
                        add_message(messages, f"You found {g} gold!")
                        state = "message"

                    elif r == "trap":
                        dmg = random.randint(3, 10)
                        player.hp -= dmg
                        add_message(messages, f"A trap hit you for {dmg}!")
                        if player.hp <= 0:
                            state = "gameover"
                        else:
                            state = "message"

                    elif r == "shop":
                        add_message(messages, "A merchant appears.")
                        state = "shop"

                elif action == "quit":
                    running = False

            # ==================== BATTLE ====================
            elif state == "battle":
                if action == "attack":
                    hero_anim = ANIM_FRAMES
                    add_message(messages, player.attack_enemy(current_enemy))

                    if current_enemy.hp <= 0:
                        add_message(messages, f"You killed the {current_enemy.name}!")
                        player.gold += current_enemy.reward_gold
                        player.xp += current_enemy.reward_xp
                        add_message(messages, f"+{current_enemy.reward_gold} Gold, +{current_enemy.reward_xp} XP")

                        # LEVEL UP SYSTEM
                        xp_needed = player.level * 20
                        while player.xp >= xp_needed:
                            player.xp -= xp_needed
                            add_message(messages, f"LEVEL {player.level + 1}!")
                            add_message(messages, player.level_up())
                            xp_needed = player.level * 20

                        current_enemy = None
                        title = "Victory!"
                        state = "message"

                    else:
                        enemy_anim = ANIM_FRAMES
                        add_message(messages, current_enemy.attack_player(player))
                        if player.hp <= 0:
                            state = "gameover"

                elif action == "heal":
                    msg = player.heal()
                    add_message(messages, msg if msg else "No potions left!")

                    if current_enemy and player.hp > 0:
                        enemy_anim = ANIM_FRAMES
                        add_message(messages, current_enemy.attack_player(player))
                        if player.hp <= 0:
                            state = "gameover"

                elif action == "run":
                    if random.random() < 0.5:
                        add_message(messages, "You escaped!")
                        current_enemy = None
                        state = "message"
                    else:
                        enemy_anim = ANIM_FRAMES
                        add_message(messages, "You failed to escape!")
                        add_message(messages, current_enemy.attack_player(player))
                        if player.hp <= 0:
                            state = "gameover"

                elif action == "giveup":
                    add_message(messages, "You surrendered.")
                    state = "gameover"

            # ==================== SHOP ====================
            elif state == "shop":
                if action == "buy":
                    if player.gold >= 10:
                        player.gold -= 10
                        player.potions += 1
                        add_message(messages, "You bought a potion.")
                    else:
                        add_message(messages, "Not enough gold.")

                elif action == "atk":
                    if player.gold >= 20:
                        player.gold -= 20
                        player.attack += 1
                        add_message(messages, "Sword upgraded!")
                    else:
                        add_message(messages, "Not enough gold.")

                elif action == "def":
                    if player.gold >= 20:
                        player.gold -= 20
                        player.defense += 1
                        add_message(messages, "Armor upgraded!")
                    else:
                        add_message(messages, "Not enough gold.")

                elif action == "leave":
                    state = "decision"

            # ==================== MESSAGE ====================
            elif state == "message":
                if action == "ok":
                    state = "decision"
                elif action == "quit":
                    running = False

            # ==================== GAME OVER ====================
            elif state == "gameover":
                if action == "restart":
                    return main()
                elif action == "quit":
                    running = False

        # ==========================================================
        # DRAW EVERYTHING
        # ==========================================================

        screen.blit(background, (0, 0))
        screen.blit(hero_img, (50 + hero_offset, 380))

        if current_enemy and state == "battle":
            img = enemy_images[current_enemy.name]
            screen.blit(img, (WIDTH - 200 + enemy_offset, 380))

        draw_text(screen, "DUNGEON ADVENTURE", 20, 10, big_font, YELLOW)
        draw_text(screen, f"Room: {room}", 20, 45, font)
        draw_text(screen, player.status_text(), 20, 80, font)
        draw_text(screen, title, 20, 140, font, BLUE)

        pygame.draw.rect(screen, GRAY, (20, 180, WIDTH - 40, 150))
        pygame.draw.rect(screen, WHITE, (20, 180, WIDTH - 40, 150), 2)

        y = 190
        for m in messages:
            draw_text(screen, m, 30, y, font)
            y += 24

        draw_buttons(screen, buttons, font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
