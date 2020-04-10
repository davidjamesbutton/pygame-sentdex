import pygame

DISPLAY_CAPTION = 'A bit Racey'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)

pygame.init()

pygame.display.set_caption(DISPLAY_CAPTION)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
car_img = pygame.image.load('racecar.png')

def car(x, y):
    game_display.blit(car_img, (x, y))

x = 0.5 * (DISPLAY_WIDTH - car_img.get_width())
y = DISPLAY_HEIGHT - 1.5 * car_img.get_height()

clock = pygame.time.Clock()
crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        #print(event)

    game_display.fill(COLOUR_WHITE)
    car(x, y)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()