import networkx as nx
import os
import matplotlib.pyplot as plt
import sys
import numpy as np
# Counts number of edges between two buses
def num_bus_edges(g, num_buses, first_bus, second_bus):
		# Counter variable for friendships
		total_edges = 0
		# For each spot in the first bus
		for i in range(num_buses):
			# For each spot in the second bus
			for j in range(num_buses):
				# Convert student index to node number
				student_one = i + (first_bus * num_buses)
				# Convert student index to node number
				student_two = j + (second_bus * num_buses)
				# If the second student is adjacent to the first (i.e. they are friends)
				if(student_two in g.adj[student_one]):
					# Add an edge
					total_edges += 1
		# Return total edges between two buses
		return total_edges
# Creates adversarial input graph
# Uses largest square number of students possible
# K buses each with k students forming a complete friendship graph
# Then adds dummy friendships and rowdy groups
def generate_input(max_students):
	# One-line calculation of largest square less than
	num_buses = int((max_students ** 0.5) // 1)
	# Total number of students
	num_students = num_buses ** 2
	# Create graph
	g = nx.Graph()
	# For all students
	for student in range(num_students):
		# Add all nodes
		g.add_node(student)

	# Add "real" friendships
	# For all buses
	for bus in range(num_buses):
		# For each first student
		for first_spot in range(num_buses):
			# For each second student
			for second_spot in range(first_spot + 1, num_buses):
				# Adjust student number by bus
				first_student = first_spot + (bus * num_buses)
				# Adjust student number by bus
				second_student = second_spot + (bus * num_buses)
				# Add each friendship
				g.add_edge(first_student, second_student)
	print(len(g.edges))
	#print(g.nodes)
	# Add "dummy" friendships
	# For each student
	for student in g.nodes:
		# All students with no connections
		potential_matches = [node for node in g.nodes if ((node not in g.adj[student]) and node != student)]
		# Add as many friendships as possible
		while (g.degree(student) < (2 * num_buses - 3)):
			# If no new friendships possible
			if(len(potential_matches) == 0):
				# Skip student
				break
			# Else, pick a random student
			match = np.random.choice(potential_matches)
			# If the other student has an available friendship (won't go over max)
			if (g.degree(match) < (2 * num_buses - 3)):
				# Calculate first student's bus number
				student_bus = student // num_buses
				# Calculate second student's bus number
				match_bus = match // num_buses
				# If there are available connections between the two buses
				if(num_bus_edges(g, num_buses, student_bus, match_bus) < num_buses - 2):
					# Add the dummy friendship
					g.add_edge(student, match)
			# Remove the student from matches (regardless of if you added one)
			potential_matches.remove(match)
	# Write file to directory
	print(num_bus_edges(g, 4, 0, 1))
	display_graph(g, 1, 500)
	#nx.write_gml(g, "/Users/sebastienwhetsel/Documents/inputs/large/graph.gml", nx.readwrite.gml.literal_stringizer)

### Idk kristen did this ¯\_(ツ)_/¯
def display_graph(graph, k, iterations):
	# play around with k and iterations - more iterations = more centered around component, k = optimal node dist
	pos=nx.spring_layout(graph, k = k, iterations = iterations)
	nx.draw(graph, pos, node_size = 25, font_size = 8, with_labels=True)
	plt.show()

if __name__ == '__main__':
	size = int(sys.argv[1])
	if size != None:
		generate_input(size)
