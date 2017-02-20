#!/usr/bin/env python2

from flask import Flask
from flask import jsonify
from simulator import Board
from team40 import Player40
import copy
import traceback

app = Flask(__name__)

@app.route("/move/<r>/<c>")
def move(r, c):
    global fl1, fl2, game_board, old_move, bot
    human_move = (int(r), int(c))
    if game_board.update(old_move, human_move, fl1) == 'UNSUCCESSFUL':
        WINNER = 'BOT'
    	MESSAGE = 'INVALID MOVE'
        return game_over((-1, -1), WINNER, MESSAGE)

    status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
    if status[1] == 'WON':							#if the game has ended after a player1 move, player 1 would win
        WINNER = 'HUMAN'
        MESSAGE = 'WON'
        return game_over((-1, -1), WINNER, MESSAGE)
    elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
        WINNER = 'NONE'
        MESSAGE = 'DRAW'
        return game_over((-1, -1), WINNER, MESSAGE)

    old_move = human_move
    game_board.print_board()

    #do the same thing for player 2
    temp_board_status = copy.deepcopy(game_board.board_status)
    temp_block_status = copy.deepcopy(game_board.block_status)

    try:
        bot_move = bot.move(game_board, old_move, fl2)
    except Exception:
        print traceback.format_exc()
        WINNER = 'HUMAN'
        MESSAGE = 'INVALID MOVE'
        return game_over((-1, -1), WINNER, MESSAGE)
    if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
        WINNER = 'HUMAN'
        MESSAGE = 'MODIFIED THE BOARD'
        return game_over(bot_move, WINNER, MESSAGE)
    if game_board.update(old_move, bot_move, fl2) == 'UNSUCCESSFUL':
        WINNER = 'HUMAN'
        MESSAGE = 'INVALID MOVE'
        return game_over(bot_move, WINNER, MESSAGE)

    status = game_board.find_terminal_state()	#find if the game has ended and if yes, find the winner
    if status[1] == 'WON':						#if the game has ended after a player move, player 2 would win
        WINNER = 'BOT'
        MESSAGE = 'WON'
        return game_over(bot_move, WINNER, MESSAGE)
    elif status[1] == 'DRAW':
        WINNER = 'NONE'
        MESSAGE = 'DRAW'
        return game_over(bot_move, WINNER, MESSAGE)

    old_move = bot_move
    game_board.print_board()
    print game_board.find_valid_move_cells(old_move)
    return jsonify({'move': sermove(old_move), 'valid': sermoves(game_board.find_valid_move_cells(old_move))})

def game_over(move, WINNER, MESSAGE):
    return jsonify({'move': sermove(move), 'winner': WINNER, 'message': MESSAGE})

def sermove(move):
    return [move[0], move[1]]

def sermoves(moves):
    x = []
    for move in moves:
        x.extend([sermove(move)])
    return x

@app.route("/init/<i_play_as>")
def init(i_play_as):
    global fl1, fl2, game_board, old_move, bot
    fl1 = 'x'
    fl2 = 'o'
    game_board = Board()
    old_move = (-1,-1)
    bot = Player40()
    if i_play_as == 'o':
        temp_board_status = copy.deepcopy(game_board.board_status)
        temp_block_status = copy.deepcopy(game_board.block_status)

        try:
            bot_move = bot.move(game_board, old_move, fl2)
        except Exception:
            print traceback.format_exc()
            WINNER = 'HUMAN'
            MESSAGE = 'INVALID MOVE'
            return game_over((-1, -1), WINNER, MESSAGE)
        if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
            WINNER = 'HUMAN'
            MESSAGE = 'MODIFIED THE BOARD'
            return game_over(bot_move, WINNER, MESSAGE)
        if game_board.update(old_move, bot_move, fl2) == 'UNSUCCESSFUL':
            WINNER = 'HUMAN'
            MESSAGE = 'INVALID MOVE'
            return game_over(bot_move, WINNER, MESSAGE)

        old_move = bot_move
        game_board.print_board()

        return jsonify({'move': sermove(old_move), 'valid': sermoves(game_board.find_valid_move_cells(old_move))})
    return "yay"

@app.route('/')
def root():
    return app.send_static_file('./index.html')

if __name__ == "__main__":
    app.run()
