#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import math


class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        # HMM init at the moment N = M
        epsilon = 0.05
        global n
        n = 14
        global m
        m = N_EMISSIONS
        # global a
        global known_fish
        known_fish = {}  # to store fish_id : fish_type

        global models
        models = []
        for spec in range(N_SPECIES):
            a = [[random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for s in range(n)] for s in range(n)]
            for row in a:
                if sum(row) != 1.0:
                    row[-1] = 1 - sum(row[:-1])

            b = [[random.uniform((1 / m) - epsilon, (1 / m) + epsilon) for s in range(m)] for s in range(n)]
            for row in b:
                if sum(row) != 1.0:
                    row[-1] = 1 - sum(row[:-1])

            pi = [random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for s in range(n)]
            if sum(pi) != 1.0:
                pi[-1] = 1 - sum(pi[:-1])

            models.append([a, b, pi])

        pass

    # re-estimate pi
    def reestimatePi(self, gamma_t_list):
        pi = gamma_t_list[0]
        return pi

    # re-estimate A
    def reestimateA(self, a, di_gamma_t_list, gamma_t_list):
        for i in range(n):
            denominator = 0
            for t in range(t_total - 1):
                denominator += gamma_t_list[t][i]
            for j in range(n):
                numerator = 0
                for t in range(t_total - 1):
                    numerator += di_gamma_t_list[t][i][j]
                a[i][j] = numerator / denominator
        return a

        # re-estimate B

    def reestimateB(self, b, obs, gamma_t_list):
        for i in range(n):
            denominator = 0
            for t in range(t_total):
                denominator += gamma_t_list[t][i]
            for j in range(m):
                numerator = 0
                for t in range(t_total):
                    if j == obs[t]:
                        numerator += gamma_t_list[t][i]
                b[i][j] = numerator / denominator
        return b

    def baumWelch(self, obs, model):
        # iterating
        max_interations = 10
        iterations_done = 0
        oldLogProb = -float('inf')
        a, b, pi = model

        while True:

            # global cts
            cts = [0.0 for t in range(t_total)]
            c0 = 0.0
            # init alpha0
            alpha_t_list = []
            alpha_0 = [0.0 for s in range(n)]
            for i in range(n):
                alpha_0[i] = pi[i] * [row[obs[0]] for row in b][i]
                c0 += alpha_0[i]
            # scale
            cts[0] = 1 / c0
            alpha_0 = [p * cts[0] for p in alpha_0]
            alpha_t_list.append(alpha_0)

            # get alpha_t's
            for t in range(1, t_total):
                new_alpha_t = [0.0 for s in range(n)]
                for i in range(n):
                    for j in range(n):
                        new_alpha_t[i] += alpha_t_list[-1][j] * a[j][i]
                    new_alpha_t[i] *= [row[obs[t]] for row in b][i]
                cts[t] = 1 / sum(new_alpha_t)
                # scaling
                new_alpha_t = [p * cts[t] for p in new_alpha_t]
                alpha_t_list.append(new_alpha_t)

            # beta
            # global beta_t_list
            beta_t_list = [[0.0 for v in range(n)] for t in range(t_total)]
            beta_t_list[t_total - 1] = [cts[-1] for v in range(n)]

            for t in range(t_total - 2, -1, -1):
                for i in range(n):
                    for j in range(n):
                        beta_t_list[t][i] += a[i][j] * [row[obs[t + 1]] for row in b][j] * beta_t_list[t + 1][j]
                    # scale
                    beta_t_list[t][i] *= cts[t]

            # di_gamma and gamma for scalled alpha, beta
            # global di_gamma_t_list
            di_gamma_t_list = []
            # global gamma_t_list # [[[]]]
            gamma_t_list = []  # [[]]
            for t in range(t_total - 1):
                gamma_t = [0.0 for v in range(n)]
                di_gamma_t = [[0.0 for c in range(n)] for r in range(n)]
                for i in range(n):
                    for j in range(n):
                        di_gamma_t[i][j] = alpha_t_list[t][i] * a[i][j] * [row[obs[t + 1]] for row in b][j] * \
                                           beta_t_list[t + 1][j]
                        gamma_t[i] += di_gamma_t[i][j]
                gamma_t_list.append(gamma_t)
                di_gamma_t_list.append(di_gamma_t)
            # special case gamma_T-1(i)
            gamma_t_list.append(alpha_t_list[-1])

            # re etimate the HMMs lambda
            pi = self.reestimatePi(gamma_t_list)
            a = self.reestimateA(a, di_gamma_t_list, gamma_t_list)
            b = self.reestimateB(b, obs, gamma_t_list)

            # logarithmic probability
            logProb = 0.0
            for i in range(t_total):
                logProb += math.log(cts[i])
            logProb = -logProb

            iterations_done += 1
            if iterations_done >= max_interations or logProb < oldLogProb:
                break
            oldLogProb = logProb

        return [a, b, pi]

    def alphaPass(self, model, obs):
        a, b, pi = model

        cts = [0.0 for _ in range(t_total)]
        c0 = 0.0
        # init alpha0
        alpha_t_list = []
        alpha_0 = [0.0 for _ in range(n)]
        for i in range(n):
            alpha_0[i] = pi[i] * [row[obs[0]] for row in b][i]
            c0 += alpha_0[i]
        # scale
        cts[0] = 1 / c0
        alpha_0 = [p * cts[0] for p in alpha_0]
        alpha_t_list.append(alpha_0)

        # get alpha_t's
        for t in range(1, t_total):
            new_alpha_t = [0.0 for s in range(n)]
            for i in range(n):
                for j in range(n):
                    new_alpha_t[i] += alpha_t_list[-1][j] * a[j][i]
                new_alpha_t[i] *= [row[obs[t]] for row in b][i]
            cts[t] = 1 / sum(new_alpha_t)
            # scaleing
            new_alpha_t = [p * cts[t] for p in new_alpha_t]
            alpha_t_list.append(new_alpha_t)
        return sum(alpha_t_list[-1])

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """

        wait_time = 110

        global t_total
        t_total = step

        global observation_seq
        observation_seq = observations
        # global obs
        # obs =
        # baumWelch(obs)

        """
        build 7 models, one per speciese with their own matrices
        a model represents a speciese, each species has other probabilities in B observations(to move)
        """

        probabilities = []
        for model in models:
            probabilities.append(self.alphaPass(model, obs))

        guess_type = probabilities.index(max(probabilities))

        # This code would make a random guess on each step:
        # return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        return None  # (0,4), (1,6), (2,4), (3,0), (4,5), (5,0), (6,4), (7,0), (8,3) <= (fish_id, guess)

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        known_fish[fish_id] = true_type

        for id_ in known_fish.keys():
            type_ = known_fish[id_]
            models[type_] = self.baumWelch(observation_seq[id_], models[type_])

        pass
