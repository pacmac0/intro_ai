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
        # HMM init
        """
        a = 

        b = 

        p = 
        """



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

        """
        # observation sequences per fish
        obs = [[] for fish in range(N_FISH)]
        for fish_idx, move in enumerate(observations):
            obs[fish_idx].append(move)

        if (step % 10) == 0:
            print('We observed ' + str(len(obs[0])) + ' moves made by ' + str(len(obs)) + ' fish')
        """

        # This code would make a random guess on each step:
        return (step % N_FISH, random.randint(0, N_SPECIES - 1))

        return None

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
