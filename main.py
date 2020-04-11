import pygame
import random


# Constants
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
FONT_NAME = 'comicsansms'
FPS = 60


pygame.init()

# Load resources from disk
image_car = pygame.image.load('assets/race_car.png')
font_small = pygame.font.SysFont(FONT_NAME, 25)
font_large = pygame.font.SysFont(FONT_NAME, 115)
sound_crash = pygame.mixer.Sound('assets/crash_sfx.wav')
pygame.mixer.music.load('assets/background_music.wav')
pygame.mixer.music.set_volume(0.5)


# Setup window
pygame.display.set_caption(DISPLAY_CAPTION)

display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

icon_car = pygame.transform.scale(image_car, (32, 32))
pygame.display.set_icon(icon_car)

clock = pygame.time.Clock()


def draw_background_colour(colour):
    display_surface.fill(colour)

def draw_blue_block(block_rect):
    pygame.draw.rect(display_surface, COLOUR_BLUE, block_rect)

def draw_car(car_rect):
    display_surface.blit(image_car, car_rect)

def draw_score(count):
    text_surface = font_small.render(f'Score: {count}', True, COLOUR_BLACK)
    display_surface.blit(text_surface, (0, 0))

def draw_large_message(text):
    text_surface = font_large.render(text, True, COLOUR_BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    display_surface.blit(text_surface, text_rect)

def draw_button(text_surface, button_rect, colour, hover_colour, action=None):
    mouse_pos = pygame.mouse.get_pos()

    # Button was clicked
    if left_button_is_pressed() and button_rect.collidepoint(mouse_pos):
        if action is not None:
            action()

    button_colour = colour
    # Mouse hovered button
    if button_rect.collidepoint(mouse_pos):
        button_colour = hover_colour
    pygame.draw.rect(display_surface, button_colour, button_rect)

    text_rect = text_surface.get_rect()
    text_rect.center = button_rect.center
    display_surface.blit(text_surface, text_rect)

def left_button_is_pressed():
    return pygame.mouse.get_pressed()[0] == 1

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def play_music():
    pygame.mixer.music.play(-1)

def game_quit():
    pygame.quit()
    quit()

def pause_scene():
    pause_music()

    paused = True

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        draw_background_colour(COLOUR_WHITE)
        draw_large_message("Paused")

        pygame.display.update()
        clock.tick(FPS)

    resume_music()

def crash_scene():
    stop_music()
    pygame.mixer.Sound.play(sound_crash)

    button_width = 100
    button_height = 50

    play_again_button_rect = pygame.Rect(150, 450, button_width, button_height)
    play_again_button_surface = font_small.render('Play again', True, COLOUR_BLACK)

    exit_button_rect = pygame.Rect(550, 450, button_width, button_height)
    exit_button_surface = font_small.render('Exit', True, COLOUR_BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        draw_large_message('You crashed!')

        draw_button(play_again_button_surface, play_again_button_rect, COLOUR_DARK_GREEN, COLOUR_GREEN, driving_scene)
        draw_button(exit_button_surface, exit_button_rect, COLOUR_DARK_RED, COLOUR_RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)

def menu_scene():
    button_width = 100
    button_height = 50

    start_button_rect = pygame.Rect(150, 450, button_width, button_height)
    start_button_text_surface = font_small.render('Start', True, COLOUR_BLACK)

    exit_button_rect = pygame.Rect(550, 450, button_width, button_height)
    exit_button_text_surface = font_small.render('Exit', True, COLOUR_BLACK)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        draw_background_colour(COLOUR_WHITE)
        draw_large_message(DISPLAY_CAPTION)

        draw_button(start_button_text_surface, start_button_rect, COLOUR_DARK_GREEN, COLOUR_GREEN, driving_scene)
        draw_button(exit_button_text_surface, exit_button_rect, COLOUR_DARK_RED, COLOUR_RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)

def driving_scene():
    play_music()

    car_rect = image_car.get_rect()
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

        draw_background_colour(COLOUR_WHITE)
        draw_car(car_rect)
        draw_blue_block(block_rect)
        draw_score(score)

        pygame.display.update()

        clock.tick(FPS)

if __name__ == '__main__':
    menu_scene()