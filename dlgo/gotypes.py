import enum
# 定義玩家執黑或白子
class Player(enum.Enum):
    black = 1
    white = 2 
    # 回傳玩家對手的顏色
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

# a = Player.black
# print(a,a.other)

from collections import namedtuple

class Point(namedtuple("Point","row col")):
    def neighbors(self):
        return [
            Point(self.row-1,self.col  ),
            Point(self.row+1,self.col  ),
            Point(self.row  ,self.col-1),
            Point(self.row  ,self.col+1)
        ]

# a=Point(1,1)
# print(a,a.neighbors())