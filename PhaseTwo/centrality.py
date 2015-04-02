import gzip
import numpy
import networkx as nx
import scipy
import matplotlib.pyplot as plt
import random
import operator

def readIn():
	graph = nx.read_edgelist('../twitter_combined.txt.gz', nodetype=int, create_using=nx.DiGraph())
	graph.remove_edges_from(graph.selfloop_edges())
	return graph

def generateThresholds(graph):
	thresholds = {}
	for node in graph.nodes():
		thresholds[node] = random.gauss(.55, .68)
	#nx.set_node_attributes(graph, 'threshold', thresholds)
	return thresholds

def sortAndSplice(centralities, count):
	sorted_centralities = sorted(centralities.items(), key=operator.itemgetter(1), reverse=True)
	sorted_nodes = [int(tup[0]) for tup in sorted_centralities[0:count]]
	return sorted_nodes

def degree(graph, count):
	centralities = nx.degree_centrality(graph)
	return sortAndSplice(centralities, count)

def eigenvector(graph, count):
	centralities = nx.eigenvector_centrality_numpy(graph)
	return sortAndSplice(centralities, count)

def k_core(graph, count):
	centralities = nx.core_number(graph)
	return sortAndSplice(centralities, count)

def simulation(graph, thresholds, turned):
	turned = set(turned)
	seed_size = len(turned)
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
			if (float(turned_count) / successor_count >= thresholds[node]):
				turned.add(node)
				spreading = True
	print "With a seed size of", seed_size, ":", (len(turned) - seed_size), "were turned"
	#return turned

# def cascading(graph, count):






