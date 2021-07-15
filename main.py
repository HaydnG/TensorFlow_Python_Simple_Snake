# Simple pygame program

# Import and initialize the pygame library
import random
from datetime import datetime
import numpy as np
import tensorflow as tf
import gym
import os
import datetime
from gym import wrappers
import pygame
import game
pygame.init()

#https://www.youtube.com/watch?v=VGkcmBaeAGM
#https://github.com/python-engineer/snake-ai-pytorch/blob/main/agent.py


food_game = game.Game()


while food_game.running:

    final_move = [0, 0, 0, 0]
    movey = random.randint(0, 2)
    if movey != 2:
        final_move[movey] = 1
    movex = random.randint(2, 4)
    if movex != 4:
        final_move[movex] = 1

    print(final_move)

    food_game.play_step(final_move)




#https://towardsdatascience.com/deep-reinforcement-learning-build-a-deep-q-network-dqn-to-play-cartpole-with-tensorflow-2-and-gym-8e105744b998