import time
import copy


class Chess:
    def __init__(self):
        print('game start')
        self.white_list = ['Rw', 'Nw', "Bw", 'Qw', "Kw", "Pw"]
        self.black_list = ['Rb', 'Nb', "Bb", "Qb", "Kb", "Pb"]
        self.board = [
                      ['Rb', 'Nb', "Bb", 'Qb', "Kb", "Bb", "Nb", "Rb"],
                      ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["Pw", "Pw", "Pw", "Pw", "Pw", "Pw", "Pw", "Pw"],
                      ['Rw', 'Nw', "Bw", 'Qw', "Kw", "Bw", "Nw", "Rw"],
                      ]
    def legal(self,x1,y1,x2,y2):
        if 8>x1>-1 and 8>y1>-1 and 8>x2>-1 and 8>y2>-1:
            return False
        else:
            return True
    def legal_range(self,x):
        if 8>x[0]>-1 and 8>x[1]>-1:
            return True
        else:
            return False
    def __int__(self,board): # why i made this
        self.board = board

    def pair_piece_position(self,e):
        t = True
        first = second =False
        r1 =c1=r2=c2=0
        for i in range(0, 8):
            for j in range(0, 8):
                if t and self.board[i][j] == e:
                    r1 = i
                    c1 = j
                    t = False
                    first = True
                elif self.board[i][j] == e:
                    r2 = i
                    c2 = j
                    second = True
        return [first, r1, c1, second, r2, c2]

    def return_board(self):
        return self.board

    def set_board(self,board):
        self.board = board

    def check_destination(self,e,r1,c1,r2,c2,white):
        b = False
        if e != self.board[r1][c1]:
            return False
        if self.legal(r1,c1,r2,c2):
            return False
        if white:
            if self.board[r2][c2] == "":
                return True
            else:
                for x in self.black_list:
                    if self.board[r2][c2] == x:
                        b = True
                if b:
                    return True
                else:
                    return False

        else:  # black
            if self.board[r2][c2] == "":
                return True
            else:
                for x in self.white_list:
                    if self.board[r2][c2] == x:
                        b = True
                if b:
                    return True
                else:
                    return False

    def printpostion(self,r1,c1):
        p=self.board[r1][c1]
        return p

    def display(self):
        temp = copy.deepcopy(self.board)
        k = 8;
        z = ['  a ', 'b ', "c ", 'd ', "e ", "f ", "g ", "h "]
        print("\n", z)
        for i in range(0,8):
            for j in range(0,8):
                if temp[i][j] == "":
                    temp[i][j] = "  "

        for x in temp:
            print(k, x)
            k = k - 1



