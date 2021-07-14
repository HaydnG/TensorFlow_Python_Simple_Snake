# Simple pygame program

# Import and initialize the pygame library
import random

import pygame
pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
    K_KP_1,
    K_KP_4,
)

# Set up the drawing window
screen = pygame.display.set_mode([1280, 720])

food = [screen.get_width() / 2, screen.get_height() / 2]

class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height =height



p1 = player(100, 200, 10, 10)
# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.rect(screen, (0, 0, 255), (food[0], food[1], 40, 40))

    pygame.draw.rect(screen, (255,0, 255), (p1.x, p1.y, p1.width, p1.height))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        p1.y-=0.3

    if keys[pygame.K_a]:
        p1.x -=0.3

    if keys[pygame.K_d]:
        p1.x+=0.3

    if keys[pygame.K_s]:
        p1.y+=0.3

    if (p1.y + p1.height) > food[1] and p1.y < (food[1] + 40) \
            and (p1.x + p1.width) > food[0] and p1.x < (food[0] + 40):
        food[0] = random.randint(0, screen.get_width() - 40)
        food[1] = random.randint(0, screen.get_height() - 40)



    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()


#https://towardsdatascience.com/deep-reinforcement-learning-build-a-deep-q-network-dqn-to-play-cartpole-with-tensorflow-2-and-gym-8e105744b998