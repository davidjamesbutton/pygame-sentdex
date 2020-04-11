import colour
import music
import pygame
import random


# Constants
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
CAR_X_SPEED = 5
DISPLAY_CAPTION = 'A bit Racey'
DISPLAY_HEIGHT = 600
DISPLAY_WIDTH = 800
FONT_NAME = 'comicsansms'
FPS = 60


pygame.init()

# Load resources from disk
image_car = pygame.image.load('assets/race_car.png')
font_small = pygame.font.SysFont(FONT_NAME, 25)
font_large = pygame.font.SysFont(FONT_NAME, 115)
sound_crash = pygame.mixer.Sound('assets/crash_sfx.wav')
music.load('assets/background_music.wav')


# Setup window
pygame.display.set_caption(DISPLAY_CAPTION)

display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

icon_car = pygame.transform.scale(image_car, (32, 32))
pygame.display.set_icon(icon_car)

clock = pygame.time.Clock()


def draw_background_colour(background_colour):
    display_surface.fill(background_colour)

def draw_blue_block(block_rect):
    pygame.draw.rect(display_surface, colour.BLUE, block_rect)

def draw_car(car_rect):
    display_surface.blit(image_car, car_rect)

def draw_text_with_center(text, font, center):
    text_surface = font.render(text, True, colour.BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = center
    display_surface.blit(text_surface, text_rect)

def draw_text_with_upperleft(text, font, upper_left):
    text_surface = font.render(text, True, colour.BLACK)
    display_surface.blit(text_surface, upper_left)

def draw_score(count):
    draw_text_with_upperleft(f'Score: {count}', font_small, (0, 0))

def draw_large_centered_msg(text):
    center_pos = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    draw_text_with_center(text, font_large, center_pos)

def draw_button(text, button_rect, default_colour, hover_colour, action=None):
    mouse_pos = pygame.mouse.get_pos()

    # Button was clicked
    if left_button_is_pressed() and button_rect.collidepoint(mouse_pos):
        if action is not None:
            action()

    button_colour = default_colour
    # Mouse hovered button
    if button_rect.collidepoint(mouse_pos):
        button_colour = hover_colour
    pygame.draw.rect(display_surface, button_colour, button_rect)

    draw_text_with_center(text, font_small, button_rect.center)

def left_button_is_pressed():
    return pygame.mouse.get_pressed()[0] == 1

def game_quit():
    pygame.quit()
    quit()

def pause_scene():
    music.pause()

    paused = True

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        draw_background_colour(colour.WHITE)
        draw_large_centered_msg("Paused")

        pygame.display.update()
        clock.tick(FPS)

    music.resume()

def crash_scene():
    music.stop()
    pygame.mixer.Sound.play(sound_crash)

    play_again_button_rect = pygame.Rect(150, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(550, 450, BUTTON_WIDTH, BUTTON_HEIGHT)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        draw_large_centered_msg('You crashed!')

        draw_button('Play again', play_again_button_rect, colour.DARK_GREEN, colour.GREEN, driving_scene)
        draw_button('Exit', exit_button_rect, colour.DARK_RED, colour.RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)

def menu_scene():
    start_button_rect = pygame.Rect(150, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(550, 450, BUTTON_WIDTH, BUTTON_HEIGHT)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        draw_background_colour(colour.WHITE)
        draw_large_centered_msg(DISPLAY_CAPTION)

        draw_button('Start', start_button_rect, colour.DARK_GREEN, colour.GREEN, driving_scene)
        draw_button('Exit', exit_button_rect, colour.DARK_RED, colour.RED, game_quit)

        pygame.display.update()
        clock.tick(FPS)

def driving_scene():
    music.play()

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

        draw_background_colour(colour.WHITE)
        draw_car(car_rect)
        draw_blue_block(block_rect)
        draw_score(score)

        pygame.display.update()

        clock.tick(FPS)

if __name__ == '__main__':
    menu_scene()