class King(Chess):
    def __init__(self):
        super(King, self).__init__()
        self.king_value = 200  # -----> infinity?
        self.king_moved = False

    def king_is_in_check(self, white=True):
        pass

    def king_castle_condition(self,r1,c1,r2,c2,white):  # what' scenes?
        if r1 == r2 and (c2 == c1-2 or c2 == c1+2) and ~self.king_moved:
            return True
        else:
            return False

    def get_king_position(self,white):
        rq=cq=9
        if white:
            e = "Kw"
        else:
            e = "Kb"

        for i in range(0, 8):
            try:
                cq = self.board[i].index(e)
                break
            except:
                pass
        rq = i
        return [rq,cq]

    def king_possible_moves(self,turn):
        k = "Kb"
        kx = 0
        if turn:
            k = "Kw"
            kx = 7
        x,y = self.get_king_position(turn) # king's position + (8 moves)
        # castling moves ,[x,y+2][x,y-2]
        m = []
        m.append([x,y])
        l = [[x-1,y+1],[x-1,y],[x-1,y-1],[x,y+1],[x,y-1],[x+1,y+1],[x+1,y],[x+1,y-1]]
        for i in l:
            if -1 < i[0] < 8 and -1 < i[1] < 8 and self.check_destination(k,x,y,i[0],i[1],turn):
                m.append([i[0],i[1]])
        l1 = [[x,y+2],[x,y-2]]
        if kx == x and ~self.king_moved:
            for i in l1:
                if self.legal_move_king(x, y, i[0], i[1], turn):
                    m.append([i[0], i[1]])

        return m

    def legal_move_king(self, r1, c1, r2, c2, white=True):
        if 8 > r1 > -1 and 8 > c1 > -1 and 8 > r2 > -1 and 8 > c2 > -1:
            if r1 == r2:  # checking if the move is legal
                if c2 == c1 + 1:
                    self.king_moved = True
                    return True
                elif c2 == c1 - 1:
                    self.king_moved = True
                    return True
                elif c2 == c1 - 2 or c2 == c1 + 2:
                    x = 0
                    r = "Rb"
                    if white:
                        x = 7
                        r = "Rw"
                    if ~self.king_moved:
                        b = True
                        if c2 == c1 - 2 and self.board[x][0] == r:
                            for i in range(1, 4):
                                if self.board[x][i] != "":
                                    b = False
                            return b
                        elif c2 == c1 + 2 and self.board[x][7] == r:
                            for i in range(5, 7):
                                if self.board[x][i] != "":
                                    b = False
                            return b
                else:
                    return False
            elif r1 - 1 == r2 or r1 + 1 == r2:
                if c2 == c1 + 1:
                    self.king_moved = True
                    return True
                elif c2 == c1:
                    self.king_moved = True
                    return True
                elif c2 == c1 - 1:
                    self.king_moved = True
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def checkByPawn(self,rq,cq,white): # list index out of range
        if white:
            if rq + 1 < 8 and cq - 1 > -1 and self.board[rq + 1][cq - 1] == ["Pb"]:
                return True
            elif rq + 1 < 8 and cq + 1 < 8 and self.board[rq + 1][cq + 1] == ["Pb"]:
                return True
            else:
                return False
        else:
            if 8 > rq - 1 > -1 and 8 > cq - 1 > -1 and self.board[rq - 1][cq - 1] == ["Pw"]:
                return True
            elif rq - 1 > -1 and cq + 1 < 8 and self.board[rq - 1][cq + 1] == ["Pw"]:
                return True
            else:
                return False


class Rook(Chess):
    def __init__(self):
        super().__init__()
        self.rook_value = 5

    def rook_destination(self,e,r1,c1,r2,c2,white):
        if self.legal_move_rook(r1,c1,r2,c2):
            if white:
                for x in self.white_list:
                    if self.board[r2][c2] == x:
                        return False
                return True
            else:
                for x in self.black_list:
                    if self.board[r2][c2] == x:
                        return False
                return True
        else:
            return False

    def legal_move_rook(self, r1, c1, r2, c2):
        if 8 > r1 > -1 and 8 > c1 > -1 and 8 > r2 > -1 and 8 > c2 > -1:
            if r1 == r2:
                if c2 > c1:
                    for i in range(c1+1, c2):
                        if self.board[r1][i] != "":
                            return False
                    return True
                elif c1 > c2:
                    for i in range(c2+1, c1):
                        if self.board[r1][i] != "":
                            return False
                    return True
                else:
                    return False

            elif c1 == c2:
                if r2 > r1:
                    for i in range(r1+1, r2):
                        if self.board[i][c1] != "":
                            return False
                    return True
                elif r1 > r2:
                    for i in range(r2+1, r1):
                        if self.board[i][c1] != "":
                            return False
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    def checkByRook(self,rq,cq,white=True):
        # check Rook
        e = "Rw"
        if white:
            e = "Rb"

        [rook1, rr1, rc1, rook2, rr2, rc2] = self.pair_piece_position(e)

        if rook1:
            return self.legal_move_rook(rr1, rc1, rq, cq)
        if rook2:
            return self.legal_move_rook(rr2, rc2, rq, cq)

    def rook_moves(self,n,x,y,turn):
        if n == "Qw" or n == "Rw":
            turn = True
        else:
            turn = False
        l = [x,y]
        l1 = l2 = l3 = l4 = []
        t1 = t2 = t3 = t4 = True
        for i in range(1,8):
            if y + i < 8 and t1:
                if self.rook_destination(n,x,y,x,y+i,turn) and self.legal_move_rook(x,y,x,y+i):
                    l1.append(x)
                    l1.append(y + i)
                else:
                    t1 = False
            if y - i > -1 and t2:
                if self.rook_destination(n, x, y, x, y - i, turn) and self.legal_move_rook(x, y, x, y - i):
                    l2.append(x)
                    l2.append(y - i)
                else:
                    t2 = False
            if x + i < 8 and t3:
                if self.rook_destination(n, x, y, x + i, y, turn) and self.legal_move_rook(x, y, x + i, y):
                    l3.append(x+i)
                    l3.append(y)
                else:
                    t3 = False
            if x - i > -1 and t4:
                if self.rook_destination(n, x, y, x - i, y, turn) and self.legal_move_rook(x, y, x - i, y):
                    l4.append(x-i)
                    l4.append(y)
                else:
                    t4 = False
        l.append(l1)
        l.append(l2)
        l.append(l3)
        l.append(l4)
        return l

    def rook_possible_moves(self,e,white):

        rook1, rr1, rc1, rook2, rr2, rc2 = self.pair_piece_position(e)
        l1 = []
        if rook1:
            l1 = self.rook_moves(e,rr1, rc1,True)
        if rook2:
            l1.extend(self.rook_moves(e,rr2, rc2,True))
        return l1


