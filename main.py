import pygame
import random
import time
import threading

DISPLAY_CAPTION = 'A bit Racey'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 60
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLUE = (0, 0, 255)
CAR_X_SPEED = 5

pygame.init()

pygame.display.set_caption(DISPLAY_CAPTION)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

clock = pygame.time.Clock()

car_img = pygame.image.load('racecar.png')

def draw_block(block_rect):
    pygame.draw.rect(game_display, COLOUR_BLUE, block_rect)

def draw_car(car_rect):
    game_display.blit(car_img, car_rect)

def draw_blocks_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render(f'Dodged: {count}', True, COLOUR_BLACK)
    game_display.blit(text, (0, 0))

def crash():
    message_display('You Crashed')

def run_sync(func):
    thread = threading.Thread(target=func)
    thread.start()
    thread.join()

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    game_display.blit(text_surf, text_rect)

    # Run synchronously to ensure display has updated before pausing
    # https://stackoverflow.com/questions/55881619/sleep-doesnt-work-where-it-is-desired-to/55882173
    run_sync(lambda: pygame.display.update())

    time.sleep(2)
    game_loop()

def text_objects(text, font):
    text_surface = font.render(text, True, COLOUR_BLACK)
    return text_surface, text_surface.get_rect()

def game_loop():
    car_rect = car_img.get_rect()
    car_rect.top = DISPLAY_HEIGHT - 1.5 * car_rect.height
    car_rect.centerx = DISPLAY_WIDTH / 2

    block_width = 100
    block_height = 100
    block_pos_left = random.randrange(0, DISPLAY_WIDTH - block_width)
    block_pos_top = -3 * block_height
    block_rect = pygame.Rect(block_pos_left, block_pos_top, block_width, block_height)
    block_speed = 4

    dodged = 0

    while True:

        ### HANDLE INPUT EVENTS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # print(event)

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
        if car_rect.right > DISPLAY_WIDTH or car_rect.left < 0:
            crash()

        # Block below display
        if block_rect.top > DISPLAY_HEIGHT:
            # Increment score
            dodged += 1
            # Increase difficulty
            block_speed += 0.3
            block_rect.inflate_ip(5, 0)
            # Reset block
            block_rect.top = 0 - block_height
            block_rect.left = random.randrange(0, DISPLAY_WIDTH - block_rect.width)

        # Car and block collide
        if car_rect.colliderect(block_rect):
            crash()

        ### DRAW GAME STATE

        game_display.fill(COLOUR_WHITE)
        draw_car(car_rect)
        draw_block(block_rect)
        draw_blocks_dodged(dodged)

        pygame.display.update()

        clock.tick(FPS)

game_loop()