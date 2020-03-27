from dlgo import gotypes
from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo.utils import print_move,print_board
import time

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    # print(agent.base)
    bots={
        # gotypes.Player.black : agent.naive.RandomBot(),
        # gotypes.Player.white : agent.naive.RandomBot()
        gotypes.Player.black : naive.RandomBot(),
        gotypes.Player.white : naive.RandomBot()
    }
    
    while not game.is_over() :
        time.sleep(.3)

        print(chr(27)+"[2J") 
        print_board(game.board)
        bot_move=bots[game.next_player].select_move(game)
        print_move(game.next_player,bot_move)
        game = game.apply_move(bot_move)



if __name__=="__main__":
    main()