import pygame
import time
import threading

DISPLAY_CAPTION = 'A bit Racey'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 60
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
X_SPEED = 5

pygame.init()

pygame.display.set_caption(DISPLAY_CAPTION)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

clock = pygame.time.Clock()

car_img = pygame.image.load('racecar.png')

def car(x, y):
    game_display.blit(car_img, (x, y))

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
    x = 0.5 * (DISPLAY_WIDTH - car_img.get_width())
    y = DISPLAY_HEIGHT - 1.5 * car_img.get_height()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # print(event)

        keys = pygame.key.get_pressed()

        x_change = 0

        if keys[pygame.K_LEFT]:
            x_change -= X_SPEED
        if keys[pygame.K_RIGHT]:
            x_change += X_SPEED

        x += x_change

        if x + car_img.get_width() > DISPLAY_WIDTH or x < 0:
            crash()

        game_display.fill(COLOUR_WHITE)
        car(x, y)

        pygame.display.update()

        clock.tick(FPS)

game_loop()