class Bishop(Chess):  # diagnol
    def __init__(self):
        super().__init__()
        self.bishop_value = 3

    def bishop_destination(self,e,r1,c1,r2,c2,white):
        if self.legal_move_bishop(r1,c1,r2,c2):
            if white:
                for x in self.white_list:
                    if self.board[r2][c2] == x:
                        return False
                return True
            else:
                for x in self.black_list:
                    if self.board[r2][c2] == x:
                        return False
                return True
        else:
            return False

    def legal_move_bishop(self, r1, c1, r2, c2):
        if 8 > r1 > -1 and 8 > c1 > -1 and 8 > r2 > -1 and 8 > c2 > -1:

            if abs(r1 - r2) != abs(c1 - c2):
                return False
            if r2 > r1:
                if c2 > c1:
                    for i in range(1, r2 - r1):
                        if self.board[r1 + i][c1 + i] != "":
                            return False
                    return True
                elif c2 < c1:
                    for i in range(1, r2 - r1):
                        if self.board[r1 + i][c1 - i] != "":
                            return False
                    return True
            elif r2 < r1:
                if c2 < c1:
                    for i in range(1, r1 - r2):
                        if self.board[r1 - i][c1 - i] != "":
                            return False
                    return True
                elif c2 > c1:
                    for i in range(1, r1 - r2):
                        if self.board[r1 - i][c1 + i] != "":
                            return False
                    return True
        else:
            return False

    def checkByBishop(self,rq,cq,white=True):
        if white:
            e = "Bb"
        else:
            e = "Bw"
        [bishop1, rb1, cb1, bishop2, rb2, cb2] = self.pair_piece_position(e)

        if bishop1:
            return self.legal_move_bishop(rb1, cb1, rq, cq)
        if bishop2:
            return self.legal_move_bishop(rb2, cb2, rq, cq)

    def bishop_moves(self,b,x,y,turn):
        l = [x,y]
        l1 = l2 = l3 = l4 = []
        t1 = t2 = t3 = t4 = True
        for i in range(1,8):
            if x + i < 8 and y + i < 8 and t1:
                if self.bishop_destination(b,x,y,x+i,y+i,turn):
                    l1.append(x + i)
                    l1.append(y+i)
                else:
                    t1 = False
            if x+i<8 and y-i>-1 and t2:
                if self.bishop_destination(b, x, y, x + i, y - i, turn):
                    l2.append(x+i)
                    l2.append(y-i)
                else:
                    t2 = False
            if x-i>-1 and y + i < 8 and t3:
                if self.bishop_destination(b, x, y, x - i, y + i, turn):
                    l3.append(x - i)
                    l3.append(y+i)
                else:
                    t3 = False
            if x-i>-1 and y-i>-1 and t4:
                if self.bishop_destination(b, x, y, x - i, y - i, turn):
                    l4.append(x - i)
                    l4.append(y - i)
                else:
                    t4 = False
        l.append(l1)
        l.append(l2)
        l.append(l3)
        l.append(l4)
        return l

    def bishop_possible_moves(self,e,white):

        [bishop1, rb1, cb1, bishop2, rb2, cb2] = self.pair_piece_position(e)
        l1 = []
        if bishop1:
            l1 = self.bishop_moves(e,rb1,cb1,white)
        if bishop2:
            l1.extend(self.bishop_moves(e,rb2,cb2,white))
        return l1


