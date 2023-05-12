from GameState import GameState
import datetime
from Board import Board

# GAME CONSTANTS
X = 'X'
O = 'O'
EMPTY = '_'
BOARD_SIZE = 5
SEARCH_TIME = 5

class Game:
    def __init__(self, board):
        self.mBoard = Board(BOARD_SIZE, board)
        self.mBoardSize = BOARD_SIZE
        self.mBestMove = 0

   # check if a player wins
    def isWin(self, turn):
        char = ''
        if turn % 2 == 0:
            char = 'X'
        else:
            char = 'O'
        lastMove = self.mBoard.getLastMove()
        row, col = self.mBoard.convertPosition(lastMove)

        if self.mBoard.all_same(self.mBoard.getNumberOfRow(row), char) or \
                self.mBoard.all_same(self.mBoard.getNumberOfColumn(col), char):
            return True

        if self.mBoard.checkIfOnMainDiagonal(lastMove):
            if self.mBoard.all_same(self.mBoard.getMainDiagonal(), char):
                return True

        if self.mBoard.checkIfOnSecondaryDiagonal(lastMove):
            if self.mBoard.all_same(self.mBoard.getSecondaryDiagonal(), char):
                return True

        return False

    # Check if the game is tie
    def isTie(self):
        for i in range(self.mBoard.size ** 2):
            if self.mBoard.isEmptyPosition(i):
                return False
        return True

    # Return all the valid moves on the board
    def generate(self):
        possibleMoves = []
        for i in range(self.mBoard.size ** 2):
            if self.mBoard.isEmptyPosition(i):
                possibleMoves.append(i)
        return possibleMoves

    def checkGameState(self):
        if self.isWin(0):
            return GameState.XWon

        if self.isWin(1):
            return GameState.OWon

        if self.isTie():
            return GameState.tie

        return GameState.notEnd

    def AImove(self):
        computerMove = self.iterativeDeepSearch()
        print(computerMove)
        return self.mBoard.convertPosition(computerMove)

    def minimax(self, depth, isMax, alpha, beta, startTime, timeLimit):
        moves = self.generate()
        score = self.evaluate()
        position = None

        if datetime.datetime.now() - startTime >= timeLimit:
            self.mTimePassed = True

        if not moves or depth == 0 or self.mTimePassed:
            gameResult = self.checkGameState()
            if gameResult.value == 'X':
                return -10**(self.mBoard.size+1), position
            elif gameResult.value == 'O':
                return 10**(self.mBoard.size+1), position
            elif gameResult.value == 'Tie':
                return 0, position

            return score, position

        if isMax:
            for i in moves:
                    self.mBoard.playO(i)
                    score, dummy = self.minimax(depth-1, not isMax, alpha, beta, startTime, timeLimit)
                    if score > alpha:
                        alpha = score
                        position = i
                        self.mBestMove = i

                    self.mBoard.deleteMove(i)
                    if beta <= alpha:
                        break

            return alpha, position
        else:
            for i in moves:
                self.mBoard.playX(i)
                score, dummy = self.minimax(depth-1, not isMax, alpha, beta, startTime, timeLimit)
                if score < beta:
                    beta = score
                    position = i
                    self.mBestMove = i
                self.mBoard.deleteMove(i)
                if alpha >= beta:
                    break

            return beta, position

    # Choose the best move within search time
    def iterativeDeepSearch(self):
        startTime = datetime.datetime.now()
        endTime = startTime + datetime.timedelta(0, SEARCH_TIME)
        depth = 1
        position = None
        self.mTimePassed = False
        while True:
            currentTime = datetime.datetime.now()
            if currentTime >= endTime:
                break
            best, position = self.minimax(depth, True, -10000000, 10000000, currentTime, endTime-currentTime)
            depth += 1

        if position is None:
            position = self.mBestMove

        return position

    # calculate number of X, O and empty squares
    def calculateLine(self, line):
        oNum = line.count(O)
        xNum = line.count(X)
        empty = line.count(EMPTY)
        return oNum, xNum, empty

    # evaluate the score of a line
    def getScoreLine(self, line):
        score = 0
        oSum, xSum, EmptySum = self.calculateLine(line)
        if xSum == 0 and oSum != 0:
            if oSum == self.mBoard.size:
                score += 11 ** (oSum - 1)
            score += 10 ** (oSum - 1)
        if oSum == 0 and xSum != 0:
            score += -(10 ** (xSum - 1))
        return score

    # evaluate the score of the game board
    def evaluate(self):
        score = 0
        for i in range(self.mBoard.size):
            score += self.getScoreLine(self.mBoard.getNumberOfRow(i))
            score += self.getScoreLine(self.mBoard.getNumberOfColumn(i))

        diagonals = self.mBoard.getDiagonal()
        for i in range(2):
            score += self.getScoreLine(diagonals[i]) 
        return score