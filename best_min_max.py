import math
import time
from operator import itemgetter
import threading
import chess_game as w
from chess_game import GameObject, GameInterface
import copy
import multiprocessing as mp
from multiprocessing import Pool
import random

class Moves(GameObject):
    def __init__(self, board):
        super(Moves, self).__init__()
        self.temp_obj = GameObject()
        self.board = board

    def check_check(self, turn):
        [rq, cq] = self.get_king_position(turn)
        if self.checkByPawn(rq, cq, turn):
            return True
        elif self.checkByQueen(rq, cq, turn):
            return True
        elif self.checkByKnight(rq, cq, turn):
            return True
        elif self.checkByRook(rq, cq, turn):
            return True
        elif self.checkByBishop(rq, cq, turn):
            return True
        else:
            return False

    def knight_action(self, turn):
        e = "Nb"
        if turn:
            e = "Nw"
        p = []
        m = self.knight_possible_moves(turn)
        for i in range(0, len(m)):
            x = m[i][0]
            y = m[i][1]
            if len(m[i]) > 2:
                for j in range(0, len(m[i]) - 2, 2):
                    x1 = m[i][2 + j]
                    y1 = m[i][3 + j]
                    b = self.copyBoard()
                    self.temp_obj.undo(b)
                    self.temp_obj.move(e, x, y, x1, y1)
                    if self.temp_obj.check_check(turn):
                        pass
                    else:
                        c = self.temp_obj.cost_evaluation()
                        p.append([e, [x, y], [x1, y1], c])
        return p

    def action_list(self, e, m, turn):
        p = []
        for i in range(0, int(len(m) / 6)):
            x = m[0 + i * 6]
            y = m[1 + i * 6]
            for j in range(2, 6):
                l = m[j + 6 * i]
                for k in range(0, len(l), 2):
                    x1 = l[0 + k]
                    y1 = l[1 + k]
                    b = self.copyBoard()
                    self.temp_obj.undo(b)
                    self.temp_obj.move(e, x, y, x1, y1)
                    if self.temp_obj.check_check(turn):
                        pass
                    else:
                        c = self.temp_obj.cost_evaluation()
                        p.append([e, [x, y], [x1, y1], c])

        return p

    def bishop_action(self, turn):
        e = "Bb"
        if turn:
            e = "Bw"
        m = self.bishop_possible_moves(e, turn)
        p=self.action_list(e, m, turn)
        return p

    def rook_action(self, turn):
        e = "Rb"
        if turn:
            e = "Rw"
        m = self.rook_possible_moves(e, turn)

        p = self.action_list(e, m, turn)
        return p

    def queen_action(self, turn):
        e = "Qb"
        if turn:
            e = "Qw"
        m = self.queen_possible_moves(turn)
        p = []
        for i in range(0, int(len(m) / 12)):
            l = m[i * 12:12 + 12 * i]
            p = p + self.action_list(e, l, turn)
        return p

    def pawn_action(self, turn):
        e = "Pb"
        if turn:
            e = "Pw"
        p = []
        m = self.pawns_possible_moves(turn)
        length = len(m)
        for i in range(0, length):
            x = m[i][0]
            y = m[i][1]
            for j in range(2, len(m[i]), 2):
                x1 = m[i][j]
                y1 = m[i][j + 1]
                b = self.copyBoard()
                self.temp_obj.undo(b)
                self.temp_obj.move(e, x, y, x1, y1)
                if self.temp_obj.check_check(turn):
                    pass
                else:
                    c = self.temp_obj.cost_evaluation()
                    p.append([e, [x, y], [x1, y1], c])

        return p

    def king_action(self, turn):
        e = "Kb"
        if turn:
            e = "Kw"
        p = []
        m = self.king_possible_moves(turn)
        x = m[0][0]
        y = m[0][1]
        for i in range(1, len(m)):
            x1 = m[i][0]
            y1 = m[i][1]
            b = self.copyBoard()
            self.temp_obj.undo(b)
            self.temp_obj.move(e, x, y, x1, y1)
            if self.temp_obj.check_check(turn):
                pass
            else:
                c = self.temp_obj.cost_evaluation()
                p.append([e, [x, y], [x1, y1], c])
        return p

    def total_action(self, turn):
        q = self.queen_action(turn)
        n = self.knight_action(turn)
        bs = self.bishop_action(turn)
        r = self.rook_action(turn)
        p = self.pawn_action(turn)
        k = self.king_action(turn)
        t = p + r + q + n + bs + k

        return t