class Queen(Rook,Bishop):
    def __init__(self):
        super().__init__()
        self.queen_value = 9

    def priority_save_queen(self):
        # if king is not in check or or or
        pass

    def legal_move_queen(self, r1, c1, r2, c2):

        return self.legal_move_rook(r1, c1, r2, c2) or self.legal_move_bishop(r1, c1, r2, c2)

    def checkByQueen(self, rq, cq, white=True):
        e = "Qw"
        if white:
            e = "Qb"
        count = 0
        q_positions = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == e:
                    r1 = i
                    c1 = j
                    q_positions.append([r1,c1])
                    count = count + 1

        for i in range(0, count):
            return self.legal_move_queen(rq,cq,q_positions[i][0],q_positions[i][1])

    def queen_possible_moves(self,turn):
        e = "Qb"
        if turn:
            e = "Qw"
        count = 0
        q_positions = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == e:
                    r1 = i
                    c1 = j
                    q_positions.append([r1,c1])
                    count = count + 1

        l1 = l2 =[]
        for i in range(0,count):
            l1 = l1 + self.bishop_moves(e,q_positions[i][0],q_positions[i][1],turn)
            l2 = l2 + self.rook_moves(e,q_positions[i][0],q_positions[i][1],turn)

        return l1 + l2


class Knight(Chess):
    def __init__(self):
        super().__init__()
        self.knight_value = 3

    def legal_move_knight(self, r1, c1, r2, c2):
        if 8 > r1 > -1 and 8 > c1 > -1 and 8 > r2 > -1 and 8 > c2 > -1:

            if r1 - 1 == r2:
                if c1 + 2 == c2:
                    return True
                elif c1 - 2 == c2:
                    return True
                else:
                    return False
            elif r1 + 1 == r2:
                if c1 + 2 == c2:
                    return True
                elif c1 - 2 == c2:
                    return True
                else:
                    return False
            elif r1 - 2 == r2:
                if c1 + 1 == c2:
                    return True
                elif c1 - 1 == c2:
                    return True
                else:
                    return False
            elif r1 + 2 == r2:
                if c1 + 1 == c2:
                    return True
                elif c1 - 1 == c2:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def checkByKnight(self, rq, cq, white):
        # check Rook
        e = "Nw"
        if white:
            e = "Nb"

        [kn1, rr1, rc1, kn2, rr2, rc2] = self.pair_piece_position(e)

        if kn1:
            return self.legal_move_rook(rr1, rc1, rq, cq)
        if kn2:
            return self.legal_move_rook(rr2, rc2, rq, cq)

    def Knight_moves(self,x,y,turn):
        n = "Nb"
        if turn:
            n = "Nw"
        l = []
        l.append(x)
        l.append(y)
        if x-2>-1 and y+1<8 and self.check_destination(n,x,y,x-2,y+1,turn):
            l.append(x-2)
            l.append(y+1)
        if x-2>-1 and y-1>-1 and self.check_destination(n,x,y,x-2,y-1,turn):
            l.append(x-2)
            l.append(y-1)
        if x+2<8 and y+1<8 and self.check_destination(n,x,y,x+2,y+1,turn):
            l.append(x+2)
            l.append(y+1)
        if x+2<8 and y-1>-1 and self.check_destination(n,x,y,x+2,y-1,turn):
            l.append(x+2)
            l.append(y-1)
        if x-1>-1 and y+2<8 and self.check_destination(n,x,y,x-1,y+2,turn):
            l.append(x-1)
            l.append(y+2)
        if x-1>-1 and y-2>-1 and self.check_destination(n,x,y,x-1,y-2,turn):
            l.append(x-1)
            l.append(y-2)
        if x+1<8 and y+2<8 and self.check_destination(n,x,y,x+1,y+2,turn):
            l.append(x + 1)
            l.append(y + 2)
        if x+1<8 and y-2>-1 and self.check_destination(n,x,y,x+1,y-2,turn):
            l.append(x + 1)
            l.append(y - 2)
        return l

    def knight_possible_moves(self,white):
        e = "Nb"
        if white:
            e = "Nw"
        m_list = []
        [kn1, rr1, rc1, kn2, rr2, rc2] = self.pair_piece_position(e)
        if kn1:
            l1 = self.Knight_moves(rr1,rc1,white)
            m_list.append(l1)
        if kn2:
            l2 = self.Knight_moves(rr2,rc2,white)
            m_list.append(l2)
        return m_list


