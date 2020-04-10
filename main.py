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
CAR_X_SPEED = 5

pygame.init()

pygame.display.set_caption(DISPLAY_CAPTION)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

clock = pygame.time.Clock()

car_img = pygame.image.load('racecar.png')

def draw_block(left, top, width, height):
    pygame.draw.rect(game_display, COLOUR_BLACK, [left, top, width, height])

def draw_car(left, top):
    game_display.blit(car_img, (left, top))

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
    car_pos_left = 0.5 * (DISPLAY_WIDTH - car_img.get_width())
    car_pos_top = DISPLAY_HEIGHT - 1.5 * car_img.get_height()

    block_width = 100
    block_height = 100
    block_pos_left = random.randrange(0, DISPLAY_WIDTH - block_width)
    block_pos_top = -3 * block_height
    block_speed = 7

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

        car_pos_left += car_x_change

        if car_pos_left + car_img.get_width() > DISPLAY_WIDTH or car_pos_left < 0:
            crash()

        block_pos_top += block_speed

        if block_pos_top > DISPLAY_HEIGHT:
            block_pos_top = 0 - block_height
            block_pos_left = random.randrange(0, DISPLAY_WIDTH - block_width)

        ### DRAW GAME STATE

        game_display.fill(COLOUR_WHITE)
        draw_car(car_pos_left, car_pos_top)
        draw_block(block_pos_left, block_pos_top, block_width, block_height)

        pygame.display.update()

        clock.tick(FPS)

game_loop()