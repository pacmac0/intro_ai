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
        global n
        n = 16
        global m
        m = N_EMISSIONS
        global obs_sequences
        obs_sequences = [[] for _ in range(N_FISH)]
        global known_fish
        known_fish = [[] for _ in range(N_SPECIES)]
        global last_train
        last_train = [-1] * 7
        global models
        models = [self.initABPi() for _ in range(N_SPECIES)]
        pass

    def initABPi(self):
        epsilon = 0.0001
        a = [[random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for _ in range(n)] for _ in range(n)]
        b = [[random.uniform((1 / m) - epsilon, (1 / m) + epsilon) for _ in range(m)] for _ in range(n)]
        pi = [random.uniform((1 / n) - epsilon, (1 / n) + epsilon) for _ in range(n)]
        return [a, b, pi]

    # re-estimate pi
    def reestimatePi(self, gamma_t_list):
        return gamma_t_list[0]

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
        max_interations = 1
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
            beta_t_list = [[0.0 for _ in range(n)] for t in range(t_total)]
            beta_t_list[t_total - 1] = [cts[-1] for v in range(n)]

            for t in range(t_total - 2, -1, -1):
                for i in range(n):
                    for j in range(n):
                        beta_t_list[t][i] += a[i][j] * [row[obs[t + 1]] for row in b][j] * beta_t_list[t + 1][j]
                    # scale
                    beta_t_list[t][i] *= cts[t]

            # di_gamma and gamma for scalled alpha, beta
            di_gamma_t_list = []
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

            # print('a sum =', sum([sum(row) for row in a]) - 14)
            # print('b sum =', sum([sum(row) for row in b]) - 14)
            # print('pi sum =', sum(pi) - 1)

        return [a, b, pi]

    def alphaPass(self, model, obs):
        a, b, pi = model

        # cts = [0.0 for _ in range(t_total)]
        # c0 = 0.0
        # init alpha0
        alpha_t_list = []
        alpha_0 = [0.0 for _ in range(n)]
        for i in range(n):
            alpha_0[i] = pi[i] * [row[obs[0]] for row in b][i]
            # c0 += alpha_0[i]
        # scale
        # cts[0] = 1 / c0
        # alpha_0 = [p * cts[0] for p in alpha_0]
        alpha_t_list.append(alpha_0)

        # get alpha_t's
        for t in range(1, t_total):
            new_alpha_t = [0.0 for s in range(n)]
            for i in range(n):
                for j in range(n):
                    new_alpha_t[i] += alpha_t_list[-1][j] * a[j][i]
                new_alpha_t[i] *= [row[obs[t]] for row in b][i]
            # cts[t] = 1 / sum(new_alpha_t)
            # scaleing
            # new_alpha_t = [p * cts[t] for p in new_alpha_t]
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
        # provideT_total for baum welch
        global t_total
        t_total = step
        # keep all observations
        global obs_sequences
        for fish, move in enumerate(observations):
            obs_sequences[fish].append(move)
        # build barier to accumulate observations to train on
        if step < 110:
            return None

        # guess based on trained models
        if step < 115:
            # randomly pick fish to guess
            guess_fish = random.choice([f for f in list(range(70)) if f not in sum(known_fish, [])])
            probabilities = [self.alphaPass(model, obs_sequences[guess_fish]) for model in models]
            guess_type = probabilities.index(max(probabilities))
            return guess_fish, guess_type

        probabilities = []
        for i in range(len(obs_sequences)):
            if i in sum(known_fish, []):
                probabilities.append([-100 for _ in models])
            else:
                probabilities.append([self.alphaPass(model, obs_sequences[i]) for model in models])
        max_probabilities = [max(probs) for probs in probabilities]
        guess_fish = max_probabilities.index(max(max_probabilities))
        guess_type = (probabilities[guess_fish]).index(max(probabilities[guess_fish]))

        # This code would make a random guess on each step:
        # return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        # return None  # (0,4), (1,6), (2,4), (3,0), (4,5), (5,0), (6,4), (7,0), (8,3) <= (fish_id, guess)
        # print(guess_fish, guess_type)
        return guess_fish, guess_type

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

        known_fish[true_type].append(fish_id)
        # print(known_fish)
        models[true_type] = self.baumWelch(sum([obs_sequences[i] for i in known_fish[true_type]], []), self.initABPi())

        global last_train
        last_train[true_type] = t_total

        t_guessed_before = [g for g in last_train if 0 < g < max(last_train)]

        if t_total < 60:
            n_retrain = 5
        elif t_total < 150:
            n_retrain = 3
        else:
            n_retrain = 2

        if t_guessed_before:
            for type_ in [last_train.index(t) for t in
                          sorted(t_guessed_before)[:min(n_retrain, len(t_guessed_before))]]:
                models[type_] = self.baumWelch(sum([obs_sequences[i] for i in known_fish[type_]], []), self.initABPi())
                last_train[type_] = t_total + random.uniform(0, 0.5)

        pass
