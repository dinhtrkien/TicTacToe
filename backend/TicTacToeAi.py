from TicTacToe import Board, Game

class TicTacToeAI:
    def __init__(self, player):
        self.player = player

    def get_move(self, board, size):
        copiedBoard = [['_' for i in range(size)] for j in range(size)]
        for i in range(size):
            for j in range(size):
                if board[i][j] != " ":
                    copiedBoard[i][j] = str(board[i][j]).upper()

        game = Game(board=copiedBoard)
        return game.AImove()