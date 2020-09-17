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
        # HMM
        epsilon = 0.05
        global n
        n = 14 # guessed as 2*N_SPECIES
        global m
        m = 8  # N_EMISSIONS
        global obs_sequences
        obs_sequences = [[] for fish in range(N_FISH)]
        global species_sequence_mapping
        species_sequence_mapping = [[] for fish_type in range(N_SPECIES)]
        global models
        models = []
        global guessed_fish
        guessed_fish = []
        for species in range(N_SPECIES):
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
                # catch division by zero error
                if denominator == 0.0:
                    denominator = 0.00001
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
                # catch division by zero error
                if denominator == 0.0:
                    denominator = 0.00001
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
            # take care of division by zero error 
            if c0 == 0.0:
                c0 = 0.00001
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
                ct = sum(new_alpha_t)
                # take care of division by zero error 
                if ct == 0.0:
                    ct = 0.00001
                cts[t] = 1 / ct
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
                # prevent log(0) error
                if cts[i] == 0.0:
                    cts[i] = 0.0001
                logProb += math.log(cts[i])
            logProb = -logProb

            iterations_done += 1
            if iterations_done >= max_interations or logProb < oldLogProb:
                break
            oldLogProb = logProb

        return [a, b, pi]

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        # provide t_total for baum welch
        global t_total
        t_total = step
        # keep all observations
        global obs_sequences
        for fish, move in enumerate(observations):
            obs_sequences[fish].append(move)
        # build barier to accumulate observations to train on
        if step <= 80:
            return None
        # guess bassed on trained models, by using alpha pass and choosing the max probabil for the sequence

        # get observation sequence for unguessed fish 
        global guessed_fish
        # choose random from list of fish/sequences that are not guessed yet
        unguessed = random.choice([i for i in range(N_FISH) if i not in guessed_fish])
        obs = obs_sequences[unguessed]

        # get probability of observation for each model by using alpha-pass
        for model in models:
            cts = [0.0 for t in range(t_total)]
            c0 = 0.0
            # init alpha0
            alpha_t_list = []
            alpha_0 = [0.0 for s in range(n)]
            for i in range(n):
                alpha_0[i] = model[2][i] * [row[obs[0]] for row in model[1]][i]
                c0 += alpha_0[i]
            # scale
            # take care of division by zero error 
                if c0 == 0.0:
                    c0 = 0.00001
            cts[0] = 1/c0
            alpha_0 = [p * cts[0] for p in alpha_0]
            alpha_t_list.append(alpha_0)

            # get alpha_t's
            for t in range(1, t_total):
                new_alpha_t = [0.0 for s in range(n)]
                for i in range(n):
                    for j in range(n):
                        new_alpha_t[i] += alpha_t_list[-1][j] * model[0][j][i]
                    new_alpha_t[i] *= [row[obs[t]] for row in model[1]][i]
                ct = sum(new_alpha_t)
                # take care of division by zero error 
                if ct == 0.0:
                    ct = 0.00001
                cts[t] = 1/ct
                # scaleing
                new_alpha_t = [p * cts[t] for p in new_alpha_t]
                alpha_t_list.append(new_alpha_t)



        guess = step % N_FISH # argmax of mdels probabilities 
        # keep track of already guessed fish/ sequences to choose from the others for next guess
        guessed_fish.append(step % N_FISH)
        # This code would make a random guess on each step:
        return (guess, random.randint(0, N_SPECIES - 1))

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
        # starts getting called after barrier passed
        
        # create fish to observation-sequence mapping
        global species_sequence_mapping
        species_sequence_mapping[true_type].append(fish_id) # fish_id is at the same time index of sequence in observations
        # retrain model of fish with new information
        models[true_type] = self.baumWelch(obs_sequences[fish_id], models[true_type])

        """
        # train each "species"-model for all the assosiated sequences 
        global models
        for species, species_sequences in enumerate(species_sequence_mapping):
            for sequnce_idx_of_spec in species_sequences:
                models[species] = self.baumWelch(obs_sequences[sequnce_idx_of_spec], models[species])
        """
        
        """
        print(true_type)
        print('SUM of pi: ' + str(sum(models[0][2])))
        print('SUM of a: ' + str(sum(models[0][0][0])))
        print('SUM of b: ' + str(sum(models[0][1][0])))
        """
        pass
