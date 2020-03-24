import copy
from dlgo.gotypes import Player,Point

class Move():
    # 定義下棋的動作
    def __init__(self,point=None,is_pass=False,is_resign=False):
        assert(point is not None)^is_pass^is_resign
        self.point=point
        self.is_play=(point is not None)
        self.is_pass=is_pass
        self.is_resign=is_resign
    # 落子
    @classmethod
    def play(cls,point):
        return Move(point=point)
    # 跳過
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    # 投降
    @classmethod
    def resign(cls):
        return Move(is_resign=True)

# a=Move.play(Point(2,2))
# print(a.point)

class GoString():
    # 定義一個棋子串，及其周圍的氣
    def __init__(self,color,stones,liberties):
        self.color=color
        self.stones=set(stones)
        self.liberties=set(liberties)
    # 移除氣
    def remove_liberty(self,point):
        self.liberties.remove(point)
    # 加入氣    
    def add_liberty(self,point):
        self.liberties.add(point)
    # 合併兩棋子串
    def merged_with(self,go_string):
        assert go_string.color==self.color
        combined_stones=self.stones|go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties|go_string.liberties)-combined_stones
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self,other):
        return isinstance(other,GoString) and \
            self.color==other.color and \
            self.stones==other.stones and \
            self.liberties==other.liberties

# a = GoString(Player(2),Point(1,1),Point(1,1).neighbors())
# print(a.color,a.liberties,a.num_liberties)

class Board():
    def __init__(self,num_rows,num_cols):
        self.num_rows=num_rows
        self.num_cols=num_cols
        self._grid={}

    def place_stone(self,player,point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = [] 
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string=self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player :
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color :
                    adjacent_opposite_color.append(neighbor_string)

        new_string = GoString(player,[point],liberties)

        for same_color_string in adjacent_same_color:
            new_string=new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0 :
                self._remove_string(other_color_string)


    def is_on_grid(self,point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols 
    
    def get(self,point):
        string = self._grid.get(point)
        if string is None : 
            return None 
        return string.color

    def get_go_string(self,point):
        string = self._grid.get(point)
        if string is None : 
            return None 
        return string

    # 提掉整個棋子串
    def _remove_string(self,string):
        for point in string.stones :
            for neighbor in point.neighbors() :
            # 刷新周圍棋子串的狀態
                neighbor_string = self._grid.get(neighbor)
                # 周圍的這點是空的，在之前已經被提掉
                if neighbor_string is None :
                    continue
                # 周圍的這點是對方的，位對方的棋子串增加一氣
                if neighbor_string is not string :
                    neighbor_string.add_liberty(point)
            # 提掉一個子
            self._grid[point]=None

# a = Board(5,5)
# a.place_stone(Player.black,Point(1,1))
# print(a._grid)

class GameState():
    def __init__(self,board,next_player,previous,move):
        self.board=board
        self.next_player=next_player
        self.previous_state=previous
        self.last_move=move

    def apply_move(self,move):
        if move.is_play :
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player,move.point)
        else : 
            next_board = self.board
        return GameState(next_board,self.next_player.other,self,move)

    @classmethod
    def new_game(cls,board_size):
        if isinstance(board_size,int):
            board_size=(board_size,board_size)
        board=Board(*board_size)
        print(board_size,*board_size)
        return GameState(board,Player.black,None,None)
    
    def is_over(self):
        # 剛建立新局
        if self.last_move is None :
            print('just build')
            return False
        if self.last_move.is_resign :
            return True 
        second_last_move = self.previous_state.last_move
        if second_last_move is None :
            print('first step')
            return False
        return self.last_move.is_pass and second_last_move.is_pass 
    
    def is_move_self_capture(self,player,move):
        if not move.is_play:
            return False 
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player,move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0 
    
    @property 
    def situation(self):
        return (self.next_player,self.board)

    def does_move_violate_ko(self,player,move):
        if not move.is_play:
            return False 
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player,move.point)
        next_situation = (player.other,next_board)
        past_state = self.previous_state
        while past_state is not None :
            if past_state.situation == next_situation :
                return True 
            past_state = past_state.previous_state
        return False 


a=GameState.new_game(19)
print(a,a.next_player,a.is_over())
# a=a.apply_move(Move.play(Point(2,2)))
a=a.apply_move(Move.resign())
print(a,a.next_player,a.is_over())
a=a.apply_move(Move.resign())
print(a,a.next_player,a.is_over())