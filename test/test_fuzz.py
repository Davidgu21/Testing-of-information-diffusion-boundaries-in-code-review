import random
random.seed(54677)
nr_of_nodes = random.randrange(0, 10)
node_names = []
random_graph = {}
#create dict for graph
for i in range(0, nr_of_nodes):
    node_names.append("node_" + str(i))

for n in node_names:
    nr_of_connections = random.randrange(0,nr_of_nodes)
    node_connections = []
    for i in range(0,nr_of_connections):        # Can connect to same node more than once
        # node_connections.append(random.randrange(nr_of_nodes))
        node_connections.append(node_names[random.randrange(nr_of_nodes)])
    random_graph[n] = node_connections

print(f"Dict with node and connections: \n{random_graph}")
random_src = random.choice(node_names)
print(f"source node: {random_src}")