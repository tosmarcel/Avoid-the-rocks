import pygame
import random
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
playerImg = pygame.image.load("player.png")
fireballImg = pygame.image.load("fireball.png")

class Player(object):
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    speed_bonus = 0
    width = 40
    height = 40

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.x_speed > 0:
            self.x_speed += self.speed_bonus
        elif self.x_speed < 0:
            self.x_speed -= self.speed_bonus

        if self.y_speed > 0:
            self.y_speed += self.speed_bonus
        elif self.y_speed < 0:
            self.y_speed -= self.speed_bonus

        self.x += self.x_speed
        self.y += self.y_speed
        gameDisplay.blit(playerImg, (self.x, self.y))

    def left_bound(self):
        if self.x <= 0:
            self.x_speed = self.x_speed * -1
    def right_bound(self):
        if self.x > display_width - self.width:
            self.x_speed = self.x_speed * -1
    def top_bound(self):
        if self.y <= 0:
            self.y_speed = self.y_speed * -1
    def bottom_bound(self):
        if self.y >= display_height - self.height:
            self.y_speed = self.y_speed * -1

    def bound(self):
        self.left_bound()
        self.right_bound()
        self.top_bound()
        self.bottom_bound()

    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Fireball(object):
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    width = 40
    height = 40
    has_reached_limit = False #This will let us know if it can de-spawn
    side = 0

    def __init__(self):
        self.side = random.randint(1,4)
        # Where does the fireball spawn?
        # 1 - left
        # 2 - top
        # 3 - right
        # 4 - bottom

        if self.side == 1:
            self.x = -60 # get to the left of the window
            self.y = random.randint(0, display_height-self.height)
            self.x_speed = 10

        elif self.side == 2:
            self.x = random.randint(0, display_width-self.width)
            self.y = -60
            self.y_speed = 10

        elif self.side == 3:
            self.x = display_width + 60
            self.y = random.randint(0, display_height-self.height)
            self.x_speed = -10

        elif self.side == 4:
            self.x = random.randint(0, display_width-self.width)
            self.y = display_height + 60
            self.y_speed = -10

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        gameDisplay.blit(fireballImg, (self.x, self.y))
        if self.side == 1 and self.x > display_width:
            self.has_reached_limit = True
        if self.side == 2 and self.y > display_height:
            self.has_reached_limit = True
        if self.side == 3 and self.x < -40:
            self.has_reached_limit = True
        if self.side == 4 and self.y < -40:
            self.has_reached_limit = True

    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def game_loop():
    player = Player(display_width/2, display_height/2)
    fireballs = []
    difficulty = 1.0

    score = 0
    gameDisplay.fill((255,255,255))
    player.update()
    pygame.display.update()

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.x_speed = 2
                if event.key == pygame.K_LEFT:
                    player.x_speed = -2
                if event.key == pygame.K_DOWN:
                    player.y_speed = 2
                if event.key == pygame.K_UP:
                    player.y_speed = -2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.x_speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_speed = 0

        gameDisplay.fill((255,255,255))

        player.bound()
        player.update()

        if len(fireballs) < difficulty:
            fireballs.append(Fireball())

        fireball_index = 0
        for fireball in fireballs:
            fireball.update()

            if fireball.rectangle().colliderect(player.rectangle()):
                death_screen(score)

            if fireball.has_reached_limit:
                fireballs.pop(fireball_index)
                fireball_index -= 1
                score += 1
                difficulty += 0.1
                player.speed_bonus += 0.01
                print score
                print player.speed_bonus
        pygame.display.update()
        clock.tick(50)


def main_screen():
    gameDisplay.fill((0,0,0))
    text = pygame.font.Font('freesansbold.ttf', 60)
    text_on_screen = text.render("LET'S PLAY!", True, (255, 255, 255))
    text_rect = text_on_screen.get_rect()
    text_rect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(text_on_screen, text_rect)
    pygame.display.update()
    time.sleep(2)
    game_loop()
    
def death_screen(score):
    gameDisplay.fill((0,0,0))
    text = pygame.font.Font('freesansbold.ttf', 60)
    message = "U DEAD BRUH! Score: " + str(score)
    text_on_screen = text.render(message, True, (255, 255, 255))
    text_rect = text_on_screen.get_rect()
    text_rect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(text_on_screen, text_rect)
    pygame.display.update()
    time.sleep(2)
    main_screen()

main_screen()
