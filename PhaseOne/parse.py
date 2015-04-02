import gzip
import numpy
import networkx as nx
import matplotlib.pyplot as plt
import random

def getRandomNodes(graph, node_count):
	nodes = set()
	total_nodes = len(graph.nodes())
	while not len(nodes) == node_count:
		rand = random.randint(0, total_nodes - 1)
		nodes.add(graph.nodes()[rand])
	return nodes

# using the same threshold for everyone, (initial = the beginning seeded nodes)
def thresholdSim(graph, threshold, turned):
	spreading = True
	while spreading:
		spreading = False
		for node in graph.nodes():
			if node in turned:
				continue
			turned_count = 0
			successor_count = 0
			for successor in graph.successors(node):
				successor_count += 1
				if successor in turned:
					turned_count += 1
			if successor_count == 0:
				continue
			if (float(turned_count) / successor_count >= threshold):
				turned.add(node)
				spreading = True
	return turned

def graphThreshold(graph, seed_count, threshold):
	seed_set = getRandomNodes(graph, seed_count)
	result = thresholdSim(graph, threshold, seed_set)
	print "there were", len(result), "turned nodes"
	return result
	#nx.draw(graph, node_color=['y' if node in result else 'r' for node in graph], node_size=10)


def readIn():
	G = nx.read_edgelist('../twitter_combined.txt.gz', nodetype=int, create_using=nx.DiGraph())
	return G

def subGraph(graph):
	start_node = graph.nodes()[0]
	bfs_edges = list(nx.bfs_edges(graph,start_node))
	sub_graph_nodes = set()
	for i in range(len(bfs_edges)):
		parent = bfs_edges[i][0]
		child = bfs_edges[i][1]
		sub_graph_nodes.add(parent)
		sub_graph_nodes.add(child)
		# could end up being 1001, I'm assuming that's ok
		if len(sub_graph_nodes) >= 1000:
			break

	sub_graph = graph.subgraph(list(sub_graph_nodes))
	return sub_graph

def display():
	nx.draw(sub_graph, node_size=10)
	plt.show()

#graphThreshold(sub_graph, 5, .2)