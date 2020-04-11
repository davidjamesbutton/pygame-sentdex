import pygame
import random

pygame.init()

CAR_X_SPEED = 5
COLOUR_BLACK = (0, 0, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_DARK_GREEN = (0, 200, 0)
COLOUR_DARK_RED = (200, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)
COLOUR_WHITE = (255, 255, 255)
DISPLAY_CAPTION = 'A bit Racey'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FONT_INTRO_BUTTONS = pygame.font.SysFont('comicsansms', 20)
FONT_LARGE_MESSAGE = pygame.font.SysFont('comicsansms', 115)
FONT_SCORE = pygame.font.SysFont('comicsansms', 25)
FPS = 60

pygame.display.set_caption(DISPLAY_CAPTION)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

clock = pygame.time.Clock()

car_img = pygame.image.load('racecar.png')

def draw_background(colour):
    game_display.fill(colour)

def draw_block(block_rect):
    pygame.draw.rect(game_display, COLOUR_BLUE, block_rect)

def draw_car(car_rect):
    game_display.blit(car_img, car_rect)

def draw_score(count):
    text = FONT_SCORE.render(f'Score: {count}', True, COLOUR_BLACK)
    game_display.blit(text, (0, 0))

def draw_large_message(text):
    text_surface = FONT_LARGE_MESSAGE.render(text, True, COLOUR_BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    game_display.blit(text_surface, text_rect)

def draw_button(text_surf, button_rect, colour, hover_colour, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Button was clicked
    if mouse_pressed[0] == 1 and button_rect.collidepoint(mouse_pos):
        if action is not None:
            action()

    button_colour = colour
    # Mouse hovered button
    if button_rect.collidepoint(mouse_pos):
        button_colour = hover_colour
    pygame.draw.rect(game_display, button_colour, button_rect)

    text_rect = text_surf.get_rect()
    text_rect.center = button_rect.center
    game_display.blit(text_surf, text_rect)

def game_quit():
    pygame.quit()
    quit()

def pause_scene():
    paused = True
    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        draw_background(COLOUR_WHITE)
        draw_large_message("Paused")

        pygame.display.update()
        clock.tick(FPS)

def crash_scene():
    button_width = 100
    button_height = 50
    button1_rect = pygame.Rect(150, 450, button_width, button_height)
    button2_rect = pygame.Rect(550, 450, button_width, button_height)

    button1_text_surface = FONT_INTRO_BUTTONS.render('Play again', True, COLOUR_BLACK)
    button2_text_surface = FONT_INTRO_BUTTONS.render('Exit', True, COLOUR_BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        draw_large_message('You crashed!')
        draw_button(button1_text_surface, button1_rect, COLOUR_DARK_GREEN, COLOUR_GREEN, driving_scene)
        draw_button(button2_text_surface, button2_rect, COLOUR_DARK_RED, COLOUR_RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)

def menu_scene():
    button_width = 100
    button_height = 50
    button1_rect = pygame.Rect(150, 450, button_width, button_height)
    button2_rect = pygame.Rect(550, 450, button_width, button_height)

    button1_text_surface = FONT_INTRO_BUTTONS.render('Start', True, COLOUR_BLACK)
    button2_text_surface = FONT_INTRO_BUTTONS.render('Exit', True, COLOUR_BLACK)

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        draw_background(COLOUR_WHITE)
        draw_large_message(DISPLAY_CAPTION)

        draw_button(button1_text_surface, button1_rect, COLOUR_DARK_GREEN, COLOUR_GREEN, driving_scene)
        draw_button(button2_text_surface, button2_rect, COLOUR_DARK_RED, COLOUR_RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)


def driving_scene():
    car_rect = car_img.get_rect()
    car_rect.top = DISPLAY_HEIGHT - 1.5 * car_rect.height
    car_rect.centerx = DISPLAY_WIDTH / 2

    block_width = 100
    block_height = 100
    block_pos_left = random.randrange(0, DISPLAY_WIDTH - block_width)
    block_pos_top = -3 * block_height
    block_rect = pygame.Rect(block_pos_left, block_pos_top, block_width, block_height)
    block_speed = 4

    score = 0

    while True:

        ### HANDLE INPUT EVENTS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_scene()

        keys = pygame.key.get_pressed()

        car_x_change = 0

        if keys[pygame.K_LEFT]:
            car_x_change -= CAR_X_SPEED
        if keys[pygame.K_RIGHT]:
            car_x_change += CAR_X_SPEED

        ### UPDATE GAME STATE

        car_rect.move_ip(car_x_change, 0)

        block_rect.move_ip(0, block_speed)

        # Car outside display
        if car_rect.right > DISPLAY_WIDTH:
            car_rect.right = DISPLAY_WIDTH
        if car_rect.left <  0:
            car_rect.left = 0

        # Block below display
        if block_rect.top > DISPLAY_HEIGHT:
            # Increment score
            score += 1
            # Increase difficulty
            block_speed += 0.3
            block_rect.inflate_ip(5, 0)
            # Reset block
            block_rect.top = 0 - block_height
            block_rect.left = random.randrange(0, DISPLAY_WIDTH - block_rect.width)

        # Car and block collide
        if car_rect.colliderect(block_rect):
            crash_scene()

        ### DRAW GAME STATE

        draw_background(COLOUR_WHITE)
        draw_car(car_rect)
        draw_block(block_rect)
        draw_score(score)

        pygame.display.update()

        clock.tick(FPS)

menu_scene()