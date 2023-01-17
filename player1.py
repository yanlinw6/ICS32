import socket
import time
from gameboard import BoardClass

class Player1:

    def __init__(self):
        """Args:
        Player 1's username
        """
        self.register_usrname()   

    def register_usrname(self):
        """Ask the username for player 1."""
        self.name = input("Please enter the username for player 1: ")

    def start_socket(self):
        """Check the connection of the socket.
        Return:
        False when the connections failed.
        True when the connections succeed.
        
        """
        self.register_socket()
        if not self.check_connections():
            return False
        
        self.connect_host()
        return True

    def register_socket(self):
        """The information we need(ie.host name/IP address, port) and create a socket object."""
        self.host_ip    = input("Please enter host name/IP address of player 2 you want to play with: ")
        self.port       = int(input("Please enter port of the host: "))
        self.socket     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
    def check_connections(self):
        """If the connection cannot be made then the user will be asked if they want to try again:
        If the user enters 'y' then you will request the host information from the user again.
        If the user enters 'n' then you will end the program.
        If the user enters other values, the program will ask him to try again.
        Return:
        True when the connection succeed.
        False when the user enters "n".
        """
        connect_success = False

        while not connect_success:
            try:
                self.socket.connect((self.host_ip, self.port))
                connect_success = True
            except socket.error:
                try_reconnect = input("Do you want reconnect? (Enter \'y\' or \'n\') only): ")

                while try_reconnect not in {'y', 'n'}:
                    try_reconnect = input("Wrong Input!! (Enter \'y\' or \'n\') only): ")
                
                if try_reconnect == 'y':
                    self.register_socket()
                else:
                    return False

        return True

    def connect_host(self):
        """Send the data to player 2."""
        serverData = self.socket.recv(1024).decode('ascii')
        self.player2_name = serverData.split(':')[1].strip()
        self.socket.send(bytes('Hello this is player1: ' + self.name, "ascii"))

    def run(self):
        """Function to run the program."""
        if not self.start_socket():
            print("Player 1 ends program")
            return
        self.board = BoardClass(self.name, self.player2_name, 1)
        self.play_game()
        self.end()

    def play_game(self):
        """Once a game as finished (win or tie) the user will indicate if they want to play again using the command line.
        If the user enters 'y' or 'Y' then player 1 will send "Play Again" to player 2.
        If the user enters 'n' or 'N' then player 1 will send "Fun Times" to player 2 and end the program.
        Once the user is done player they will print all the statistics.
        
        """
        while True:
            self.board.updateGamesPlayed()
            self.play_one_round_game()
            while True:
                next_move = input("Do you want to play another round?(Y or N): ").lower()
                if next_move in {'y', 'n'}:
                    break
                print("Wrong Input, input must be \'Y\' or \'N\'")
            
            if next_move == 'y':
                self.socket.send(bytes("Play Again", 'ascii'))
                self.board.resetGameBoard()
            else:
                self.socket.send(bytes("Fun Times", 'ascii'))
                break

    def play_one_round_game(self):
        while not self.board.is_game_finished():
            print(self.board)
            x, y = self.make_move()
            self.socket.send(bytes("{} {}".format(x, y), "ascii"))
            if self.board.is_game_finished():
                return
            self.recive_action()
    
    def make_move(self):
        """Continue ask the player 1 for the position.
        If player 1 makes a move, he will wait for player 2 to make a move.
        Returns:
        The position that player 1 has made.
        
        """
        while True:
            x, y = self.input_move()
            if self.board.updateGameBoard(1, x, y):
                break
        
        return x, y
               
    def input_move(self):
        """Ask player 1 for the desired position he wants to move
        Returns:
        integer type of x and y.
        
        """
        while True:
            try:
                
                x, y = input("Please enter the x and y coordinate for your next move splited by space(e.g 2 3 for coordinate (2, 3))").split(" ")
                return int(x), int(y)

            except:

                print("Please try again with the correct input.")
                

    def recive_action(self):
        """Wait for the move of player 2 and simply update the gameboard when it is player 1's turn."""
        other_x, other_y = self.socket.recv(1024).decode("ascii").split(" ")
        other_x = int(other_x)
        other_y = int(other_y)
        self.board.updateGameBoard(2, other_x, other_y)

    def end(self):
        """Finish the game and simply print out the statistic."""
        self.socket.close()
        self.board.printStats()


if __name__ == '__main__':
    #Testing
    test_1 = Player1()
    test_1.run()