class Pawn(Chess):
    def __init__(self):
        super().__init__()
        self.pawn_value = 1

    def pawn_destiny(self,r2,c2,turn):
        b = True
        if self.board[r2][c2] == "":
            return False
        else:
            if turn:
                for x in self.white_list:
                    if self.board[r2][c2] == x:
                        return False
                return True
            else:
                for x in self.black_list:
                    if self.board[r2][c2] == x:
                        return False
                return True


    def legal_move_pawn(self, r1, c1, r2, c2, white):
        if 8 > r1 > -1 and 8 > c1 > -1 and 8 > r2 > -1 and 8 > c2 > -1:
            if c1 == c2:  # pawn ahead is block (blocked pawn) #c1==c2
                if self.board[r2][c2] != "":
                    return False
            if white:
                #print("pawn white")
                if r1 == 6:
                    if r2 == r1 - 2 and c1 == c2:
                        return True
                   # elif r2 == r1 - 1 and c1 == c2: #or c1 + 1 == c2 or c1 - 1 == c2):
                    #    return True
                    else:
                        if r2 == r1 - 1:
                            if c1 == c2:  # or
                                return True
                            elif self.board[r2][c2] != "" and (c1 + 1 == c2 or c1 - 1 == c2):
                                return True
                            else:
                                return False
                        return False
                else:
                    if r2 == r1 - 1:
                        if c1 == c2: #or
                            return True
                        elif self.board[r2][c2]!="" and (c1 + 1 == c2 or c1 - 1 == c2):
                            return True
                        else:
                            return False

            else:
                if r1 == 1:
                    if r2 == r1 + 2 and c1 == c2:
                        return True
                    elif r2 == r1 + 1 and c1 == c2:  # or ):
                        return True
                    elif self.board[r1][c1] != "" and (c1 + 1 == c2 or c1 - 1 == c2):
                        return True
                    else:
                        return False
                else:
                    if r2 == r1 + 1:
                        if c1 == c2: # or c1 + 1 == c2 or c1 - 1 == c2:
                            return True
                        elif self.board[r1][c1]!="" and (c1 + 1 == c2 or c1 - 1 == c2):
                            return True
                        else:
                            return False
        else:
            return False

    def pawns_possible_moves(self,turn):
        if turn:
            e = "Pw"
            x = 6
            s = -1
        else:
            e = "Pb"
            x = 1
            s = 1

        possible_moves = []
        for i in range(0,8):
            l = []
            if self.board[x][i] == e:
                l = l + [x, i]
                l1 = [x+2*s,i,x+s,i]
                for k in range(0,2):
                    if self.board[l1[2*k]][l1[1 + 2*k]] == "":
                        l = l + [l1[2*k],l1[1 + 2*k]]
                if i-1>-1 and self.pawn_destiny(x+s,i-1,turn):
                    l.append(x+s)
                    l.append(i-1)
                if i+1<8 and self.pawn_destiny(x+s,i+1,turn):
                    l.append(x+s)
                    l.append(i+1)
                possible_moves.append(l)
            if turn:
                for i in range(5, -1,-1):
                    for j in range(0, 8):
                        l = []
                        if self.board[i][j] == e and self.board[i+s][j] == "":
                            l.append(i)
                            l.append(j)
                            l.append(i + s)
                            l.append(j)
                            if j - 1 > -1 and self.pawn_destiny(i+s,j-1,turn):
                                l.append(i + s)
                                l.append(j - 1)
                            if j + 1 < 8 and self.pawn_destiny(i+s,j+1,turn):
                                l.append(i + s)
                                l.append(j + 1)
                            possible_moves.append(l)
            else:
                for i in range(2, 8):
                    for j in range(0, 8):
                        l = []
                        if self.board[i][j] == e and self.board[i+s][j] == "":
                            l.append(i)
                            l.append(j)
                            l.append(i + s)
                            l.append(j)
                            if j - 1 > -1 and self.pawn_destiny(i+s,j-1,turn):
                                l.append(i + s)
                                l.append(j - 1)
                            if j + 1 < 8 and self.pawn_destiny(i+s,j+1,turn):
                                l.append(i + s)
                                l.append(j + 1)
                            possible_moves.append(l)

        return possible_moves


