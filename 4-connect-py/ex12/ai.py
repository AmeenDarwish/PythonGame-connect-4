import numpy as np
import random

EMPTY_CELL = '_'
NUM_OF_COLUMNS = 7

class AI:
    """
    This class represents the artificial intelligence. It can play
    against another artificial intelligence or a human. It will place a
    disk randomly.
    :param game: Game object
    :param player: current player (1/2)
    """

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def find_legal_move(self):
        """
        This function will create a list in which it will add the number of
        each column that has yet to be filled. From that list, a random
        valid column will be returned.
        :return: the number of a column the disk can be placed in.
        """
        possible_moves = []
        transposed_game = np.transpose(self.game.board.board)
        for i in range(NUM_OF_COLUMNS):
            if EMPTY_CELL in list(transposed_game)[i]:
                possible_moves.append(i)
        if possible_moves == []:
            raise Exception('No possible AI moves')
        return random.choice(possible_moves)

    def get_last_found_move(self):
        pass