class AI_move():

    def __init__(self):
        self.temp = GameObject()
        self.b = []  # board
        self.movesObj = Moves(self.b)
        self.turn = False
    def set_board(self,board):
        self.b = board
    def best_min_max(self,a):
        tempG = GameObject()
        # depth = 1
        tempo = copy.deepcopy(self.b)
        tempG.set_board(tempo)
        tempG.move(a[0], a[1][0], a[1][1], a[2][0], a[2][1], False)
        value = -math.inf
        move = [0,[],[],value]
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l2 = m.total_action(True)
        try:
            b = sorted(l2, key=itemgetter(3), reverse=False)[0]  # F
        except:
            return move

        #print("l2",l2)
        tempo1 = tempG.copyBoard()
        tempG.move(b[0], b[1][0], b[1][1], b[2][0], b[2][1], True)
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l3 = m.total_action(False)
        if len(l3) == 0:
            return move
        try:
            c = sorted(l3, key=itemgetter(3), reverse=True)[0]
        except:
            return move
        #print("l3",l3)
        tempo2 = tempG.copyBoard()
        tempG.move(c[0], c[1][0], c[1][1], c[2][0], c[2][1], False)
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l4 = m.total_action(True)
        try:
            d = sorted(l4, key=itemgetter(3), reverse=False)[0]  # F
        except:
            return move
        #print("l4",l4)
        tempo3 = tempG.copyBoard()
        tempG.move(d[0], d[1][0], d[1][1], d[2][0], d[2][1], True)
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l5 = m.total_action(False)
        try:
            e = sorted(l5, key=itemgetter(3), reverse=True)[0]  # T
        except:
            return move
        tempo4 = tempG.copyBoard()
        tempG.move(e[0], e[1][0], e[1][1], e[2][0], e[2][1], False)
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l6 = m.total_action(False)
        try:
            f = sorted(l6, key=itemgetter(3), reverse=False)[0]  # F
        except:
            return move

        tempo5 = tempG.copyBoard()
        tempG.move(f[0], f[1][0], f[1][1], f[2][0], f[2][1], True)
        b2 = tempG.copyBoard()
        m = Moves(b2)
        l7 = m.total_action(False)
        try:
            f = sorted(l7, key=itemgetter(3), reverse=True)[0]  # T
        except:
            return move
        #print("l5",l5)
        tempG.undo(tempo5)
        tempG.undo(tempo4)
        tempG.undo(tempo3)
        tempG.undo(tempo2)
        tempG.undo(tempo1)
        tempG.undo(tempo)
        return f+a


if __name__ == '__main__':
    g = GameInterface()
    while True:
        white_play = True
        while white_play:
            p = input('Enter the piece:')
            xi = input('Enter piece initial position:')
            xf = input('Enter piece final position:')
            white_play = g.input(p,xi,xf)
            if white_play:
                print("Enter correct inputs")
        ########
        b = g.deep_board()
        m = Moves(b)
        t = m.total_action(False)
        print(t)
        if len(t) == 0:
            print("CHECKMATE")
            break
        else:
            a = AI_move()
            a.set_board(b)
            start = time.time()
            pool = Pool(mp.cpu_count())
            outputs_async = pool.map_async(a.best_min_max, t)
            outputs = outputs_async.get()
            # print("Output: {}".format(outputs))
            moves = sorted(outputs, key=itemgetter(3), reverse=True)
            move_list = []
            for x in moves:
                if moves[0][3] == x[3]:
                    move_list.append(x)
            random.shuffle(move_list)
            move = move_list[0]
            # print(outputs)
            # print(move[0],move[1][0])
            end = time.time()
            print("time", end - start)
            print('move',move)
            # print(move[4], move[5][0], move[5][1], move[6][0], move[6][1])
            g.inputAiMove(move[4], move[5][0], move[5][1], move[6][0], move[6][1])

