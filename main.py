import random

import pygame
from tensorflow import keras
import tensorflow as tf
import game
import agent
from collections import deque
import numpy as np
pygame.init()
import helper

#https://www.youtube.com/watch?v=VGkcmBaeAGM
#https://github.com/python-engineer/snake-ai-pytorch/blob/main/agent.py


#https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc
#https://github.com/mswang12/minDQN/blob/main/minDQN.py

episodes = 10000

def main():

    epsilon = 1 # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
    max_epsilon = 1 # You can't explore more than 100% of the time
    min_epsilon = 0.001 # At a minimum, we'll always explore 1% of the time
    decay = 0.004

    total_steps=0

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    game_count = 0

    env = game.Game(True, False)
    game_agent = agent.Agent(env)

    target_game_agent = agent.Agent(env)

    replay_memory = deque(maxlen=40_000)

    # X = states, y = actions
    X = []
    y = []

    steps_to_update_target_model = 0

    for episode in range(episodes):
        game_count += 1
        total_training_rewards = 0

        env.reset()

        observation = env.get_state()

        done = False
        while not done:
            total_steps+=1
            steps_to_update_target_model += 1

            random_number = np.random.rand()
            # 2. Explore using the Epsilon Greedy Exploration Strategy
            action = [0, 0, 0, 0]
            if random_number <= epsilon:
                move = random.randint(0, 3)
                action[move] = 1
            else:
                # Exploit best known action
                # model dims are (batch, env.observation_space.n)
                encoded = game_agent.encode_observation(observation, env.observations)
                encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
                predicted = game_agent.model.predict(encoded_reshaped).flatten()

                move = np.argmax(predicted).item()
                action[move] = 1

            new_observation, reward, done, info = env.step(action)
            replay_memory.append([observation, action, reward, new_observation, done])

            # 3. Update the Main Network using the Bellman Equation
            if steps_to_update_target_model % 2 == 0 or done:
                game_agent.train(replay_memory, target_game_agent.model, done)

            observation = new_observation
            total_training_rewards += reward


            if done:
                plot_scores.append(total_training_rewards)
                total_score += total_training_rewards
                mean_score = total_score / game_count

                plot_mean_scores.append(mean_score)
                if game_count % 4 == 0:
                    helper.plot(plot_scores, plot_mean_scores)

                print('Total training rewards: {} Total Steps: {}, Games: {}, with final reward = {} - Total Score: {} - Epsilon: {}'.format(
                    total_training_rewards, total_steps,episode, reward, info, epsilon))
                total_training_rewards += 1

                if steps_to_update_target_model >= 15:
                    print('Copying main network weights to the target network weights')
                    target_game_agent.model.set_weights(game_agent.model.get_weights())
                    steps_to_update_target_model = 0
                break


        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

main()

# env = game.Game(False, True)
#
#
#
# while env.running:
#
#
#
#     ## Testing Random Move
#     # final_move = [0, 0, 0, 0]
#     # movey = random.randint(0, 2)
#     # if movey != 2:
#     #     final_move[movey] = 1
#     # movex = random.randint(2, 4)
#     # if movex != 4:
#     #     final_move[movex] = 1
#
#     #print(final_move)
#
#     state, reward, end, food = env.step([0,0,0,0])
#
#     print(state)


#https://towardsdatascience.com/deep-reinforcement-learning-build-a-deep-q-network-dqn-to-play-cartpole-with-tensorflow-2-and-gym-8e105744b998