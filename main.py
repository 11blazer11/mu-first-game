import sys
from random import randint, choice
import pygame

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

GREEN = (46, 245, 39)
RED = (255, 0, 0)
BLUE = (39, 93, 245)
WHITE = (255, 255, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Test Pygame")
pygame.display.set_icon(pygame.image.load("gameicon.png"))
background = pygame.image.load("back.jpg")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
good_img = pygame.image.load("good.png")
random = pygame.image.load("random.png")

lose_sound = pygame.mixer.Sound("lose.mp3")
win_sound = pygame.mixer.Sound("won.mp3")

class Enemy:
    def __init__(self, enemy_type):
        self.enemy_type = enemy_type
        if enemy_type == "enemy":
            self.image = enemy_img
        else:
            self.image = good_img

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = randint(1, 3)
        self.x = randint(0, WINDOW_WIDTH - self.width)
        self.y = randint(0, WINDOW_HEIGHT - self.height)
        self.touch = False

    def move(self):
        self.x += self.speed
        if self.x > WINDOW_WIDTH:
            self.x = -self.width
            self.y = randint(0, WINDOW_HEIGHT - self.height)
            self.touch = False

    def draw(self):
        window.blit(self.image, (self.x, self.y))

class RandomSprite:
    def __init__(self):
        self.image = random
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = randint(0, WINDOW_WIDTH - self.width)
        self.y = randint(0, WINDOW_HEIGHT - self.height)
        self.touch = False

    def draw(self):
        window.blit(self.image, (self.x, self.y))

enemies = [Enemy("enemy") for _ in range(4)]
goods = [Enemy("good") for _ in range(4)]
random_sprite = RandomSprite()

player_width = player_img.get_width()
player_height = player_img.get_height()
player_x = 250
player_y = 350
player_speed = 5

score = 0
game_over = False
running = True
game_won = False

clock = pygame.time.Clock()

while running:
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_won:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_w] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < WINDOW_HEIGHT - player_height:
            player_y += player_speed

        for enemy in enemies + goods:
            enemy.draw()
            enemy.move()

            if player_x < enemy.x + enemy.width and player_x + player_width > enemy.x \
                    and player_y < enemy.y + enemy.height and player_y + player_height > enemy.y:
                if enemy.enemy_type == "enemy" and not enemy.touch:
                    score -= 100
                    enemy.touch = True
                elif enemy.enemy_type == "good" and not enemy.touch:
                    score += 100
                    enemy.touch = True

            if score < 0:
                lose_sound.play()
                game_over = True

        if 500 <= score < 550:
            random_sprite.draw()
        if player_x < random_sprite.x + random_sprite.width and player_x + player_width > random_sprite.x \
                and player_y < random_sprite.y + random_sprite.height and player_y + player_height > random_sprite.y:
            if not random_sprite.touch:
                score_change = choice([-350, 350])
                score += score_change
                random_sprite.touch = True

        if score >= 1000:
            for enemy in enemies:
                enemy.speed = 3.5

    if score >= 2000:
        font = pygame.font.Font(None, 74)
        text = font.render("You won", True, BLUE)
        window.blit(text, (200, 250))
        win_sound.play()
        game_won = True

    if score <= -100:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        window.blit(text, (200, 250))

    font = pygame.font.Font(None, 74)
    text = font.render(f"score: {score}", True, WHITE)
    window.blit(text, (10, 10))

    window.blit(player_img, (player_x, player_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
