"""
A file contains preprocessing function. 
"""


def recognize_trees(graphs):
    """
    Returns a list that contains boolean whether a graph is a tree or not. 

    :param graphs: a list that contains all the graphs
    :return: a list that determines whether a graph is a tree
    """

    tree_graphs = [True for _ in range(len(graphs))] 

    for index, graph in enumerate(graphs):
        # If |V| - 1 != |E| then we already know it is not a tree.
        if len(graph.vertices) - 1 != len(graph.edges):
            tree_graphs[index] = False
            continue

        # Else we do bfs on this graph to check for connectivity.
        is_tree = bfs(graph)
        tree_graphs[index] = is_tree
    
    return tree_graphs


def bfs(graph):
    """
    Start Breadth-First Search to check for connectivity of a graph.

    :param graph: the graph to be checked.
    :return: True if a graph is a tree; otherwise False.
    """
    connected = False
    vertices = len(graph.vertices)
    initial = graph.vertices[0]
    queue, labeled_vertices = [initial], [initial]
    while queue:
        v = queue.pop(0)    # take out the first vertex in queue
        nbs = v.neighbours  # get the vertex's neighbours 

        for w in nbs:
            if w not in labeled_vertices:
                queue.append(w)
                labeled_vertices.append(w)
    
    if len(labeled_vertices) == vertices:
        connected = True
    
    return connected
