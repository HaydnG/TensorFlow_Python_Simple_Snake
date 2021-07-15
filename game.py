import time

import pygame
import random
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

    def __init__(self):
        self.px = 100
        self.py = 200
        self.pwidth = 10
        self.pheight = 10

        self.food_count = 0

        self.screen = pygame.display.set_mode([1280, 720])
        self.food = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        self.food_size = 40

        self.running = True
        self.last_pickup = time.time()
        self.elapsed = 0


    def play_step(self, action):
        self.elapsed = time.time() - self.last_pickup

        game_over = False
        reward = 0

        if self.elapsed > 20:
            self.running = False
            game_over = True
            reward = -10
            return reward, game_over, self.food_count

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or action[0] == 1:
            self.py -= 0.5
        if keys[pygame.K_s] or action[1] == 1:
            self.py += 0.5

        if keys[pygame.K_a] or action[2] == 1:
            self.px -= 0.5

        if keys[pygame.K_d] or action[3] == 1:
            self.px += 0.5


        if self._check_collision():
            reward += 10

        distance = ((((self.px - self.food[0] )**2) + ((self.py-self.food[1])**2) )**0.5)
        distance_reward = 5 - ((distance / 700) * 5)
        time_reward = 4 - ((self.elapsed / 4) * 2)



        # Flip the display
        pygame.display.flip()
        self._draw_frame()

        final_reward = reward + distance_reward + time_reward
        print(final_reward)

        return final_reward, self.food_count

    def _check_collision(self):
        if (self.py + self.pheight) > self.food[1] and self.py < (self.food[1] + self.food_size) \
                and (self.px + self.pwidth) > self.food[0] and self.px < (self.food[0] + self.food_size):
            self._food_pickup()
            return True
        return False

    def _food_pickup(self):
        self.food[0] = random.randint(0, self.screen.get_width() - self.food_size)
        self.food[1] = random.randint(0, self.screen.get_height() - self.food_size)

        self.food_count +=1
        self.last_pickup = time.time()

    def _draw_frame(self):
        self.screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.rect(self.screen, (0, 0, 255), (self.food[0], self.food[1], self.food_size, self.food_size))

        pygame.draw.rect(self.screen, (255, 0, 255), (self.px, self.py, self.pwidth, self.pheight))

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        myfont = pygame.font.SysFont('Segoe UI', 50)
        food_count_text = myfont.render(str(self.food_count), True, (255, 0, 255))
        elapsed_text = myfont.render(str(int(self.elapsed)), True, (255, 0, 255))
        self.screen.blit(food_count_text, (20, 10))
        self.screen.blit(elapsed_text, (self.screen.get_width() - elapsed_text.get_width() - 20, 10))


    def quit(self):
        self.running = False
        pygame.quit()
