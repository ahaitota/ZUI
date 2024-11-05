from blockworld import BlockWorldEnv
import random

class QLearning():
	q_table = dict()
	
	# don't modify the methods' signatures!
	def __init__(self, env: BlockWorldEnv):
		self.env = env

	def train(self):
		eps = 0.1
		alpha = 0.1
		gamma = 0.95

		train = True 
		s = self.env.reset()

		while train:		
			if eps > random.uniform(0, 1):
				a = random.choice(s[0].get_actions())
			else:
				this_state = []
				for action in s[0].get_actions():
					q_value = self.q_table.get((s[0], action, s[1]), 0)
					this_state.append((action, q_value))
				a = max(this_state, key=lambda x: x[1])[0]

			s_, r, done = self.env.step(a)

			if done:
				max_a_ = 0
			else:
				next_state = []
				for action in s_[0].get_actions():
					q_value = self.q_table.get((s_[0], action, s_[1]), 0)
					next_state.append((action, q_value))
				a_ = max(next_state, key=lambda x: x[1])[0]

				max_a_ = self.q_table.get((s_[0], a_, s_[1]), 0)

			curr_q_value = self.q_table.get((s[0], a, s[1]), 0)
			
			self.q_table[(s[0], a, s[1])] = curr_q_value + alpha * (r + gamma * max_a_ - curr_q_value)

			if done:
				s = self.env.reset()
				continue

			s = s_


	def act(self, s):
		this_state = []
		for action in s[0].get_actions():
			q_value = self.q_table.get((s[0], action, s[1]), 0)
			this_state.append((action, q_value))
		
		a = max(this_state, key=lambda x: x[1])[0]
		return a

if __name__ == '__main__':
	# Here you can test your algorithm. Stick with N <= 4
	N = 4

	env = BlockWorldEnv(N)
	qlearning = QLearning(env)

	# Train
	qlearning.train()

	# Evaluate
	test_env = BlockWorldEnv(N)

	test_problems = 10
	solved = 0
	avg_steps = []

	for test_id in range(test_problems):
		s = test_env.reset()
		done = False

		print(f"\nProblem {test_id}:")
		print(f"{s[0]} -> {s[1]}")

		for step in range(50): 	# max 50 steps per problem
			a = qlearning.act(s)
			s_, r, done = test_env.step(a)

			print(f"{a}: {s[0]}")

			s = s_

			if done:
				solved += 1
				avg_steps.append(step + 1)
				break

	avg_steps = sum(avg_steps) / len(avg_steps)
	print(f"Solved {solved}/{test_problems} problems, with average number of steps {avg_steps}.")
