import pygame
import random

red = (255, 0, 0)
yellow = (255, 255, 0)

class Player:
    """
    Player Class: 
        The upper, lower, left and the right bound is used for the collision - that is, where the bullet hits if the player ship is hits. 
        The PRIMARY_WEAPON_COOLDOWN_TIMER allows for the bullets to have a pause between each shot. 

    """

    def __init__(self, player_name, posX, margin, left_bound, right_bound, adjustment):
        self.player_name = player_name
        self.health = 500
        self.BASE_BULLET_DAMAGE = 25 
        self.destroyed = False
        self.velocity = 0
        self.bullets = []
        self.power = 100
        self.margin = margin

        self.posX = posX
        self.posY = 400

        # For collisions: 
        self.UPPER_BOUND = 18
        self.LOWER_BOUND = 105
        self.LEFT_BOUND = left_bound
        self.RIGHT_BOUND = right_bound

        # For pause between each bullet shot. 
        self.PRIMARY_WEAPON_COOLDOWN_TIMER = 0

        # for primary weapon launch position. 
        self.HORIZONTAL_ADJUSTMENT_FOR_PRIMARY_WEAPON = adjustment
        self.VERTICAL_ADJUSTMENT_FOR_PRIMARY_WEAPON = 59


        self.PRIMARY_WEAPON_POWER_REQUIERMENT = 60

    def return_live_bound(self, side) -> int:
        if (side == "left"):
            return self.posX + self.LEFT_BOUND
        elif (side == "right"):
            return self.posX + self.RIGHT_BOUND
        elif (side == "up"): 
            return self.posY + self.UPPER_BOUND
        elif (side == "down"):
            return self.posY + self.LOWER_BOUND

    def destroyed_check(self):
        if self.health <= 0:
            self.destroyed = True

    def reload_main_arnament(self):
        if self.power < 500:
            self.power = self.power + 1
    
    def movement(self, UP, DOWN, LEFT, RIGHT):
        keys = pygame.key.get_pressed()
        if keys[UP] and self.posY < 560:
            self.posY = self.posY + self.engineSpeed()
        elif keys[DOWN] and self.posY > 100:
            self.posY = self.posY - self.engineSpeed()
        if keys[LEFT] and self.posX > 5:
            self.posX = self.posX - self.engineSpeed()
        elif keys[RIGHT] and self.posX < 1130:
            self.posX = self.posX + self.engineSpeed()
        
        if keys[UP] or keys[DOWN] or keys[LEFT] or keys[RIGHT]:
            pass
        elif self.velocity > 0:
            self.velocity = self.velocity - 1

    def return_position(self):
        return [self.posX, self.posY]

    def engineSpeed(self):
        if False:
            return 1
        else:
            if self.velocity < 15:
                self.velocity = self.velocity + 0.15
            if self.velocity <= 0:
                self.velocity = 0
            return self.velocity

    def player_health_display(self, screen):
        pygame.draw.rect(screen, (90, 90, 90), [self.margin, 30, 500, 20], 0)
        
        if self.health > 220:
            pygame.draw.rect(screen, (0, 255, 0), [self.margin, 30, (self.health), 20], 0)
        elif self.health > 100: 
            pygame.draw.rect(screen, (255, 187, 0), [self.margin, 30, (self.health), 20], 0)
        else: 
            pygame.draw.rect(screen, (200, 0, 0), [self.margin, 30, (self.health), 20], 0)

    def player_power_display(self, screen):
        pygame.draw.rect(screen, (125, 92, 0), [self.margin, 60, 500, 20], 0)
        if self.power > self.PRIMARY_WEAPON_POWER_REQUIERMENT:
            pygame.draw.rect(screen, (255, 150, 0), [self.margin, 60, (self.power), 20], 0)
        else:
            pygame.draw.rect(screen, (200, 100, 0), [self.margin, 60, (self.power), 20], 0)
    
    def player_engine_rpm_display(self, screen):
        pygame.draw.rect(screen, (20, 20, 20), [self.margin, 550, (self.velocity * 34), 20], 0)
        if self.velocity > 12:
            pygame.draw.rect(screen, (255, 0, 0), [self.margin, 550, (self.velocity * 34), 20], 0)
        elif self.velocity > 8:
            pygame.draw.rect(screen, (255, 128, 0), [self.margin, 550, (self.velocity * 34), 20], 0)
        else:
            pygame.draw.rect(screen, (0, 255, 0), [self.margin, 550, (self.velocity * 34), 20], 0)

    def show_player_borders(self, DEBUG, screen):
        if DEBUG:
            pygame.draw.line(screen, red, (0, self.posY + self.UPPER_BOUND), (1200, self.posY + self.UPPER_BOUND), 4)
            pygame.draw.line(screen, red, (0, self.posY + self.LOWER_BOUND), (1200, self.posY + self.LOWER_BOUND), 4)

            pygame.draw.line(screen, yellow, (self.posX + self.LEFT_BOUND, 0), (self.posX + self.LEFT_BOUND, 600), 4)
            pygame.draw.line(screen, yellow, (self.posX + self.RIGHT_BOUND, 0), (self.posX + self.RIGHT_BOUND, 600), 4)

    def primary_weapon_functionality(self, key, bullet_speed, pic, screen):
        # Make the bullets when key is pressed. 
        keys = pygame.key.get_pressed()

        if self.PRIMARY_WEAPON_COOLDOWN_TIMER <= 0 and keys[key] and self.power > self.PRIMARY_WEAPON_POWER_REQUIERMENT:
                self.power = self.power - self.PRIMARY_WEAPON_POWER_REQUIERMENT

                x = self.posX + self.HORIZONTAL_ADJUSTMENT_FOR_PRIMARY_WEAPON
                y = self.posY + self.VERTICAL_ADJUSTMENT_FOR_PRIMARY_WEAPON
                self.bullets.append([x, y])

                # Initiate weapon cooldown. 
                self.PRIMARY_WEAPON_COOLDOWN_TIMER = 20
        else:
            self.PRIMARY_WEAPON_COOLDOWN_TIMER = self.PRIMARY_WEAPON_COOLDOWN_TIMER - 2

        # Move the bullets. 
        for b in range(len(self.bullets)):
            try:
                self.bullets[b][0] = self.bullets[b][0] + bullet_speed
                if self.bullets[b][0] > 1200 or self.bullets[b][0] < 0:
                    self.bullets.pop(b)
            except IndexError:
                break

        # Show the Bullets. 
        for bullet in range(len(self.bullets)):
            screen.blit(pic, [self.bullets[bullet][0], self.bullets[bullet][1]])
    
    def bullet_hitting_mechansim(self, opponent, debug):
        for index, _ in enumerate(self.bullets):
            if self.bullets[index][0] > opponent.return_live_bound("left") and self.bullets[index][0] < opponent.return_live_bound("right") and self.bullets[index][1] > opponent.return_live_bound("up") and self.bullets[index][1] < opponent.return_live_bound("down"):
                if debug:
                    print("popping: [" + str(self.bullets[index][0]) + ", " + str(self.bullets[index][1]) + "] which hit player 2")
                    
                self.bullets.pop(index)
                opponent.health = opponent.health - 30