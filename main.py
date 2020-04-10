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
car_img = pygame.image.load('racecar.png')

def car(x, y):
    game_display.blit(car_img, (x, y))

x = 0.5 * (DISPLAY_WIDTH - car_img.get_width())
y = DISPLAY_HEIGHT - 1.5 * car_img.get_height()
x_change = 0

clock = pygame.time.Clock()
crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # TO DO: Fix car getting stuck when overlapping fast key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -X_SPEED
            if event.key == pygame.K_RIGHT:
                x_change = X_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

        # print(event)

    x += x_change

    game_display.fill(COLOUR_WHITE)
    car(x, y)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
quit()