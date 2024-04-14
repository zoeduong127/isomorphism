"""
This file contains the helper functions. 
"""

from graph_io import *
import timeit 


def print_result(decision, results):
    """
    Print the result following a particular format. 

    :param decision: True if #Aut problem is included; otherwise False.
    :param results: A list contains pairs of isomorphic graphs (and count automorphism (if decision = True))
    """
    if decision:
        print("Sets of isomorphic graphs:    Number of automorphisms:")
        for res in results:
            print(f"{res[0]}{' ' * (30 - len(str(res[0])))}{res[1]}")
    else:
        print("Sets of isomorphic graphs:")
        for res in results:
            print(f"{res[0]}")


def read_file(filename):
    """
    Given the file name, read the file and return graphs in the file.

    :param filename: name of the file
    """
    start = timeit.default_timer()
    with open(filename) as g:
        graphs = load_graph(g, read_list=True)[0]
    end = timeit.default_timer()
    print(f'Time for loading the graph: {end - start}')

    return graphs 


def get_highest_degree_color(multi_colors, choice):
    """
    Return the color class that has highest-degree vertices.

    :param multi_colors: {color: [list of corresponding vertices]}, where length of corresponding vertices > 2. 
    :param choice: set to True for the color with the highest degree; otherwise False for the smallest degree.
    """

    # Sort based on the degree of the vertices,
    sorted_multi_colors = dict(sorted(multi_colors.items(), key=lambda item: item[1][0].degree, reverse=True))
    if choice:
        return list(sorted_multi_colors.keys())[0]
    else:
        return list(sorted_multi_colors.keys())[-1]


def get_most_vertices_color(multi_colors, choice):
    """
    Return the color class that has the most vertices. 

    :param multi_colors: {color: [list of corresponding vertices]}, where length of corresponding vertices > 2. 
    :param choice: set to True if we want to get the color with the most vertices; otherwise False for the least. 
    """

    # sort based on the degree of the vertices
    sorted_multi_colors = dict(sorted(multi_colors.items(), key=lambda item: (len(item[1])), reverse=True))
    if choice:
        return list(sorted_multi_colors.keys())[0]
    else:
        return list(sorted_multi_colors.keys())[-1]
