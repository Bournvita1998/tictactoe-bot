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
		for i in range(len(moves)):
			temp_board = copy.deepcopy(board)
			temp_board.update(old_move, moves[i], self.player_map[True])
			v = self.ab_minimax(temp_board, moves[i], self.default_depth, -self.MAX, self.MAX, False)
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
			v = -1000000000
			moves = board.find_valid_move_cells(old_move)
			for new_move in moves:
				temp_board = copy.copy(board)
				temp_board.update(old_move, new_move, self.player_map[max_player])
				v = max(v, self.ab_minimax(temp_board, new_move, depth - 1, alpha, beta, False))
				alpha = max(alpha, v)
				if beta <= alpha:
					break
				return v

		else:
			v = 1000000000
			moves = board.find_valid_move_cells(old_move)
			for new_move in moves:
				temp_board = copy.copy(board)
				temp_board.update(old_move, new_move, self.player_map[max_player])
				v = min(v, self.ab_minimax(temp_board, new_move, depth - 1, alpha, beta, True))
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v

	def heuristic(self, board):
		# heur1
		return board.block_status.count(self.player_map[True]) - board.block_status.count(self.player_map[False])
