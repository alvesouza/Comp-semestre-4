
class Queen():
    def __init__(self, i, j):
        self.i = i
        self.j = j

class Casa():
    def __init__(self, i, j):
        self.queen = None
        self.value = 0
        self.last_round = 0
        self.i = i
        self.j = j

def abs_int(x):
    if x > 0:
        return x
    return -x

def rivals_casa(casa, queen):
    if casa.j == queen.j or (abs_int(queen.i - casa.i) == abs_int(queen.j - casa.j)):
        return True
    return False

class Board(object):
    def __init__(self, n):
        self.board = []
        self.queens = []
        self.heuristic = 0
        self.round = 0
        for j in range(n):
            self.board.append([])
            for i in range(n):
                self.board[j].append(Casa(i, j))

        for i in range(n):
            self.queens.append(Queen(i, 0))
            self.board[0][i].queen = self.queens[i]
        self.casa_minimum = self.board[0][0]

    def calculate_heuristics_values(self):
        n = len(self.board)
        i = 0
        # j = 0
        x_spot = 0
        # y_spot = 0
        self.casa_minimum = self.board[0][0]
        # heuristic = 0
        while x_spot < n:
            y_spot = 0
            while y_spot < n:

                i = 0
                heuristic = 0
                while i < n:
                    j = i+1
                    while j < n:
                        # if i == j:
                        #     j += 1
                        #     continue
                        if x_spot == i:
                            if rivals_casa(self.board[y_spot][x_spot], self.queens[j]):
                                heuristic += 1
                        elif x_spot == j:
                            if rivals_casa(self.board[y_spot][x_spot], self.queens[i]):
                                heuristic += 1
                        elif rivals_casa(self.queens[i], self.queens[j]):
                            heuristic += 1

                        j += 1
                    i += 1

                self.board[y_spot][x_spot].value = heuristic
                if self.casa_minimum.queen is not None:
                    if self.board[y_spot][x_spot].queen is None:
                        self.casa_minimum = self.board[y_spot][x_spot]
                elif self.board[y_spot][x_spot].value < self.casa_minimum.value:
                    self.casa_minimum = self.board[y_spot][x_spot]
                elif self.board[y_spot][x_spot].value == self.casa_minimum.value and (
                        self.casa_minimum.last_round > self.board[y_spot][x_spot].last_round):
                    self.casa_minimum = self.board[y_spot][x_spot]
                y_spot += 1
            x_spot += 1
        self.heuristic = self.board[self.queens[0].j][self.queens[0].i].value

    def change_queen(self):
        i = self.casa_minimum.i
        j = self.casa_minimum.j

        queen_minimum = self.queens[i]
        self.board[queen_minimum.j][queen_minimum.i].queen = None
        self.board[queen_minimum.j][queen_minimum.i].last_round = self.round
        queen_minimum.i = i
        queen_minimum.j = j
        self.round += 1
        self.board[j][i].queen = queen_minimum
        self.board[j][i].last_round = self.round
        self.calculate_heuristics_values()

    def print_board(self):
        i = 0
        j = 0
        n = len(self.board)
        print("Heuristica: ", self.heuristic)
        while j < n:
            i = 0
            while i < n:
                if self.board[j][i].queen:
                    print("Q", end=" ")
                else:
                    print(self.board[j][i].value, end=' ')
                i += 1

            print("")
            j += 1

    def solve_game(self):
        self.calculate_heuristics_values()

        while self.heuristic != 0:
            # self.print_board()
            self.change_queen()

        self.print_board()


if __name__ == '__main__':
    game = Board(10)
    game.solve_game()
