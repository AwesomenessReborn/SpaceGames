import pygame
import random
from ships.player_ship import Player

DEBUG = False

def player_processes(player_list, screen):
    for player in player_list:
        player.player_health_display(screen)
        player.player_power_display(screen)
        player.player_engine_rpm_display(screen)
        player.destroyed_check()

pygame.init()

def main():
    """
    Main
    """

    #introduction 
    print('Welcome to Spacegames')

    player1 = Player(input("Player 1, please enter your ship name : "), 200, 50, 22, 90, 100) # left player
    player2 = Player(input("Player 2, please enter your ship name : "), 1000, 640, 34, 102, 5) # Right player

    p1Ship = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('images/spaceplane.png'), 90), (125, 125))
    p2Ship = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('images/spaceplane.png'), -90), (125, 125))

    p1bullet = pygame.transform.scale(pygame.image.load('images/u3Mh2UU.png'), (21, 14))
    p2bullet = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('images/u3Mh2UU.png'), (21, 14)), 180)

    background = pygame.image.load('images/Background.jpg')

    # starting up the window. 
    screen = pygame.display.set_mode([1200,600])
    clock = pygame.time.Clock()
    screen.fill((0,15,90))

    # Game Loop: ----------------------------------------
    done = False
    while not done:
        player1.reload_main_arnament()
        player2.reload_main_arnament()

        # Ship Movement. 
        player1.movement(pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d)
        player2.movement(pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)

        # Update Game Screen. 
        screen.blit(background, [0,0])
        screen.blit(p2Ship, player2.return_position())
        screen.blit(p1Ship, player1.return_position())

        # health, power and engine rpm display. 
        player_processes([player1, player2], screen)

        player1.primary_weapon_functionality(pygame.K_q, 10, p1bullet, screen)
        player2.primary_weapon_functionality(pygame.K_SPACE, -10, p2bullet, screen)

        player1.bullet_hitting_mechansim(player2, DEBUG)
        player2.bullet_hitting_mechansim(player1, DEBUG)

        # DEBUG MECHANICS ------------------------
        player1.show_player_borders(DEBUG, screen)
        player2.show_player_borders(DEBUG, screen)

        if player1.destroyed == True:
            done = True
            print(player2.name + ' has destroyed ' + player1.name)
            print(player2.name + ' wins!!!')
        elif player2.destroyed == True:
            done = True
            print(player1.name + ' has destroyed ' + player2.name)
            print(player1.name + ' wins!!!')

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()

if __name__ == "__main__":
    main()