class GameObject(King,Queen,Knight,Pawn):
    def __init__(self):
        super(GameObject, self).__init__()

    def pawn_promotion(self, e,r1, c1, r2, c2, white):
        if white:
            if r1 == 1 and e == "Pw":
                self.board[r1][c1] = ""
                self.board[r2][c2] = "Qw"
                return False
            else:
                return True
        else:  # black
            if r1 == 6 and e == "Pb":
                self.board[r1][c1] = ""
                self.board[r2][c2] = "Qb"
                return False
            else:
                return True

    def castling(self,e, r1, c1, r2, c2, white=True):

        if r1 == r2 and (c2 == c1-2 or c2 == c1+2) and (e=="Kb"or e == "Kw"):
            x = 0
            r = "Rb"
            k = "Kb"
            if white:
                x = 7
                r = "Rw"
                k = "Kw"
            if c2 == c1 - 2:
                self.board[x][3] = r
                self.board[x][0] = ""
                self.board[r2][c2] = k
                self.board[r1][c1] = ""
                return False

            elif c2 == c1 + 2:
                self.board[x][5] = r
                self.board[x][7] = ""
                self.board[r2][c2] = k
                self.board[r1][c1] = ""
                return False

        else:
            return True

    def move(self, e, r1, c1, r2, c2, white=True):
        if self.pawn_promotion(e, r1, c1, r2, c2, white) and self.castling(e, r1, c1, r2, c2, white):
             #print(e,r1,c1,r2,c2,white)
             self.board[r1][c1] = ""
             self.board[r2][c2] = e
        #self.display()

    def copyBoard(self):
        temp_board = copy.deepcopy(self.board)
        return temp_board

    def undo(self,temp):
        self.board = temp  # see see
        #self.display()

    def rescueKing(self):
        # han han bhai rescue karo
        kb = False
        kw = False
        for i in range(0,8):
            for j in range(0, 8):
                if self.board[i][j] == "Kw":
                    kw =True
                elif self.board[i][j] == "Kb":
                    kb = True
        return kw and kb

    def check_check(self,turn):
        [rq,cq] = self.get_king_position(turn)
        if self.checkByPawn(rq,cq,turn):
            return True
        elif self.checkByQueen(rq,cq,turn):
            return True
        elif self.checkByKnight(rq,cq,turn):
            return True
        elif self.checkByRook(rq,cq,turn):
            return True
        elif self.checkByBishop(rq,cq,turn):
            return True
        else:
            return False

    def cost_evaluation(self):
        cost = 0
        for i in range(0,8):
            for j in range(0,8):
                if self.board[i][j] == "Qb":
                    cost = cost + 9
                elif self.board[i][j] == "Kb":
                    cost = cost + 200
                elif self.board[i][j] == "Rb":
                    cost = cost + 5
                elif self.board[i][j] == "Bb":
                    cost = cost + 3
                elif self.board[i][j] == "Nb":
                    cost = cost + 3
                elif self.board[i][j] == "Pb":
                    cost = cost + 1
                elif self.board[i][j] == "Kw":
                     cost = cost - 200
                elif self.board[i][j] == "Qw":
                    cost = cost - 9
                elif self.board[i][j] == "Rw":
                    cost = cost - 5
                elif self.board[i][j] == "Bw":
                    cost = cost - 3
                elif self.board[i][j] == "Nw":
                    cost = cost - 3
                elif self.board[i][j] == "Pw":
                    cost = cost - 1
        return cost


