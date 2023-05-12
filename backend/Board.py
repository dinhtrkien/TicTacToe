class Board:
    def __init__(self, size, board):
        self.size = size
        self.board = board
        self.lastMove = None

    # convert position from number to (x, y)
    def convertPosition(self, position):
        x = position%self.size
        y = position//self.size
        return y, x

    # get the last move played
    def getLastMove(self):
        return self.lastMove

    # get the number of row
    def getNumberOfRow(self, numberOfRow):
        return self.board[numberOfRow]

    # get the number of column
    def getNumberOfColumn(self, numberOFColumn):
        return [row[numberOFColumn] for row in self.board]

    # return the 2 main diagonals of the board
    def getDiagonal(self):
        diagonal1 = self.getMainDiagonal()
        diagonal2 = self.getSecondaryDiagonal()
        return diagonal1, diagonal2

    # Get the main diagonal of the board, left to right
    def getMainDiagonal(self):
        return [self.board[i][i] for i in range(self.size)]

    # Get the main diagonal of the board, right to left
    def getSecondaryDiagonal(self):
        diagonal = []
        j = 0
        for i in reversed(range(self.size)):
            diagonal.append(self.board[i][j])
            j += 1
        return diagonal

    # Check if position is on the main diagonal
    def checkIfOnMainDiagonal(self, position):
        return position % (self.size + 1) == 0

    # Check if position is on the secondary diagonal
    def checkIfOnSecondaryDiagonal(self, position):
        return position % (self.size - 1) == 0

    # play X on the board
    def playX(self, position):
        self.lastMove = position
        (row, column) = self.convertPosition(position)
        self.board[row][column] = X

    # delete the move on the board
    def deleteMove(self, position):
        (row, column) = self.convertPosition(position)
        self.board[row][column] = EMPTY

    # play O on the board
    def playO(self, position):
        self.lastMove = position
        (row, column) =  self.convertPosition(position)
        self.board[row][column] = O

    # check if the position on the board is empty
    def isEmptyPosition(self, position):
        (row, column) = self.convertPosition(position)
        return self.board[row][column] == EMPTY

    # check if a line is filled with X or O
    def all_same(self, listToBeChecked, char):
        return all(x == char for x in listToBeChecked)