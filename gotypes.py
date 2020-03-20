import enum

class Player(enum.Enums):
    black = 1
    white = 2 

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

print(Player)

# from collections import namedtuple

# class Point(namedtuple("Point","row col"))