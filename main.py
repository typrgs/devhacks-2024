import pygame
import sys

from character import *
from enemy import *


# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Movable Square")

player_size = 100
player_speed = 5

player = character(player_size, player_speed)
the_player = pygame.sprite.Group()
the_player.add(player)


enemies = pygame.sprite.Group()
enemy1 = enemy(player_size, player_speed-4)
enemies.add(enemy1)

def handle_movement():
    global player
    keys = pygame.key.get_pressed()
    if  player.getX() > 0:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.moveX(-1)
    if player.getX() < SCREEN_WIDTH - player.get_width():
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.moveX(1)
    if player.getY() > 0:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveY(-1)
    if player.getY() < SCREEN_HEIGHT - player.get_height():
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.moveY(1)


def enemy_ping(enemies, x, y):
    for e in enemies.sprites():
        if isinstance(e, enemy): 
            print("updated")
            e.player_location(x, y)

# Main game loop
running = True
while running:
    #update enemies location of player
    enemy_ping(enemies, player.getX(), player.getY())
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Handle player input
    handle_movement()

    # Draw the square
    enemies.update()
    the_player.update()
    the_player.draw(screen)
    enemies.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()