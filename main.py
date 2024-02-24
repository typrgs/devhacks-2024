import pygame
import sys

from character import *
from enemy import *

from player import *
from character_frames import *
from inventory import *
from projectile import *
from item import *
from shop_setup import *
from entity_movement import *
from var_setup import *

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DIMENSION OF THE DERANGED DEITY')
bg = pygame.image.load("assets/bg.png").convert()

player = Player(player_size, player_speed, player_hp, (0,0), [player_down(), player_up(), player_left(), player_right()])
player_attacks = pygame.sprite.Group()#empty

the_player = pygame.sprite.Group()
the_player.add(player)

inv = pygame.sprite.Group(Inventory((SCREEN_WIDTH/2 + 8,SCREEN_HEIGHT/2 + INV_HEIGHT_OFFSET)))
raba = Item("Rabadon's Deathcap", (SCREEN_WIDTH/2 + 8,SCREEN_HEIGHT/2 + INV_HEIGHT_OFFSET), "assets/raba.png", 120, 0, 25)
stormsurge = Item("Stormsurge", (SCREEN_WIDTH/2 + 8,SCREEN_HEIGHT/2 + INV_HEIGHT_OFFSET), "assets/stormsurge.png" , 90, 0, 10)

enemies = pygame.sprite.Group()
enemy1 = Enemy(player_size, player_speed-4, player_hp, (300, 400), player_down())
enemies.add(enemy1)

def draw_sprites():
    the_player.update()
    player_attacks.update()
    the_player.draw(screen)
    enemies.update()
    enemies.draw(screen)
    inv.update()
    inv.draw(screen)
    player_attacks.draw(screen)

def draw_shop():
    global ITEM_1_BOUGHT
    global ITEM_2_BOUGHT
    global ITEM_3_BOUGHT
    shop_screen = pygame.display.set_mode((900, 500))
    pygame.display.set_caption('Buy Menu')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

        shop_screen.fill(BLACK)
        if not ITEM_1_BOUGHT:
            shop_screen.blit(num_1, num_1_rect)
        if not ITEM_2_BOUGHT:
            shop_screen.blit(num_2, num_2_rect)
        if not ITEM_3_BOUGHT:
            shop_screen.blit(num_3, num_3_rect)
        shop_items.update()
        shop_items.draw(shop_screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            ITEM_1_BOUGHT = True
            inv.add(raba)
            shop_items.remove(item_1)
        elif keys[pygame.K_2]:
            ITEM_2_BOUGHT = True
            inv.add(stormsurge)
            shop_items.remove(item_2)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('DIMENSION OF THE DERANGED DEITY')
    screen.blit(bg, (0,0))
    pygame.display.flip()

def draw_loss_screen():
    loss_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('You lose trashy')

    screenL2.update()
    screenL2.draw(loss_screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
def draw_win_screen():
    win_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('You win lololololololololololol')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screenW2.update()
        screenW2.draw(win_screen)
        pygame.display.flip()

def draw_start_screen():
    start_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('why play, press enter to start')

    screenS2.update()
    screenS2.draw(start_screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('DIMENSION OF THE DERANGED DEITY')
    screen.blit(bg, (0,0))
    pygame.display.flip()

draw_start_screen()

running = True
# Main game loop
while running:
    #update enemies location of player
    enemy_ping(enemies, player.getX(), player.getY())
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                draw_shop()

    # Clear the screen
    screen.blit(bg, (0,0))
    
    if(not time_halted[0]):
        # Handle player input
        handle_movement(player)
        #Handle player attack
        player_attack(player, player_attacks, time_halted)
    else: 
        check_halt(time_halted)

    # Draw the square
    draw_sprites()

    #check if touching only if user has not quit
    if running:
        running = handle_player_collision(player, enemies)
        if not running:
            draw_loss_screen()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()