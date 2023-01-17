class BoardClass:
    def __init__ (self, player_1 : str, player_2 : str, owner : int) -> None:
        """Args:
    Players user name(1, 2)
    User name of the last player to have a turn
    Initial gameboard
    Number of turns
    Number of total games
    Number of wins
    Number of ties
    Number of losses
    Number of empty_spot
    Direction of where to start and the starting points
        
    """
        self.player_1   = player_1
        self.player_2   = player_2
        self.owner      = owner
        self.game_board = [[""] * 3 for _ in range(3)]
        self.turn       = 0
        self.total_game = 0
        self.win_game   = 0
        self.tie_game   = 0
        self.empty_spot = 9
        self.directions = ((1, 0, 3),  # down
                           (0, 1, 3),  # right
                           (1, 1, 1),  # left diagonal
                           (-1, 1, 1)) # right diagonal

        self.start_point = ((0, 0), (0, 1), (0, 2), 
                            (0, 0), (1, 0), (2, 0), 
                            (0, 0),
                            (2, 0))

    def updateGamesPlayed(self):
        """Keeps track how many games have started."""

        self.total_game += 1

    def resetGameBoard(self):
        """Clear all the moves from game board."""

        self.game_board = [[""] * 3 for _ in range(3)]
        self.turn = 0

    def updateGameBoard(self, player: int, x_coord: int, y_coord: int) -> bool:
        """Update the gameboard with the players' move.
        Return：
        True if players make valid moves
        False for invalid moves.
        
        """
        mark = 'x' if player == 1 else 'o'
        x, y = x_coord - 1, y_coord - 1
        if self.check_coord_valid(x, y):
            self.turn += 1
            self.game_board[y][x] = mark
            self.empty_spot -= 1
            return True
        else:
            return False

    def check_coord_valid(self, x, y):
        """Check if the coordinates x and y are valid. 
        It cannot be placed out of the board
        Or if the spot is already taken, it cannot be replaced.
        Return: 
        False with the previous two cases
        True for valid moves.

        """
        if x < 0 or y < 0 or x > 2 or y > 2:
            print("Coordinate out of range (should be 1 - 3)")
            return False
        elif self.game_board[y][x] != '':
            print("This spot has already been occupied")
            return False
        else:
            return True

    def is_game_finished(self) -> bool:
        """Return true if someone wins the game or result in a tie
        Count the number of wins and ties
        Else return false.
        
        """
        Winner = self.isWinner()

        if Winner != 0:
            print("player {}({}) wins this round of game!!!".format(Winner, (self.player_1 if Winner == 1 else self.player_2)))
            if Winner == self.owner:
                self.win_game += 1
            return True
        elif self.boardIsFull():
            print("This round of game reaches to a tie")
            self.tie_game += 1
            return True
        else:
            return False
    

    def isWinner(self) -> int:
        """Check who is the winner.
        Returns:
            int: 0 for no one wins, 1 for player 1 wins, 2 for player 2 wins
       
        """
        count = 0
        for direction in self.directions:
            y_update, x_update, start_point_num = direction

            for _ in range(start_point_num):
                if self.check_one_line(self.start_point[count][1], 
                                       self.start_point[count][0], 
                                       x_update, 
                                       y_update):
                    print(self.start_point[count][0], self.start_point[count][1], direction)
                    return (2 - self.turn % 2)
                count += 1
        
        return 0

    def check_one_line(self, x_start, y_start, x_update, y_update) -> bool:
        """Check for the start points and update points in a line.
        Return false if start point is not make or if it is not followed the update
        Else return true.
        
        """
        temp = self.game_board[y_start][x_start]
        if len(temp) == 0:
            return False
        for _ in range(2):
            if temp != self.game_board[y_start + y_update][x_start + x_update]:
                return False
            
            x_start += x_update
            y_start += y_update

        return True

    def boardIsFull(self):
        """Check if the board is full
        Return when there is zero empty spot
        
        """
        return not (self.empty_spot > 0)

    def printStats(self):
        """Prints the following each on a new line:
        Prints the players user name
        Prints the user name of the last person to make a move
        Prints the number of games
        Prints the number of wins
        Prints the number of losses
        Prints the number of ties
        
        """
        result = "Players:\nplayer 1: {}\tplayer 2: {}\n".format(self.player_1, self.player_2)
        result += "Players that take the last move: {}\n".format(self.player_2 if (self.turn % 2 == 0) else self.player_1)
        result += "Number of total games played: {}\n".format(self.total_game)
        lose_game = self.total_game - self.win_game - self.tie_game
        result += "Number of wins:\n{}: {}\t{}: {}\n".format((self.player_1 if self.owner == 1 else self.player_2), self.win_game, (self.player_2 if self.owner == 1 else self.player_1), lose_game)
        result += "Number of loses:\n{}: {}\t{}: {}\n".format((self.player_1 if self.owner == 1 else self.player_2), lose_game, (self.player_2 if self.owner == 1 else self.player_1), self.win_game)
        result += "Number of ties:\n{}: {}\t{}: {}\n".format((self.player_1 if self.owner == 1 else self.player_2), self.tie_game, (self.player_2 if self.owner == 1 else self.player_1), self.tie_game)

        print(result)

    def __repr__(self):
        """Formating the gameboard and display the row and column numbers
        Return the formatted gameboard
        
        """
        template = "\n{:<3s} {:<3s} {:<3s} {:<3s} {:<3s}"
        result = "-" * 20
        result += template.format("", "1", "2", "3", "")
        for i in range(3):
            row = [ele for ele in self.game_board[i]]
            result += template.format(str(i + 1), *row, str(i + 1))
        result += template.format("", "1", "2", "3", "")
        result += "\n" + "-" * 20
        return result

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, idx):
        return self.game_board[idx]





if __name__ == '__main__':
    #Testing
    test = BoardClass("1", "2", 1)
    test.updateGameBoard(1, 3, 1)
    test.updateGameBoard(1, 3, 2)
    test.updateGameBoard(2, 3, 3)
    print(test)
    print(test.isWinner())