class GameInterface:
    def __init__(self):
        self.c = GameObject()
        self.turn_white = True
        self.c.display()
        self.move_count = 0
    def deep_board(self):
        return self.c.copyBoard()
    def gameTurn(self):
        if self.turn_white:
            print("w-------->B")
            self.turn_white = False
        else:
            print("B-------->W")
            self.turn_white = True
    def returnTurn(self):
        return self.turn_white

    def check_legal(self,e,r1,c1,r2,c2):
        #print("legal legal legal")
        d = self.c.check_destination(e,r1,c1,r2, c2, self.turn_white)  #check destintion
        if e == "Kw" or e == "Kb":
            return self.c.legal_move_king(r1, c1, r2, c2, self.turn_white) and d
        elif e == "Qw" or e == "Qb":
            return self.c.legal_move_queen(r1, c1, r2, c2) and d
        elif e == "Pw" or e == "Pb":
            return self.c.legal_move_pawn(r1, c1, r2, c2, self.turn_white) and d
        elif e == "Bw" or e == "Bb":
            return self.c.legal_move_bishop(r1, c1, r2, c2) and d
        elif e == "Nw" or e == "Nb":
            return self.c.legal_move_knight(r1,c1,r2,c2) and d
        elif e == "Rw" or e == "Rb":
            return self.c.legal_move_rook(r1,c1,r2,c2) and d
        else:
            print(".........../")

    def alliswell(self):
        return self.c.rescueKing()

    def input(self, e, p1, p2):
        c1 = ord(p1[0]) - 97  # y1 nested list
        r1 = int(p1[1]) - 1  # x1 list
        r1 = abs(7-r1)
        c2 = ord(p2[0]) - 97  # y2
        r2 = int(p2[1]) - 1  # x2
        r2 = abs(7-r2)
        temp_board = self.c.copyBoard()
        if self.check_legal(e,r1,c1,r2,c2):
            self.c.move(e,r1,c1,r2,c2,True)
            if self.c.check_check(True):
                self.c.undo(temp_board)
                self.c.display()
                print("ILLEGAL MOVE")
                return True
            else:
                self.c.display()
                self.move_count = self.move_count + 1
                print("situation no " ,self.move_count," : ",e,p1,p2,True)
                #self.gameTurn()
                return False
        else:
            return True

    def inputAiMove(self,e, r1, c1, r2, c2):
        b =self.c.copyBoard()
        self.c.move(e, r1, c1, r2, c2, False)
        self.c.display()







