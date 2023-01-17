import socket
import time
from gameboard import BoardClass

class Player2:

    def __init__(self):
        """Args:
        Player 2's username
        """
        self.register_usrname()

    def register_usrname(self):
        """Ask for the username of player 2."""
        self.name = input("Please enter the username for player 2: ")
        print(self.name)

    def start_socket(self):
        """Start the socket."""
        self.register_host()
        self.init_host()
        self.connect_client()

    def register_host(self):
        """Register a(n) host name/IP address, a port, and a socket object for player 2. """
        self.host_ip    = input("Please enter host name/IP address of player 2: ")
        self.port       = int(input("Please enter port of the host: "))
        self.socket     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_host(self):
        """Associate host_ip and port to the socket. Set up and start running the TCP socket."""
        self.socket.bind((self.host_ip, self.port))
        self.socket.listen(5)

    def connect_client(self):
        """Accept the information sent by player 1 and receive them."""
        self.clientSocket, clientAddress = self.socket.accept()
        self.clientSocket.send(bytes('Hello this is player2: ' + self.name, "ascii"))
        clientData = self.clientSocket.recv(1024).decode('ascii')
        self.player1_name = clientData.split(':')[1].strip()

    def run(self):
        """Function to run the program."""
        self.start_socket()
        self.board = BoardClass(self.player1_name, self.name, 2)
        self.play_game()
        self.end()

    def play_game(self):
        """Function to play the whole game and end the program """
        while True:
            self.board.updateGamesPlayed()
            self.play_one_round_game()
            other_decision = self.clientSocket.recv(1024).decode('ascii')
            if other_decision == "Fun Times":
                break
            self.board.resetGameBoard()

    def play_one_round_game(self):
        """Receive the move from player 1 and print the board after player 2 makes a move."""
        while not self.board.is_game_finished():
            self.receive_move()
            if self.board.is_game_finished():
                return
            print(self.board)
            x, y = self.make_move()
            self.clientSocket.send(bytes("{} {}".format(x, y), "ascii"))
    
    def receive_move(self):
        """Receive the move from player 1."""
        other_x, other_y = self.clientSocket.recv(1024).decode("ascii").split(" ")
        other_x = int(other_x)
        other_y = int(other_y)
        self.board.updateGameBoard(1, other_x, other_y)

    def make_move(self):
        """Make a move by asking player 2 which position he desired.
        Return:
        position that player 2 chose."""
        while True:
            x, y = self.input_move()
            if self.board.updateGameBoard(2, x, y):
                break
        
        return x, y

    def input_move(self):
        """Ask player 2 for input and declare the position he desired."""
        while True:
            try:
                
                x, y = input("Please enter the x and y coordinate for your next move splited by space(e.g 2 3 for coordinate (2, 3))").split(" ")
                return int(x), int(y)

            except:

                print("Please try again with the correct input.")

    def end(self):
        """The game is finished and print out the statistic"""
        self.socket.close()
        self.board.printStats()

if __name__ == "__main__":
    # Testing
    test_2 = Player2()
    test_2.run()
