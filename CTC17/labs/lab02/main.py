# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# class __QueensBoard:
#     def __init__(self, arg = None):
#         if not self.h:
#             self.h = 0
#         if arg is None:
#             if not self.queensInBoard:
#                 self.queensInBoard = []
#         else:
#             if not self.queensInBoard:
#                 self.queensInBoard = [arg]
#             else:
#                 self.queensInBoard.append(arg)
#
#     def __str__(self):
#         return repr(self) + self.queensInBoard


def abs_int(x):
    if x > 0:
        return x
    return -x


def queens_rivals(queen01, queen02):
    if isinstance(queen01, Queen) and isinstance(queen02, Queen):
        if (queen01.y == queen02.y) or abs_int(queen02.x - queen01.x) == abs_int(queen02.y - queen01.y):
            return True
    return False


class QueensBoard(object):

    board = []
    heuristic = 0
    @classmethod
    def add_queen(cls, queen):
        if isinstance(queen, Queen):
            cls.board.append(queen)

    @classmethod
    def calculate_heuristc(cls):
        i = 0
        j = 0
        n = len(cls.board)
        found_rival = False
        cls.heuristic = 0
        board = cls.board
        while i < n:
            board[i].heuristic = 0
            i += 1

        i = 0
        while i < n:
            j = i + 1
            while j < n and not found_rival:
                if queens_rivals(board[i], board[j]):
                    board[i].heuristic += 1
                    board[j].heuristic += 1
                    cls.heuristic += 1
                j += 1

            i += 1

    @classmethod
    def get_local_minimun(cls):
        i = 0
        j = 0
        board = cls.board
        n = len(board)

        index_to_change = 0
        heuristc_queen_beegin = 0
        heuristic_queen_final = 0

        while i < n:


class Queen(object):
    def __init__(self, posX = 0, posY = 0):
        self.x = posX
        self.y = posY
        self.heuristic
        QueensBoard.add_queen(self)



