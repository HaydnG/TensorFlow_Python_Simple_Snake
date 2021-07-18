from datetime import time

import torch
import random
import numpy as np
from collections import deque

import tensorflow as tf
from tensorflow import keras
import game




class Agent:

    def __init__(self, env: game.Game):
        learning_rate = 0.5
        init = tf.keras.initializers.RandomNormal(mean=0., stddev=1.)
        self.model = keras.Sequential()
        self.model.add(keras.layers.Input(shape=[env.observations]))
        self.model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
        self.model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
        self.model.add(keras.layers.Dense(env.actions, activation='sigmoid', kernel_initializer=init))
        self.model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                      metrics=['accuracy'])
        self.env = env

    def _get_qs(self, state, step):
        return self.model.predict(state.reshape([1, state.shape[0]]))[0]

    def train(self, replay_memory, target_model, done):
        learning_rate = 0.5  # Learning rate
        discount_factor = 0.7

        MIN_REPLAY_SIZE = 1000
        if len(replay_memory) < MIN_REPLAY_SIZE:
            return

        batch_size = 64 * 2
        mini_batch = random.sample(replay_memory, batch_size)

        current_states = np.array(
            [self.encode_observation(transition[0], self.env.observation_shape) for transition in mini_batch], dtype=int)

        current_qs_list = self.model.predict(current_states)
        new_current_states = np.array(
            [self.encode_observation(transition[3], self.env.observation_shape) for transition in mini_batch], dtype=int)
        future_qs_list = target_model.predict(new_current_states)

        X = []
        Y = []
        for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
            if not done:
                max_future_q = reward + discount_factor * np.max(future_qs_list[index])
            else:
                max_future_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

            X.append(self.encode_observation(observation, self.env.observations))
            Y.append(current_qs)
        self.model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

    def encode_observation(self, observation, n_dims):
        return observation