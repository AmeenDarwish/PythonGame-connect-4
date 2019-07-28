import numpy as np


class Game:
    """
    This class represents the game (handles the game engine). Here the moves
    will be made by each player, check if there is a win either horizontally,
    vertically, or diagonally, or if the board if full and it's a tie.
    """

    DISKS_TO_WIN = 4
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6
    TIE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

    def __init__(self):
        self.current_player = 1
        self.board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT)

    def make_move(self, column):
        """
        This function will receive the number of the column we want to place
        a disk in, check if it is a valid move (the column has empty spaces,
        in borders and the game has yet to end), add to that column the
        disk and change the player. else, an exception will be raised.
        :param column: the column we want to add a disk to
        :return: None
        """
        if column is None or column < 0 or column >= self.BOARD_WIDTH \
                or self.get_winner() is not None:
            raise Exception('Illegal move')
        row = self.check_col(column)
        if row == -1:
            raise Exception('Illegal move')
        self.board.make_move(self.current_player, row, column)
        self.current_player = (self.current_player % 2) + 1  # change the player

    def check_col(self, column):
        """
        This function will check if the given column has an empty spot
        :param column: the column we want to add a disk to
        :return: the first empty row
        """
        for row in range(self.board.height - 1, -1, -1):
            if self.board.board[row][column] == Board.EMPTY_SLOT:
                return row
        return -1

    def get_current_player(self):
        """
        :return: the current player
        """
        return self.current_player

    def get_player_at(self, row, column):
        """
        :return: if the index we are checking (row,column) is not empty,
        the owner of the disk in the spot will be returned, if it's empty,
        None will be returned, and finally, if the indexes are not valid,
        an exception will be raised.
        """
        try:
            if self.board.board[row][column] != Board.EMPTY_SLOT:
                return self.board.board[row][column]
            else:
                return None
        except IndexError:
            raise Exception("illegal location")

    def _win_in_row(self, player):
        """
        This function will check if there are 4 disks, in succession, in one row
        :param player: the current player
        :return: True if four were found, False otherwise
        """
        for row_num in range(len(self.board.board)):
            win = []
            disks_in_row = 0
            for column_num in range(len(self.board.board[row_num])):
                if self.board.board[row_num][column_num] == player:
                    win.append((row_num, column_num))
                    disks_in_row += 1
                else:
                    win = []
                    disks_in_row = 0

                if disks_in_row == self.DISKS_TO_WIN:

                    return True, win
        return False, []

        # disks_in_row = 0
        # for row in self.board.board:
        #     disks_in_row = 0
        #     for element in row:
        #         if element == player:
        #             disks_in_row += 1
        #         else:
        #             disks_in_row = 0
        #
        #         if disks_in_row == self.DISKS_TO_WIN:
        #             return True
        #
        # return disks_in_row == self.DISKS_TO_WIN

    def _win_in_col(self, player):
        """
        This function will check if there are 4 disks consecutively in one
        column
        :param player: the current player
        :return: True if four were found, False otherwise
        """
        transposed_board = np.transpose(self.board.board)
        disks_in_row = 0

        for row_num in range(len(transposed_board)):
            win = []
            disks_in_row = 0
            for column_num in range(len(transposed_board[row_num])):
                if transposed_board[row_num][column_num] == str(player):
                    win.append((column_num, row_num))
                    disks_in_row += 1
                else:
                    win = []
                    disks_in_row = 0

                if disks_in_row == self.DISKS_TO_WIN:

                    return True, win
        return False, []

        # board_t = np.transpose(self.board.board)
        # disks_in_col = 0
        # for row in list(board_t):
        #     disks_in_col = 0
        #     for element in row:
        #         if element == str(player):
        #             disks_in_col += 1
        #         else:
        #             disks_in_col = 0
        #         if disks_in_col == self.DISKS_TO_WIN:
        #             return True
        #
        # return disks_in_col == self.DISKS_TO_WIN

    def _win_in_diag(self, player):
        """
        This function will check if the are 4 disks one after the other
        diagonally.
        :param player: the current player
        :return: True if four were found, False otherwise
        """
        board_inds = [[0, 1, 2, 3, 4, 5, 6],
                      [7, 8, 9, 10, 11, 12, 13],
                      [14, 15, 16, 17, 18, 19, 20],
                      [21, 22, 23, 24, 25, 26, 27],
                      [28, 29, 30, 31, 32, 33, 34],
                      [35, 36, 37, 38, 39, 40, 41]]

        for i in range(-2, 4):
            win = []
            winning_places = []
            curr_array = np.diag(self.board.board, i)
            ind_array = np.diag(board_inds, i)
            disks_in_diag = 0

            for ind in range(len(curr_array)):
                if curr_array[ind] == str(player):
                    winning_places.append(ind_array[ind])
                    disks_in_diag += 1

                    if disks_in_diag == 4:
                        for j in winning_places:
                            for row_num in range(len(board_inds)):
                                for column_num in range(
                                        len(board_inds[row_num])):
                                    if board_inds[row_num][column_num] == j:
                                        win.append((row_num, column_num))
                        print('windiag')
                        return True, win

                else:
                    winning_places = []
                    disks_in_diag = 0

            ##################################################################

            win2 = []
            winning_places2 = []
            curr_array2 = np.diag(np.fliplr(self.board.board), i)
            ind_array2 = np.diag(np.fliplr(board_inds), i)
            disks_in_diag2 = 0

            for ind2 in range(len(curr_array2)):
                if curr_array2[ind2] == str(player):
                    winning_places2.append(ind_array2[ind2])

                    disks_in_diag2 += 1

                    if disks_in_diag2 == 4:
                        for j in winning_places2:
                            for row_num in range(len(board_inds)):
                                for column_num in range(
                                        len(board_inds[row_num])):
                                    if board_inds[row_num][column_num] == j:
                                        win2.append((row_num, column_num))

                        return True, win2

                else:
                    winning_places2 = []
                    disks_in_diag2 = 0
        return False, []
        # for i in range(-2, 4):
        #     disks_in_diag = 0
        #     disks_in_diag2 = 0
        #
        #     curr_array = np.diag(self.board.board, i)
        #     curr_array2 = np.diag(np.fliplr(self.board.board), i)
        #
        #     for element1 in curr_array:
        #         if element1 == str(player):
        #             disks_in_diag += 1
        #         else:
        #             disks_in_diag = 0
        #         if disks_in_diag == self.DISKS_TO_WIN:
        #             return True
        #     for element2 in curr_array2:
        #         if element2 == str(player):
        #             disks_in_diag2 += 1
        #         else:
        #             disks_in_diag2 = 0
        #         if disks_in_diag2 == self.DISKS_TO_WIN:
        #             return True
        #
        # return disks_in_diag == self.DISKS_TO_WIN \
        #        or disks_in_diag2 == self.DISKS_TO_WIN

    def get_winner(self):
        """
        This function will check if either players won.
        :return: if there is no winner, -1 will be returned, else if there is a
        winner, they will be returned, and, if there are no winners and the
        board is full, 0 will be returned.
        """
        player1_wins = self._win_in_row(self.PLAYER_1)[0] \
                       or self._win_in_col(self.PLAYER_1)[0] \
                       or self._win_in_diag(self.PLAYER_1)[0]
        player2_wins = self._win_in_row(self.PLAYER_2)[0] \
                       or self._win_in_col(self.PLAYER_2)[0] \
                       or self._win_in_diag(self.PLAYER_2)[0]

        tie = self.board.is_full()
        if player1_wins:
            return self.PLAYER_1
        elif player2_wins:
            return self.PLAYER_2
        else:
            return self.TIE if tie else None

    def winner_indexes(self):
        if self._win_in_row(self.PLAYER_1)[0]:
            win = self._win_in_row(self.PLAYER_1)[1]
            return win
        elif self._win_in_col(self.PLAYER_1)[0]:
            win = self._win_in_col(self.PLAYER_1)[1]
            return win
        elif self._win_in_diag(self.PLAYER_1)[0]:
            win = self._win_in_diag(self.PLAYER_1)[1]
            return win

        if self._win_in_row(self.PLAYER_2)[0]:
            win = self._win_in_row(self.PLAYER_2)[1]
            return win
        elif self._win_in_col(self.PLAYER_2)[0]:
            win = self._win_in_col(self.PLAYER_2)[1]
            return win
        elif self._win_in_diag(self.PLAYER_2)[0]:
            win = self._win_in_diag(self.PLAYER_2)[1]
            return win


class Board:
    EMPTY_SLOT = '_'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[self.EMPTY_SLOT] * width for _ in range(height)]

    def make_move(self, player, row, column):
        """
        This function will add the disk to the appropriate row and column.
        :param player: the current player
        :param row: the row we want to place a disk at
        :param column: the column we want to place a disk at
        :return:
        """
        if row >= self.height or row < 0 or column < 0 or column >= self.width:
            raise Exception('Illegal location')
        self.board[row][column] = player

    def is_full(self):
        """
        This function will check whether there are any empty slots available
        in the board or not.
        :return: True if the board is full, False if not
        """
        empty_cells = 0
        for row in self.board:
            for cell in row:
                if cell == self.EMPTY_SLOT:
                    empty_cells += 1
        return empty_cells == 0

    def __repr__(self):
        return '\n'.join([', '.join(row) for row in self.board])
