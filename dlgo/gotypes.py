import enum

class Player(enum.Enum):
    black = 1
    white = 2 

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

player=Player(2)
print(player)
print(player.other)



from collections import namedtuple

class Point(namedtuple("Point","row col")):
    def neighbors(self):
        return [
            Points(self.row-1,self.col  ),
            Points(self.row+1,self.col  ),
            Points(self.row  ,self.col-1),
            Points(self.row  ,self.col+1)
        ]