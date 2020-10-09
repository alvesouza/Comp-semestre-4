from math import *
import random

class Direction(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Direction(self.x*other, self.y*other)
        else:
            raise TypeError("Error, should be multiplied by float or int")

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def turn_unit(self):
        s = sqrt(self.x*self.x + self.y*self.y)
        if s > 0:
            self.x /= s
            self.y /= s

class Ponto(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
        self.value = funcao(x, y)

    def __add__(self, other):
        if isinstance(other, Direction):
            return Ponto(x = self.x+other.x, y = self.y+other.y)
        else:
            raise TypeError("Error, should be added by Direction")

    def __sub__(self, other):
        if isinstance(other, Direction):
            return Ponto(x = self.x - other.x, y= self.y - other.y)
        else:
            raise TypeError("Error, should be subbed by Direction")

    def __str__(self):
        return "({0}, {1}) value = {2}".format(self.x, self.y, self.value)

def funcao(x, y):
    x2 = x*x
    y2 = y*y
    x__3 = x - 3
    x__3 = x__3*x__3
    x_3 = x + 3
    x_3 = x_3*x_3
    y__3 = y - 3
    y__3 = y__3*y__3
    y_3 = y + 3
    y_3 = y_3*y_3
    return 4*exp(-(x2 + y2 - 2*(x+y-1))) + exp(-(x__3 + y__3)) + exp(-(x_3 +
                                                                       y__3)) + exp(-(x__3 + y_3)) + exp(-(x_3 + y_3))

def funcao_dx(x, y):
    x2 = x*x
    y2 = y*y
    x__3 = x - 3
    x__3_2 = x__3*x__3
    x_3 = x + 3
    x_3_2 = x_3*x_3
    y__3 = y - 3
    y__3_2 = y__3*y__3
    y_3 = y + 3
    y_3_2 = y_3*y_3
    return -8*(x-1)*exp(-(x2 + y2 - 2*(x+y-1))) - 2*x__3*(exp(-(x__3_2 + y__3_2)) + exp(-(
            x__3_2 + y_3_2))) - 2*x_3*(exp(-(x_3_2 + y__3_2)) + exp(-(x_3_2 + y_3_2)))


def funcao_dy(x, y):
    x2 = x*x
    y2 = y*y
    x__3 = x - 3
    x__3_2 = x__3*x__3
    x_3 = x + 3
    x_3_2 = x_3*x_3
    y__3 = y - 3
    y__3_2 = y__3*y__3
    y_3 = y + 3
    y_3_2 = y_3*y_3
    return -8*(y-1)*exp(-(x2 + y2 - 2*(x+y-1))) - 2*y__3*(exp(-(x__3_2 + y__3_2)) + exp(-(x_3_2 + y__3_2))
                                                          ) - 2*y_3*(exp(-(x__3_2 + y_3_2)) + exp(-(x_3_2 + y_3_2)))

def decision(probability):
    return random.random() < probability

class EncontraMaximos(object):
    def __init__(self, max_turns = 10000, solve_times = 100):
        self.points_maximum = []
        self.times_solve = solve_times
        self.max_turn = max_turns
        self.max_point = Ponto(0, 0)
        self.point = Ponto(0, 0)
        self.direction = Direction(0, 0)
        self.direction.turn_unit()
        self.turn = 0
        self.probability_half_life = 2000
        self.probability_half_exp_const = -log(2)/self.probability_half_life
        self.probability_minimum = 0.1
        # self.probability_half_const = 1

        self.distance_half_life = 100
        self.distance_half_exp_const = -log(2)/self.distance_half_life
        self.distance_const = 200
        self.distance_minimum = 0.0001

    def distance_function(self):
        distance = self.distance_const*exp(self.distance_half_exp_const*self.turn)*random.random()
        if distance > self.distance_minimum:
            return distance
        return self.distance_minimum

    def probability_function(self):
        probability = exp(self.probability_half_exp_const*self.turn)
        # print("Probability ", probability)
        if probability > self.probability_minimum:
            return probability

        return self.probability_minimum

    def solve_once(self):
        # print("Begin Valor ", self.point.value)
        while self.turn < self.max_turn:
            self.direction.x = funcao_dx(self.point.x, self.point.y)
            self.direction.y = funcao_dy(self.point.x, self.point.y)
            probability = self.probability_function()
            decide = decision(probability)
            # print(decide)
            if self.direction.x == 0 and self.direction.y == 0:
                if decide or decision(0.5):
                    self.direction.x = 0.5 - random.random()
                    self.direction.y = 0.5 - random.random()
                    # print("direction = ", self.direction)
                # elif decision(0.5):
                #     self.direction.x = 0.5 - random.random()
                #     self.direction.y = 0.5 - random.random()
                #     print("direction = ", self.direction)

            self.direction.turn_unit()
            point_next = self.point + self.direction*self.distance_function()
            # print(point_next)
            if point_next.value > self.point.value:
                self.point = point_next
                if self.point.value > self.max_point.value:
                    self.max_point = self.point
                # print("Turn ", self.turn, " Valor ", self.point.value)
                # print(self.point)
            elif decide:
                self.point = point_next
                if decision(0.1):
                    self.point = self.max_point
                # print("Turn ", self.turn, " Valor ", self.point.value)
                # print(self.point)
            elif probability == self.probability_minimum:
                if decision(0.1):
                    self.point = self.max_point
                elif decision(0.5):
                    self.point = Ponto(self.point.x + 20*(0.5 - random.random()), self.point.y +
                                       20*(0.5 - random.random()))
                # print("Turn ", self.turn, " Valor ", self.point.value)
                # print(self.point)
            self.turn += 1

    def solve_times(self):
        i = 0
        while i < self.times_solve:
            self.solve_once()
            self.point = Ponto(100*(0.5 - random.random()),100*(0.5 - random.random()))
            print("inicio ",self.point)
            self.points_maximum.append(self.max_point)
            self.max_point = self.point
            self.turn = 0
            i += 1

        i = 0

        while i < self.times_solve:
            print(self.points_maximum[i])
            print("derivada x = ", funcao_dx(self.points_maximum[i].x, self.points_maximum[i].y),
                  " y = ", funcao_dy(self.points_maximum[i].x, self.points_maximum[i].y))
            i += 1

if __name__ == '__main__':
    # print("Valor ", funcao(1, 1))
    solver = EncontraMaximos(max_turns=1000)
    solver.solve_times()
