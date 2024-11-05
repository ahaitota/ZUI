import random, time
import numpy as np
import ox

class MCTSBot:
	# parameters
	c = 2 # exploration constant
	n = {} # visits
	s_a_pairs = {} # state action chosen

	V = {} # wins / n

	def __init__(self, play_as: int, time_limit: float):
		self.play_as = play_as
		self.time_limit = time_limit * 0.9

	def play_action(self, board):
		original_board = board

		start_time = time.time()
		while (time.time() - start_time) < self.time_limit:
			#root
			board = original_board
			boards_to_update = []
			boards_actions_to_update = []

			# select

			# Start from root R and select successive child nodes until a leaf node L is reached
			while not board.is_terminal():
				leaf = True
				next_states = []

				for action in board.available_actions:
					next_board = board.clone()
					next_board.apply_action(action)
					
					# calculate UCT value for each child node
	 
					if self.s_a_pairs.get((board, action), 0) == 0 or self.n.get(board, 0) == 0:
						UCT = np.inf
					else:
						N_i = self.n.get(board, 0)
						n_i = self.s_a_pairs.get((board, action), 0)
						V_i = self.V.get((board, action), 0)
						UCT = V_i + self.c * np.sqrt(np.log(N_i) / n_i)


					next_states.append((next_board, action, UCT))

					if next_board in self.n.keys():
						leaf = False


				if leaf is True and board != original_board:
					break

				next_board, action, _ = max(next_states, key=lambda x: x[2])
				
				board = next_board
				
					
			# expand

			if not board.is_terminal() and self.n.get(board, 0) != 0:
				acts = list(board.available_actions)
				act = random.choice(acts)
				new_board = board.clone()
				new_board.apply_action(act)
				board = new_board


			# simulate
   
			while not board.is_terminal():
				acts = list(board.available_actions)
				act = random.choice(acts)
				board.apply_action(act)
				boards_to_update.append((board, action))

			reward = board.get_rewards()[self.play_as]

			# backpropagate
   
			for i, (board, action) in enumerate(boards_to_update):
				if ((board, action)) in self.s_a_pairs:
					self.s_a_pairs[(board, action)] += 1
				else:
					self.s_a_pairs[(board, action)] = 1

				if board in self.n:
					self.n[board] += 1
				else:
					self.n[board] = 1

				self.V[(board, action)] = ((self.V.get((board, action), 0) + reward) / self.s_a_pairs[(board, action)]) 


		actions_from_here = []
		for action in original_board.available_actions:
			q_value = self.V.get((original_board, action), 0)
			actions_from_here.append((action, q_value))

		return max(actions_from_here, key=lambda x: x[1])[0]

if __name__ == '__main__':
    board = ox.Board(8)  # 8x8
    bots = [MCTSBot(0, 0.1), MCTSBot(1, 1.0)]
 
    # try your bot against itself
    while not board.is_terminal():
        current_player = board.current_player()
        current_player_mark = ox.MARKS_AS_CHAR[ ox.PLAYER_TO_MARK[current_player] ]
 
        current_bot = bots[current_player]
        a = current_bot.play_action(board)
        board.apply_action(a)
 
    print(f"{current_player_mark}: {a} -> \n{board}\n")
