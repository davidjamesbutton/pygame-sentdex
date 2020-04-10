import pygame

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

def game_loop():
    x = 0.5 * (DISPLAY_WIDTH - car_img.get_width())
    y = DISPLAY_HEIGHT - 1.5 * car_img.get_height()

    game_running = True

    while game_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            # print(event)

        keys = pygame.key.get_pressed()

        x_change = 0

        if keys[pygame.K_LEFT]:
            x_change -= X_SPEED
        if keys[pygame.K_RIGHT]:
            x_change += X_SPEED

        x += x_change

        if x + car_img.get_width() > DISPLAY_WIDTH or x < 0:
            game_running = False

        game_display.fill(COLOUR_WHITE)
        car(x, y)

        pygame.display.update()

        clock.tick(FPS)

game_loop()
pygame.quit()
quit()