#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        # HMM init at the moment N = M
        epsilon = 0.05
        n = N_EMISSIONS
        m = N_EMISSIONS
        global a
        a = [[random.uniform((1/n)-epsilon, (1/n)+epsilon) for s in range(n)] for s in range(n)]
        for row in a:
            if sum(row) != 1.0:
                row[-1] = 1 - sum(row[:-1])

        
        global b
        b = [[random.uniform((1/m)-epsilon, (1/m)+epsilon) for s in range(m)] for s in range(n)]
        for row in b:
            if sum(row) != 1.0:
                row[-1] = 1 - sum(row[:-1])
        
        global pi
        pi = [random.uniform((1/n)-epsilon, (1/n)+epsilon) for s in range(n)]
        if sum(pi) != 1.0:
                pi[-1] = 1 - sum(pi[:-1])
        
        pass

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        

        # This code would make a random guess on each step:
        #return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        return None #(fish_id, guess)

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





        pass
