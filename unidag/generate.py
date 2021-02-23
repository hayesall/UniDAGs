# Copyright © 2021 Alexander L. Hayes

"""
Algorithms for generating random Bayesian Network structures.
"""

from random import shuffle
from random import sample
from random import random
import networkx as nx
from networkx.algorithms.dag import is_directed_acyclic_graph
from networkx.algorithms.components import is_weakly_connected


def random_tree_graph(n_nodes):
    nodes = list(range(n_nodes))
    shuffle(nodes)
    G = nx.DiGraph()
    G.add_node(nodes[0])
    used = [nodes[0]]
    for i in nodes[1:]:
        shuffle(used)
        G.add_edge(used[0], i)
        used.append(i)
    return G


def multi_dag(n_nodes, i_iterations):
    """
    Algorithm 1 in the paper.
    """

    G = random_tree_graph(n_nodes)

    for _ in range(i_iterations):

        i, j = sample(range(n_nodes), 2)

        if (i,j) in G.edges():
            temp_G = G.copy()
            temp_G.remove_edge(i, j)
            if is_weakly_connected(temp_G):
                G = temp_G
        else:
            temp_G = G.copy()
            temp_G.add_edge(i, j)
            if is_directed_acyclic_graph(temp_G):
                G = temp_G
    return G

def polytree(n_nodes, i_iterations):
    """Algorithm 2"""

    print("⚠️ Warning! ⚠️ Implementation does not match the paper.")

    G = random_tree_graph(n_nodes)

    for _ in range(i_iterations):

        i, j = sample(range(n_nodes), 2)

        if (i,j) in G.edges():
            if random() < 0.5:
                G.remove_edge(i, j)
                G.add_edge(j, i)
        # TODO(hayesall): Else branch to track common child of edge
    return G

if __name__ == "__main__":

    import argparse
    import matplotlib.pyplot as plt
    from networkx.drawing.nx_agraph import graphviz_layout

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-n", "--nodes", type=int, default=4, help="Number of nodes in the graph")
    PARSER.add_argument("-i", "--iterations", type=int, default=100, help="Run the Markov chain for `i` iterations")
    PARSER.add_argument("-a", "--algorithm", type=str, default="tree", choices=["tree", "polytree", "graph"])
    ARGS = PARSER.parse_args()

    assert ARGS.nodes > 1

    if ARGS.algorithm == "tree":
        G = random_tree_graph(ARGS.nodes)
    elif ARGS.algorithm == "polytree":
        G = polytree(ARGS.nodes, ARGS.iterations)
    elif ARGS.algorithm == "graph":
        G = multi_dag(ARGS.nodes, ARGS.iterations)

    fig1, ax = plt.subplots()

    pos = graphviz_layout(G, prog='dot')
    nx.draw_networkx_nodes(G, pos, node_size=1300, node_color='#fcba03', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=35, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowsize=35, node_size=1300, ax=ax)

    ax.set_box_aspect(1)
    plt.show()
