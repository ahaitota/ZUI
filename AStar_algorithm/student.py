from blockworld import BlockWorld
from queue import PriorityQueue

class BlockWorldHeuristic(BlockWorld):
	def __init__(self, num_blocks=5, state=None):
		BlockWorld.__init__(self, num_blocks, state)

	def heuristic(self, goal):
		self_state = self.get_state()
		goal_state = goal.get_state()

		count = 0

		for arr in self_state:
			for item in arr:
				goal_stack = [sublist for sublist in goal_state if item in sublist][0]
				if (arr[arr.index(item):] != goal_stack[goal_stack.index(item):]):
					count += 1

		return count

	def find_path(came_from : dict, curr_node):
		# dict in the form {node : (node, action from it to here)}
		total_path = []
		while curr_node in came_from.keys():
			prev_node, action = came_from[curr_node]
			total_path.insert(0, action)
			curr_node = prev_node

		return total_path	

class AStar():
	def search(self, start, goal):
		queue = PriorityQueue()
		queue.put( (0, start) )

		came_from = dict() 
		gScore = {start : 0}

		while not queue.empty():
			_, curr_state = queue.get()
			
			if curr_state == goal:

				return BlockWorldHeuristic.find_path(came_from, curr_state)

			for action, neighbor in curr_state.get_neighbors():
				tentative_gScore = gScore[curr_state] + 1
				if (neighbor not in gScore or tentative_gScore < gScore[neighbor]):
					came_from[neighbor] = (curr_state, action)
					gScore[neighbor] = tentative_gScore
					fScore = tentative_gScore + BlockWorldHeuristic.heuristic(neighbor, goal)
					queue.put( (fScore, neighbor) )

if __name__ == '__main__':
	# Here you can test your algorithm. You can try different N values, e.g. 6, 7.
	N = 4

	start = BlockWorldHeuristic(N)
	goal = BlockWorldHeuristic(N)

	print("Searching for a path:")
	print(f"{start} -> {goal}")
	print()

	astar = AStar()
	path = astar.search(start, goal)

	if path is not None:
		print("Found a path:")
		print(path)

		print("\nHere's how it goes:")

		s = start.clone()
		print(s)

		for a in path:
			s.apply(a)
			print(s)

	else:
		print("No path exists.")

	print("Total expanded nodes:", BlockWorld.expanded)
