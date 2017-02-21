import copy
import sys

class Player40:

	def __init__(self):
		self.MAX = 1000000000
		self.default_depth = 3
		self.player_map = {}

	def move(self, board, old_move, flag):
		if flag == 'x':
			self.player_map[True] = 'x'
			self.player_map[False] = 'o'
		else:
			self.player_map[True] = 'o'
			self.player_map[False] = 'x'

		moves = board.find_valid_move_cells(old_move)
		maxindex = 0
		maxval = -self.MAX
		# temp_board = copy.deepcopy(board)
		# temp_board.update(old_move, moves[i], self.player_map[True])
		for i in range(len(moves)):
			v = self.ab_minimax(board, moves[i], self.default_depth, -self.MAX, self.MAX, False)
			if v > maxval:
				maxval = v
				maxindex = i

		return moves[maxindex]


	def ab_minimax(self, board, old_move, depth, alpha, beta, max_player):
		if depth == 0 or board.find_terminal_state() != ('CONTINUE', '-'):
			# sys.stdout.write(str(old_move) + ' ')
			return self.heuristic(board)

		# print str(self.default_depth - depth) + '\t' + str(old_move)

		if max_player:
			v = -self.MAX
			moves = board.find_valid_move_cells(old_move)
			for new_move in moves:
				# temp_board = copy.copy(board)
				board.update(old_move, new_move, self.player_map[max_player])
				v = max(v, self.ab_minimax(board, new_move, depth - 1, alpha, beta, False))
				self.undo_move(board, new_move, max_player)
				alpha = max(alpha, v)
				if beta <= alpha:
					break
				return v

		else:
			v = self.MAX
			moves = board.find_valid_move_cells(old_move)
			for new_move in moves:
				# temp_board = copy.copy(board)
				board.update(old_move, new_move, self.player_map[max_player])
				v = min(v, self.ab_minimax(board, new_move, depth - 1, alpha, beta, True))
				self.undo_move(board, new_move, max_player)
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v

	def undo_move(self, board, old_move, max_player):
		board.board_status[old_move[0]][old_move[1]] = '-'

		# checking if a block has been won or drawn or not after the current move
		x = old_move[0]/4
		y = old_move[1]/4
		board.block_status[x][y] = '-'
		bs = board.board_status

		for i in range(4):
			# checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and bs[4*x+i][4*y] != '-':
				board.block_status[x][y] = bs[4*x+i][4*y]
				return
			# checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and bs[4*x][4*y+i] != '-':
				board.block_status[x][y] = bs[4*x][4*y+i]
				return

		# checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and bs[4*x][4*y] != '-':
			board.block_status[x][y] = bs[4*x][4*y]
			return
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and bs[4*x+3][4*y] != '-':
			board.block_status[x][y] = bs[4*x+3][4*y]
			return

		# checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return
		board.block_status[x][y] = 'd'
		return


	def heuristic(self, board):
		tstate = board.find_terminal_state()
		if tstate[1] == 'WON':
			if tstate[0] == self.player_map[True]:
				return self.MAX
			else:
				return -self.MAX

		# heur1
		return board.block_status.count(self.player_map[True]) - board.block_status.count(self.player_map[False])
