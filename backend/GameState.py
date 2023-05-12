from enum import Enum
class GameState(Enum):
    tie = 'Tie'
    notEnd = 'notEnd'
    OWon = 'O'
    XWon = 'X'