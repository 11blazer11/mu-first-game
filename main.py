import sys
from random import randint, choice
import pygame

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

GREEN = (46, 245, 39)
RED = (255, 0, 0)
BLUE = (39, 93, 245)
WHITE = (255, 255, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Test Pygame")
background = pygame.image.load("back.jpg")
player = pygame.image.load("player.png")

class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = randint(0, WINDOW_WIDTH - self.width)
        self.y = randint(0, WINDOW_HEIGHT - self.height)
        self.color = choice([GREEN, BLUE])
        self.speed = choice([2, 3, 4])
        self.touch = False

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


enemies = [Enemy() for _ in range(7)]

player_width = 50
player_height = 50
player_x = 250
player_y = 350
player_speed = 5

score = 0
game_over = False
running = True

while running:
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_w] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < WINDOW_HEIGHT - player_height:
            player_y += player_speed

        for enemy in enemies:
            enemy.draw()

            if player_x < enemy.x + enemy.width and player_x + player_width > enemy.x \
                    and player_y < enemy.y + enemy.height and player_y + player_height > enemy.y:
                if enemy.color == BLUE and not enemy.touch:
                    score -= 100
                    enemy.touch = True
                    if score < 0:
                        game_over = True
                if enemy.color == GREEN and not enemy.touch:
                    score += 100
                    enemy.touch = True

    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        window.blit(text, (200, 250))

    font = pygame.font.Font(None, 74)
    text = font.render(f"score: {score}", True, WHITE)
    window.blit(text, (10, 10))

    window.blit(player, (player_x, player_y))

    pygame.display.update()

    pygame.time.Clock().tick(120)

pygame.quit()
sys.exit()
