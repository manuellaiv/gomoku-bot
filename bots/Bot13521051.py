import random
import time
from game import Board
import globals as globals

class Bot13521051(object):
    """
    Bot player
    """

    def __init__(self):
        self.player = None

        """
            TODO: Ganti dengan NIM kalian
        """
        self.NIM = "13521051"

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):

        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        while move == -1 or move not in board.availables:
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)
    
    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
        """
        chosen = self.choose_loc(board)
        x = chosen[0]
        y = chosen[1]
        return f"{x},{y}"
    
    def choose_loc(self, board:Board) -> list[int]:
        if not board.availables:
            return []
        chosen = board.move_to_location(random.choice(board.availables))
        val = -1
        for i in range(board.height):
            for j in range(board.width):
                loc = board.location_to_move([i,j])
                # print(i,j,self.consecutive_opponent(i,j,board),self.consecutive_self(i,j,board))
                val_opp = self.list_val(self.consecutive_opponent(i,j,board))
                val_self = self.list_val_self(self.consecutive_self(i,j,board))
                if ((board.states.get(loc) is None) and 1.5*val_opp+val_self > val):
                    chosen = [i,j]
                    val = 1.5*val_opp+val_self
        return chosen

    def list_val(self, l:list[list[list[int]]]) -> int:
        val = 0
        for i in range(len(l)):
            val = val + len(l[i])*len(l[i])
        return val
    
    def list_val_self(self, l:list[list[list[int]]]) -> int:
        val = 0
        for i in range(len(l)):
            if len(l[i]) == 4:
                val = val + 999999
            else:
                val = val + len(l[i])*len(l[i])
        return val

    def consecutive_self(self, i:int, j: int, board: Board) -> list[list[int]]:
        list_con = []
        limit_down = -1
        limit_up = -1
        limit_right = -1
        limit_left = -1

        # check vertically
        # down
        list_conv = []
        if (self.valid_idx(i-1,j,board) and board.states.get(board.location_to_move([i-1,j])) == self.player):
            exist = True
            i_iterate = i-1
            while (exist and self.valid_idx(i_iterate,j,board)):
                if board.states.get(board.location_to_move([i_iterate,j])) == self.player:
                    list_conv.append([i_iterate,j])
                else:
                    exist = False
                i_iterate -= 1
            limit_down = i_iterate

        # up
        if self.valid_idx(i+1,j,board) and board.states.get(board.location_to_move([i+1,j])) == self.player:
            exist = True
            i_iterate = i+1
            while (exist and self.valid_idx(i_iterate,j,board)):
                if board.states.get(board.location_to_move([i_iterate,j])) == self.player:
                    list_conv.append([i_iterate,j])
                else:
                    exist = False
                i_iterate += 1
            limit_up = i_iterate

        need = 5-len(list_conv)-1
        # check down
        while need > 0 and self.valid_idx(limit_down,j,board):
            need -= 1
            limit_down -= 1
        # check up
        while need > 0 and self.valid_idx(limit_up,j,board):
            need -= 1
            limit_up += 1
        if need == 0:
            if (len(list_conv) != 0):
                list_con.append(list_conv)

        # check horizontally
        # left
        list_conh = []
        if self.valid_idx(i,j-1,board) and board.states.get(board.location_to_move([i,j-1])) == self.player:
            exist = True
            j_iterate = j-1
            while (exist and self.valid_idx(i,j_iterate,board)):
                if board.states.get(board.location_to_move([i,j_iterate])) == self.player:
                    list_conh.append([i,j_iterate])
                else:
                    exist = False
                j_iterate -= 1
            limit_left = j_iterate

        # right
        if self.valid_idx(i,j+1,board) and board.states.get(board.location_to_move([i,j+1])) == self.player:
            exist = True
            j_iterate = j+1
            while (exist and self.valid_idx(i,j_iterate,board)):
                if board.states.get(board.location_to_move([i,j_iterate])) == self.player:
                    list_conh.append([i,j_iterate])
                else:
                    exist = False
                j_iterate += 1
            limit_right = j_iterate

        need = 5-len(list_conh)-1
        # check left
        while need > 0 and self.valid_idx(i,limit_left,board):
            need -= 1
            limit_left -= 1
        # check right
        while need > 0 and self.valid_idx(i,limit_right,board):
            need -= 1
            limit_right += 1
        if need == 0:
            if (len(list_conh) != 0):
                list_con.append(list_conh)

        # check diagonally 1
        # up left
        list_cond1 = []
        if self.valid_idx(i+1,j-1,board) and board.states.get(board.location_to_move([i+1,j-1])) == self.player:
            exist = True
            i_iterate = i+1
            j_iterate = j-1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == self.player:
                    list_cond1.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate += 1
                j_iterate -= 1
            limit_up = i_iterate
            limit_left = j_iterate

        # down right
        if self.valid_idx(i-1,j+1,board) and board.states.get(board.location_to_move([i-1,j+1])) == self.player:
            exist = True
            i_iterate = i-1
            j_iterate = j+1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == self.player:
                    list_cond1.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate -= 1
                j_iterate += 1
            limit_down = i_iterate
            limit_right = j_iterate

        need = 5-len(list_cond1)-1
        # up left
        while need > 0 and self.valid_idx(limit_up,limit_left,board):
            need -= 1
            limit_up += 1
            limit_left -= 1
        # down right
        while need > 0 and self.valid_idx(limit_down,limit_right,board):
            need -= 1
            limit_down -= 1
            limit_right += 1
        if need == 0:
            if (len(list_cond1) != 0):
                list_con.append(list_cond1)

        # check diagonally 2
        # down left
        list_cond2 = []
        if self.valid_idx(i+1,j+1,board) and board.states.get(board.location_to_move([i+1,j+1])) == self.player:
            exist = True
            i_iterate = i+1
            j_iterate = j+1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == self.player:
                    list_cond2.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate += 1
                j_iterate += 1
            limit_down = i_iterate
            limit_left = j_iterate

        # up right
        if self.valid_idx(i-1,j-1,board) and board.states.get(board.location_to_move([i-1,j-1])) == self.player:
            exist = True
            i_iterate = i-1
            j_iterate = j-1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == self.player:
                    list_cond2.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate -= 1
                j_iterate -= 1
            limit_up = i_iterate
            limit_right = j_iterate

        need = 5-len(list_cond2)-1
        # down left
        while need > 0 and self.valid_idx(limit_down,limit_left,board):
            need -= 1
            limit_down += 1
            limit_left += 1
        # up right
        while need > 0 and self.valid_idx(limit_up,limit_right,board):
            need -= 1
            limit_up -= 1
            limit_right -= 1
        if need == 0:
            if (len(list_cond2) != 0):
                list_con.append(list_cond2)

        return list_con

    def consecutive_opponent(self, i:int, j:int, board: Board) -> list[list[int]]:
        if (self.player == 1):
            opp = 2
        else:
            opp = 1
        list_con = []
        limit_down = -1
        limit_up = -1
        limit_right = -1
        limit_left = -1

        # check vertically
        # down
        list_conv = []
        if (self.valid_idx(i-1,j,board) and board.states.get(board.location_to_move([i-1,j])) == opp):
            exist = True
            i_iterate = i-1
            while (exist and self.valid_idx(i_iterate,j,board)):
                if board.states.get(board.location_to_move([i_iterate,j])) == opp:
                    list_conv.append([i_iterate,j])
                else:
                    exist = False
                i_iterate -= 1
            limit_down = i_iterate
        # up
        if self.valid_idx(i+1,j,board) and board.states.get(board.location_to_move([i+1,j])) == opp:
            exist = True
            i_iterate = i+1
            while (exist and self.valid_idx(i_iterate,j,board)):
                if board.states.get(board.location_to_move([i_iterate,j])) == opp:
                    list_conv.append([i_iterate,j])
                else:
                    exist = False
                i_iterate += 1
            limit_up = i_iterate
        need = 5-len(list_conv)-1
        # check down
        while need > 0 and self.valid_idx(limit_down,j,board):
            need -= 1
            limit_down -= 1
        # check up
        while need > 0 and self.valid_idx(limit_up,j,board):
            need -= 1
            limit_up += 1
        if need == 0:
            if (len(list_conv) != 0):
                list_con.append(list_conv)

        # check horizontally
        # left
        list_conh = []
        if self.valid_idx(i,j-1,board) and board.states.get(board.location_to_move([i,j-1])) == opp:
            exist = True
            j_iterate = j-1
            while (exist and self.valid_idx(i,j_iterate,board)):
                if board.states.get(board.location_to_move([i,j_iterate])) == opp:
                    list_conh.append([i,j_iterate])
                else:
                    exist = False
                j_iterate -= 1
            limit_left = j_iterate

        # right
        if self.valid_idx(i,j+1,board) and board.states.get(board.location_to_move([i,j+1])) == opp:
            exist = True
            j_iterate = j+1
            while (exist and self.valid_idx(i,j_iterate,board)):
                if board.states.get(board.location_to_move([i,j_iterate])) == opp:
                    list_conh.append([i,j_iterate])
                else:
                    exist = False
                j_iterate += 1
            limit_right = j_iterate

        need = 5-len(list_conh)-1
        # check left
        while need > 0 and self.valid_idx(i,limit_left,board):
            need -= 1
            limit_left -= 1
        # check right
        while need > 0 and self.valid_idx(i,limit_right,board):
            need -= 1
            limit_right += 1
        if need == 0:
            if (len(list_conh) != 0):
                list_con.append(list_conh)

        # check diagonally 1
        # up left
        list_cond1 = []
        if self.valid_idx(i+1,j-1,board) and board.states.get(board.location_to_move([i+1,j-1])) == opp:
            exist = True
            i_iterate = i+1
            j_iterate = j-1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == opp:
                    list_cond1.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate += 1
                j_iterate -= 1
            limit_up = i_iterate
            limit_left = j_iterate
        # down right
        if self.valid_idx(i-1,j+1,board) and board.states.get(board.location_to_move([i-1,j+1])) == opp:
            exist = True
            i_iterate = i-1
            j_iterate = j+1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == opp:
                    list_cond1.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate -= 1
                j_iterate += 1
            limit_down = i_iterate
            limit_right = j_iterate

        need = 5-len(list_cond1)-1
        # up left
        while need > 0 and self.valid_idx(limit_up,limit_left,board):
            need -= 1
            limit_up += 1
            limit_left -= 1
        # down right
        while need > 0 and self.valid_idx(limit_down,limit_right,board):
            need -= 1
            limit_down -= 1
            limit_right += 1
        if need == 0:
            if (len(list_cond1) != 0):
                list_con.append(list_cond1)

        # check diagonally 2
        # down left
        list_cond2 = []
        if self.valid_idx(i+1,j+1,board) and board.states.get(board.location_to_move([i+1,j+1])) == opp:
            exist = True
            i_iterate = i+1
            j_iterate = j+1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == opp:
                    list_cond2.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate += 1
                j_iterate += 1
            limit_down = i_iterate
            limit_left = j_iterate

        # up right
        if self.valid_idx(i-1,j-1,board) and board.states.get(board.location_to_move([i-1,j-1])) == opp:
            exist = True
            i_iterate = i-1
            j_iterate = j-1
            while (exist and self.valid_idx(i_iterate,j_iterate,board)):
                if board.states.get(board.location_to_move([i_iterate,j_iterate])) == opp:
                    list_cond2.append([i_iterate,j_iterate])
                else:
                    exist = False
                i_iterate -= 1
                j_iterate -= 1
            limit_up = i_iterate
            limit_right = j_iterate
        
        need = 5-len(list_cond2)-1
        # down left
        while need > 0 and self.valid_idx(limit_down,limit_left,board):
            need -= 1
            limit_down += 1
            limit_left += 1
        # up right
        while need > 0 and self.valid_idx(limit_up,limit_right,board):
            need -= 1
            limit_up -= 1
            limit_right -= 1
        if need == 0:
            if (len(list_cond2) != 0):
                list_con.append(list_cond2)

        return list_con

    def valid_idx(self, x:int, y:int, board:Board) -> bool:
        loc = x*board.width + y
        if loc not in range(board.width*board.height):
            return False
        else:
            return True