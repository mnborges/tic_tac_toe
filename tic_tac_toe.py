import os
from datetime import datetime
from termcolor import colored
from copy import deepcopy

import colorama
colorama.init()


class Board:
    def __init__(self, size):
        self._size = size
        self._canvas = [[' ' for y in range(self._size)]
                        for x in range(self._size)]
        self._table = []

    def setSize(self):
        print(f"\nCurrent size: {self._size}")
        size = input("Enter new size: ")
        try:
            size = int(size)
        except:
            print("Invalid input.")
            return False
        self._size = size
        self._table = []
        self._canvas = [[' ' for y in range(self._size)]
                        for x in range(self._size)]

    def drawBoard(self):
        div = self._size // 3
        count = 0
        # col
        for i in range(div*3 + 1):
            # line
            for j in range(div*3 + 1):
                if not i % div or not j % div:
                    self._canvas[j][i] = '.'
                elif not i % (div // 2) and not j % (div // 2):
                    self._canvas[j][i] = str(count)
                    self._table.append((j, i))
                    count += 1

    def setPos(self, pos, mark):
        self._canvas[self._table[pos][0]][self._table[pos][1]] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clearBoard(self):
        if not self._table:
            self.drawBoard()
        for index in range(len(self._table)):
            self._canvas[self._table[index][0]
                         ][self._table[index][1]] = str(index)

    def print(self):
        self.clear()
        for y in range(self._size):
            print(' '.join([col[y] for col in self._canvas]))


class Player:
    COLOURS = ['red',
               'green',
               'yellow',
               'blue',
               'magenta',
               'cyan',
               'white']

    def __init__(self, name, mark) -> None:
        self.label = name
        self.name = name
        self.mark = mark
        self.colour = 'green'

    def setUp(self):
        name = input(f"\n{self.label} new name: ")
        mark = ''
        while not mark:
            mark = input(f"{self.label} new mark: ")
            if mark.isdigit():
                mark = ''
                print("Invalid input. Mark should not be a digit.")
        print('Colour options:')
        for i in (range(len(self.COLOURS))):
            print(colored(f"[{i}] - {self.COLOURS[i]}", self.COLOURS[i]))
        colour = ''
        while not colour:
            colour = input(f"{self.label} new colour:")
            try:
                colour = int(colour)
            except:
                input("Invalid input. Hit enter to continue.")
                continue
            if colour not in range(len(self.COLOURS)):
                input("Invalid input. Hit enter to continue.")
                continue
            colour = self.COLOURS[colour]
        self.name = name
        self.mark = mark
        self.colour = colour


class TicTacToe:
    def __init__(self) -> None:
        self.canvas = Board(19)
        self.commands = ["New game", "Set Player 1",
                         "Set Player 2", "View Game History", "Change Board Size", "Exit"]
        self.turn = 0
        self.player = [Player("Player 1", "X"), Player("Player 2", "O")]
        self.history = []

    # display list of game commands
    def displayCommands(self):
        self.canvas.clear()
        for cmd in range(len(self.commands)):
            print(f"[{cmd}] - {self.commands[cmd]}")

    # change details if a player
    def setPlayer(self, player):
        print(
            f"{player.label} current name: {colored(player.name, player.colour)}\t\tCurrent mark: {colored(player.mark, player.colour)}")
        player.setUp()

    # checks whether game is finished and if so, returns the name of the winner or 'draw'
    def gameOver(self):

        def winner(mark):
            for player in self.player:
                if player.mark in mark:
                    return player.name

        q = [self.canvas._canvas[i][j] for i, j in self.canvas._table]

        for i in range(0, 7):
            # row
            if not (i % 3):
                if q[i] == q[i+1] and q[i] == q[i+2]:
                    return winner(q[i])
            if (i < 3):
                # col
                if q[i] == q[i+3] and q[i] == q[i+6]:
                    return winner(q[i])
                # diag
                if not (i % 2):
                    j = 4
                    if not i:
                        j *= 2
                    if q[i] == q[4] and q[i] == q[i+j]:
                        return winner(q[i])
        # draw
        if (self.turn == 9):
            return 'draw'

        return False

    # method that display game history
    def show_history(self):
        if not self.history:
            print("Nothing to show yet. Begin a new game.")
        for value in self.history:
            print(f"{value['timestamp']}:")
            print(
                f"\tPlayers:\n\t\t{[(p.name, p.mark) for p in value['players'] ]}")
            print("\tResult: ")
            if (value['result'] == 'draw'):
                print("\t\tNo winners.")
            else:
                print(f"\t\tVictory of {value['result']}")
        input("Hit enter to continue")

    # method that integrates all game functionalities and run them according to user input
    def begin(self):
        self.canvas.clear()
        done = False
        while not done:
            self.displayCommands()
            cmd = input("Enter command (e.g '0' to begin a new game): ")
            try:
                cmd = int(cmd)
            except:
                input("Invalid Command.\nType any key to continue")
                continue
            self.canvas.clear()
            print(self.commands[cmd].upper())
            if (cmd == 0):
                self.play()
            elif (cmd == 1 or cmd == 2):
                self.setPlayer(self.player[cmd-1])
            elif(cmd == 3):
                self.show_history()
            elif(cmd == 4):
                self.canvas.setSize()
            elif (cmd == 5):
                done = True
            else:
                input("Invalid Command.\nHit enter to continue")

    # TicTacToe runs until game is finished - some player wins or draw
    def play(self):
        self.canvas.drawBoard()
        self.canvas.print()
        while not self.gameOver():
            player = self.player[self.turn % 2]
            print(f"Turn: {self.turn}")
            pos = input(
                f"{player.name}'s turn.\nWhere would like to position your mark '{player.mark}'? ")
            try:
                pos = int(pos)
            except:
                input("Invalid position. Hit enter to continue")
                self.canvas.print()
                continue
            if(pos < 0 or pos > 8):
                input("Invalid position. Hit enter to continue")
                self.canvas.print()
                continue
            self.canvas.setPos(pos, colored(player.mark, player.colour))
            self.canvas.print()
            self.turn += 1
        print("GAME OVER!")
        result = self.gameOver()
        self.turn = 0
        self.canvas.clearBoard()
        self.history.append(
            {'result': result,
             'timestamp': datetime.now(),
             'players':
             deepcopy(self.player)
             })
        if result == 'draw':
            input("DRAW. No winners.")

        else:
            input(f"Congratulations {result}! You won.")


# remove docstrings to be able to run the file and access methods through the interface
"""
game = TicTacToe()
game.begin()
"""
