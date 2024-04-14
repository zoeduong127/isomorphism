"""
This file contains all the function that are used for complete and edgeless graphs.
"""

import math


def isCompleteGraph(graph):
    """
    Check if the given graph is complete (i.e., |E| = (n*(n-1)) / 2, where n = |V|)

    :param graph: the given graph.
    """
    n_vertices = len(graph.vertices)  # We cant use ._e or ._v these are protected members of the graph class
    n_edges = len(graph.edges)  # We should instead use .vertices or .edges

    if n_edges == (n_vertices * (n_vertices - 1) / 2):
        return True

    return False


def isEdgelessGraph(graph):
    """
    Check if the given graph has no edges.
    Because if it's the case, then we can simply count automorphism = |V|!.

    :param graph: the given graph
    """

    return len(graph.edges) == 0


# Function which we use to compare complete/edgeless graphs and compute number of automorphisms.
def easy_isomorphism(easy_graphs):
    easy_results = []

    for index, graph in easy_graphs.items():
        if not easy_results:
            easy_results.append([[index], math.factorial(len(graph.vertices))])
        else:
            for i in range(len(easy_results)):
                compare_graphs = [easy_graphs[j] for j in [easy_results[i][0][0], index]]
                if (len(compare_graphs[0].vertices) == len(compare_graphs[1].vertices)
                        and len(compare_graphs[0].edges) == len(compare_graphs[1].edges)):
                    easy_results[i][0].append(index)
                    break
                elif i < len(easy_results) - 1:
                    continue
                else:
                    easy_results.append([[index], math.factorial(len(graph.vertices))])

    return easy_results
