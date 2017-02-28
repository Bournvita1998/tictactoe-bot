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
				board.board_status[new_move[0]][new_move[1]] = '-'
				board.block_status[new_move[0]/4][new_move[1]/4] = '-'
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
				board.board_status[new_move[0]][new_move[1]] = '-'
				board.block_status[new_move[0]/4][new_move[1]/4] = '-'
				beta = min(beta, v)
				if beta <= alpha:
					break
			return v


	def heuristic(self, board):
		tstate = board.find_terminal_state()
		if tstate[1] == 'WON':
			if tstate[0] == self.player_map[True]:
				return self.MAX
			else:
				return -self.MAX

		# heur1
		heur1 = 0
		for i in range(4):
			for j in range(4):
				if board.block_status[i][j] == self.player_map[True]:
					heur1 += 1
				elif board.block_status[i][j] == self.player_map[False]:
					heur1 -= 1

		return heur1
