import time

import pygame
import random
import numpy as np
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

class Game:

    def __init__(self, time_end, user_input):

        self.draw_game = True

        self.user_input = user_input
        self.screen = pygame.display.set_mode([480, 480])

        self.observations = 8
        self.observation_shape = (1,8)
        self.actions = 4
        self.action_shape = (1,4)

        self.pwidth = 160
        self.pheight = self.pwidth

        self.wall_sensor = 1 * self.pwidth
        self.px = random.randint(0, ((self.screen.get_width() - self.pwidth) / self.pwidth) - 1) * self.pwidth
        self.py = random.randint(0, ((self.screen.get_height() - self.pwidth) / self.pwidth) - 1) * self.pwidth

        self.time_limit = 10
        self.time_end = time_end

        self.food_count = 0

        self.food = [0,0]
        self.food_size = 160
        self.no_food_border = 0
        self._move_food()
        self.distance = 0

        self.win = 10

        self.distance_reward = 0

        self.last_action = [0,0,0,0]
        self.running = True
        self.game_over = False
        self.last_pickup = time.time()
        self.elapsed = 0

        self.steps = 0
        self.max_steps = 50
        self.steps_left = 0


    def step(self, action):
        self.last_action = action
        self.steps += 1
        self.steps_left = self.max_steps - self.steps

        if self.steps >= self.max_steps and self.time_end == True:
             return self._end_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.draw_game = not self.draw_game
                    print(self.draw_game)

        if self.user_input:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.py -= 1
            if keys[pygame.K_s]:
                self.py += 1

            if keys[pygame.K_a]:
                self.px -= 1

            if keys[pygame.K_d]:
                self.px += 1

        if action[0] == 1:
            self.py += self.pwidth
        if action[1] == 1:
            self.py -= self.pwidth

        if action[2] == 1:
            self.px += self.pwidth

        if action[3] == 1:
            self.px -= self.pwidth


        if self.draw_game:
            self._draw_frame()

        if (self.py < 0) or ((self.py + self.pheight) > self.screen.get_height()) or (self.px < 0) \
                or ((self.px + self.pwidth) > self.screen.get_width()):
            return self._end_game()

        #self.distance = (((((self.px + (self.pwidth/2)) - (self.food[0] + self.food_size/2) )**2) + (((self.py + (self.pheight/2))-(self.food[1] + self.food_size/2))**2) )**0.5)
        #self.distance_reward = 5 - ((self.distance / 1000) * 5)

        if self._check_collision():
            return self.get_state(), 3, False, self.food_count

        return self.get_state(), 1, False, self.food_count

    def _end_game(self):
        self.running = False
        self.game_over = True

        return self.get_state(), -3, True, self.food_count

    def _check_collision(self):

        if self.py == self.food[1] and self.px == self.food[0]:
            self._food_pickup()
            return True
        return False

    def _food_pickup(self):
        self.steps = 0
        self.food_count +=1
        self._move_food()

    def _move_food(self):
        self.food[0] = random.randint(0, ((self.screen.get_width() - self.food_size) / self.food_size)) * self.food_size
        self.food[1] = random.randint(0, ((self.screen.get_height() - self.food_size) / self.food_size)) * self.food_size

    def _draw_frame(self):
        self.screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.rect(self.screen, (0, 0, 255), (self.food[0], self.food[1], self.food_size, self.food_size))

        pygame.draw.rect(self.screen, (255, 0, 255), (self.px, self.py, self.pwidth, self.pheight))

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        myfont = pygame.font.SysFont('Segoe UI', 50)
        food_count_text = myfont.render(str(self.food_count), True, (255, 0, 255))
        elapsed_text = myfont.render(str(int(self.steps_left)), True, (255, 0, 255))
        self.screen.blit(food_count_text, (20, 10))
        self.screen.blit(elapsed_text, (self.screen.get_width() - elapsed_text.get_width() - 20, 10))
        pygame.display.update()

    def get_state(self):

        isWallLeft = (True if self.px - 1 <= 0 else False)
        isWallRight = (True if (self.px + self.pwidth + 1) >= self.screen.get_width() else False)
        isWallUp = (True if self.py - 1 <= 0 else False)
        isWallDown = (True if (self.py + self.pheight + 1) >= self.screen.get_height() else False)

        state = [(self.food[0] ) < (self.px ),  # food left
                 (self.food[0] ) > (self.px ),  # food right
                 (self.food[1] ) < (self.py ),  # food up
                 (self.food[1] ) > (self.py ),
                 isWallLeft,
                 isWallRight,
                 isWallUp,
                 isWallDown]

        return np.array(state, dtype=int)

    def reset(self):
        self.px = random.randint(0, ((self.screen.get_width() - self.pwidth) / self.pwidth)) * self.pwidth
        self.py = random.randint(0, ((self.screen.get_height() - self.pwidth) / self.pwidth)) * self.pwidth
        self.running = True
        self.last_pickup = time.time()
        self.elapsed = 0
        self.food_count = 0
        self._move_food()
        self.steps = 0

    def quit(self):
        self.running = False
        pygame.quit()
