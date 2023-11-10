import pygame
import os
import random
import sys

# pygame initialisation
pygame.init()

# icon and header setup
pygame.display.set_caption('RunLah')
img = pygame.image.load(os.path.join("RunLahGame/Assets", "runlahicon.png"))
pygame.display.set_icon(img)

# set screen width and height; requirement for height: >= 600px
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w - 100
SCREEN_HEIGHT = info.current_h - 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load all assets
STARTSCREEN = pygame.image.load(os.path.join("RunLahGame/Assets/BG", "StartScreen.png"))

BG = pygame.image.load(os.path.join("RunLahGame/Assets/BG", "HauntedCastle.png"))

RUNNING = [pygame.image.load(os.path.join("RunLahGame/Assets/Lah", "LahRun1.png")),
           pygame.image.load(os.path.join("RunLahGame/Assets/Lah", "LahRun2.png"))]

JUMPING = pygame.image.load(os.path.join("RunLahGame/Assets/Lah", "LahJump.png"))

DUCKING = [pygame.image.load(os.path.join("RunLahGame/Assets/Lah", "LahDuck1.png")),
           pygame.image.load(os.path.join("RunLahGame/Assets/Lah", "LahDuck2.png"))]

GHOSTS = [pygame.image.load(os.path.join("RunLahGame/Assets/Ghosts", "Ghosts1.png")),
          pygame.image.load(os.path.join("RunLahGame/Assets/Ghosts", "Ghosts2.png")),
          pygame.image.load(os.path.join("RunLahGame/Assets/Ghosts", "Ghosts3.png"))]

BAT = [pygame.image.load(os.path.join("RunLahGame/Assets/Bat", "Bat1.png")),
       pygame.image.load(os.path.join("RunLahGame/Assets/Bat", "Bat2.png"))]

ENDSCREEN = pygame.image.load(os.path.join("RunLahGame/Assets/BG", "EndScreen.png"))

# player Lah class
class Lah:
    X_POS = 80
    Y_POS = 420 
    Y_POS_DUCK = 440 
    JUMP_VEL = 10 

    def __init__(self):
        self.run_img = RUNNING
        self.lah_run = True

        self.duck_img = DUCKING
        self.lah_duck = False

        self.jump_img = JUMPING
        self.lah_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.lah_rect = self.image.get_rect()
        self.lah_rect.x = self.X_POS
        self.lah_rect.y = self.Y_POS

    def update(self, userInput):
        if self.lah_duck:
            self.duck()
        if self.lah_run:
            self.run()
        if self.lah_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_SPACE] and not self.lah_jump:
            self.lah_duck = False
            self.lah_run = False
            self.lah_jump = True
        elif userInput[pygame.K_DOWN] and not self.lah_jump:
            self.lah_duck = True
            self.lah_run = False
            self.lah_jump = False
        elif not (self.lah_jump or userInput[pygame.K_DOWN]):
            self.lah_duck = False
            self.lah_run = True
            self.lah_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.lah_rect = self.image.get_rect()
        self.lah_rect.x = self.X_POS
        self.lah_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.lah_rect = self.image.get_rect()
        self.lah_rect.x = self.X_POS
        self.lah_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.lah_jump:
            self.lah_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.lah_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.lah_rect.x, self.lah_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Ghosts(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 360


class Bat(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 380
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def scale_image(image, target_width, target_height):
    image_width, image_height = image.get_size()
    width_ratio = target_width / image_width
    height_ratio = target_height / image_height
    min_ratio = min(width_ratio, height_ratio)
    new_width = int(image_width * min_ratio)
    new_height = int(image_height * min_ratio)
    return pygame.transform.scale(image, (new_width, new_height))


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Lah()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, 50)
        SCREEN.blit(text, textRect)

    # need the long width for running background for better game play
    # and to ensure characters are positioned correctly
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG, (x_pos_bg, 0))
        SCREEN.blit(BG, (image_width + x_pos_bg, 0))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, 0))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(Ghosts(GHOSTS))
            elif random.randint(0, 1) == 1:
                obstacles.append(Bat(BAT))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.lah_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        score()

        clock.tick(30)
        pygame.display.update()

        check_exit = pygame.key.get_pressed()
        if check_exit[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def menu(death_count):
    global points
    run = True

    # startscreen and endscreen height and width dynamically set
    def startscreen():
        # x_pos_bg = 0
        # image_width = STARTSCREEN.get_width()
        # SCREEN.blit(STARTSCREEN, (x_pos_bg, 0))
        # SCREEN.blit(STARTSCREEN, (image_width + x_pos_bg, 0))
        # if x_pos_bg <= -image_width:
        #     SCREEN.blit(STARTSCREEN, (image_width + x_pos_bg, 0))
        #     x_pos_bg = 0
        scaled_image = scale_image(STARTSCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
        x_pos_bg = (SCREEN_WIDTH - scaled_image.get_width()) // 2
        y_pos_bg = (SCREEN_HEIGHT - scaled_image.get_height()) // 2
        SCREEN.blit(scaled_image, (x_pos_bg, y_pos_bg))

    def endscreen():
        # x_pos_bg = 0
        # image_width = ENDSCREEN.get_width()
        # SCREEN.blit(ENDSCREEN, (x_pos_bg, 0))
        # SCREEN.blit(ENDSCREEN, (image_width + x_pos_bg, 0))
        # if x_pos_bg <= -image_width:
        #     SCREEN.blit(ENDSCREEN, (image_width + x_pos_bg, 0))
        #     x_pos_bg = 0
        scaled_image = scale_image(ENDSCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
        x_pos_bg = (SCREEN_WIDTH - scaled_image.get_width()) // 2
        y_pos_bg = (SCREEN_HEIGHT - scaled_image.get_height()) // 2
        SCREEN.blit(scaled_image, (x_pos_bg, y_pos_bg))


    while run:
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            startscreen()
        elif death_count > 0:
            endscreen()
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Your Score: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)