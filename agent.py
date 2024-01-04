# prob.py
# This is

import random
import numpy as np
import queue
import math

from gridutil import *


class Agent:
    def __init__(self, size, landmarks, sigma_move_fwd, sigma_move_turn, sigma_perc):
        self.size = size
        self.landmarks = landmarks
        self.sigma_move_fwd = sigma_move_fwd
        self.sigma_move_turn = sigma_move_turn
        self.sigma_perc = sigma_perc

        self.t = 0
        self.n = 500
        # create an initial particle set as 2-D numpy array with size (self.n, 3) (self.p)
        # and initial weights as 1-D numpy array (self.w)
        # TODO PUT YOUR CODE HERE

        self.p = np.stack([np.random.random(self.n) * self.size,
                           np.random.random(self.n) * self.size,
                           np.random.random(self.n) * 2.0 * math.pi], axis=1)

        self.w = np.ones(self.n) / self.n

        # ------------------

    def __call__(self):
        # turn by -pi/20.0 and move forward by 1
        action = (-math.pi/20, 1.0)
        # no turn, only move forward by 1.0
        # action = (0.0, 1.0)

        # use information about requested action to update posterior
        # TODO PUT YOUR CODE HERE

        self.predict_posterior(action)

        # ------------------

        self.t += 1

        return action

    def predict_posterior(self, action):
        # predict posterior using requested action
        # TODO PUT YOUR CODE HERE

        for i in range(self.n):
            loc = self.p[i, 0:2]
            orient = self.p[i, 2]

            orient = (orient+action[0]+np.random.randn(1)*self.sigma_move_turn % (2.0*math.pi))
            loc = moveForward(loc, orient, action[1]+np.random.randn(1)*self.sigma_move_fwd)
            self.p[i, 0] = loc[0]
            self.p[i, 1] = loc[1]
            self.p[i, 2] = orient

        # ------------------

        # this function does not return anything
        return

    def calculate_weights(self, percept):
        # calculate weights using percept
        # TODO PUT YOUR CODE HERE

        for i in range(self.n):
            curw = 1
            for l in range(len(self.landmarks)):
                ux = self.p[i, 0] - self.landmarks[l][0]
                uy = self.p[i, 1] - self.landmarks[l][1]
                u = math.sqrt(pow(ux, 2) + pow(uy, 2))
                dif = u - percept[l]
                curw *= math.exp(-0.5 * (dif ** 2) / pow(self.sigma_perc, 2))

            self.w[i] = curw
        self.w = self.w / np.sum(self.w)

        # ------------------

        # this function does not return anything
        return

    def correct_posterior(self):
        new_p = []
        index = 0
        beta = 0.0
        mw = max(self.w)
        for i in range(self.n):
            beta += np.random.random() * 2 * mw
            while beta > self.w[index]:
                beta -= self.w[index]
                index = (index + 1) % self.n
            new_p.append(self.p[index].tolist())

        self.p = np.array(new_p)
        return

    def get_particles(self):
        return self.p

    def get_weights(self):
        return self.w