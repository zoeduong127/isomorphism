"""
This file contains functions related to dealing with trees.
"""

from collections import Counter
import math


######################## WORKING WITH TREES ########################
def compare_trees(trees):
    """
    Compare the trees to look for automorphisms.

    :param trees: list of trees to compare
    """
    vertices1 = trees[0].vertices
    vertices2 = trees[1].vertices

    # If 2 trees have 2 different amounts of vertices then they are not isomorphic.
    if len(vertices1) != len(vertices2):
        return False, 0
    output1, output2, center = ahu_algorithm(vertices1, vertices2)

    if output1 == output2:
        auto = 1
        # In case the graph has two of the same roots we need one more multiplication by 2 (symmetry).
        if len(center) == 2:
            if center[0] == center[1]:
                auto *= 2

        check = [item[0] for item in output1]
        for label in check:
            if len(label) != 1:
                counts = list(Counter(label).values())
                for value in counts:
                    auto *= math.factorial(value)
        return True, auto
    else:
        return False, 2


def ahu_algorithm(vertices1, vertices2):
    """
    Special algorithm that works efficiently with trees to find automorphism.
    The idea is that, we loop through all leafs, then with each leaf, we check for its neighbour to see 
    if that neighbour has only 1 neighbour max (excluding leaf neighbours). 
    If that's the case, we update the corresponding adjacent labels list of that node and mark it as done. 
    In the end, when every vertex has its own label and adjacent labels list, 
    we compare the trees to see if they're isomorphic. 

    :param vertices1: list of vertices of the first tree 
    :param vertices2: list of vertices of the second tree
    """

    """
    The datastructure below is given in a list, so it can be accessed 
    via the index for each tree.
    
    
    leafs: [vertices that are leafs]
    discovered: [vertices (excluding leafs) that have 1 neighbour max + leafs]
    done: [vertices that have already satisfied the 1-neighbour-max condition]
    colors: [list of colors to keep track with]

    nodes: {vertices: [adjacent_labels], current_node_label}
    neighbours_dict: {vertex: [neighbours]}
    """
    vertices = [vertices1, vertices2]
    leafs, discovered, done, colors = [[], []], [[], []], [[], []], []
    nodes, neighbours_dict = [{}, {}], [{}, {}]

    # loop through each graph and initialize the leaf
    for index in range(0, 2):
        for v in vertices[index]:
            neighbours = v.neighbours
            neighbours_dict[index][v] = neighbours

            # If it only has 1 neighbour (which means, it is a leaf) then give it the list as [[neighbours], label].
            if len(neighbours) == 1:
                nodes[index][v] = [[-1], 0]
                discovered[index].append(v)
                leafs[index].append(v)
            else:
                nodes[index][v] = [[], -1]

    iteration = 0
    new_color = 0
    while len(discovered[0]) != len(vertices[0]) or len(discovered[1]) != len(vertices[1]):
        new_leafs = [[], []]

        for index in range(0, 2):
            for leaf in leafs[index]:  # loop through all the leaf vertices
                leaf_labels = [nodes[index][leaf][1]]  # get the labels of the leaf into a list
                leaf_neighbours = neighbours_dict[index][
                    leaf]  # get the vertices that are neighbours with the leaf nodes

                for current_neighbour in leaf_neighbours:
                    # If the vertex is already done.
                    if current_neighbour in done[index] or current_neighbour in leafs[index]:
                        continue

                    neighbours_of_current_node = neighbours_dict[index][current_neighbour]
                    inter = set(leafs[index]).intersection(neighbours_dict[index][current_neighbour])

                    # neighbours of current node can only have max 1 neighbour (excluding leafs)
                    if len(neighbours_of_current_node) - len(inter) <= 1:
                        if current_neighbour not in new_leafs[index]:
                            new_leafs[index].append(current_neighbour)
                            discovered[index].append(current_neighbour)

                        # Get the adjacent labels of the current node.
                        current_neighbour_adjacent_labels = nodes[index][current_neighbour][0]
                        # Get the combined labels for the inner node.
                        updated_adjacent_labels = sorted(current_neighbour_adjacent_labels + leaf_labels)
                        # Update the adjacent list of inner nodes.
                        nodes[index][current_neighbour][0] = updated_adjacent_labels

                        if (updated_adjacent_labels, iteration) in colors:
                            nodes[index][current_neighbour][1] = colors.index((updated_adjacent_labels, iteration)) + 1
                        else:
                            new_color += 1
                            nodes[index][current_neighbour][1] = new_color  # create a new label for the inner node
                            colors.append((updated_adjacent_labels, iteration))

                        done[index].append(leaf)
                        continue

                    else:
                        new_leafs[index].append(leaf)

        leafs[0] = new_leafs[0]
        leafs[1] = new_leafs[1]
        iteration += 1

    labels1 = sorted(list(nodes[0].values()))
    labels2 = sorted(list(nodes[1].values()))
    roots1 = [nodes[0][root1] for root1 in leafs[0]]

    return labels1, labels2, roots1


def isomorphism_algorithm(trees, decision):
    results_trees = []

    for index, graph in trees.items():
        if not results_trees:
            results_trees.append([[index], 0])
        else:
            for i in range(len(results_trees)):
                check_graphs = [trees[i] for i in [results_trees[i][0][0], index]]
                isomorphic, automorphisms = compare_trees(check_graphs)
                if isomorphic:
                    results_trees[i][0].append(index)
                    results_trees[i][1] = automorphisms
                    break
                elif i < len(results_trees) - 1:
                    continue
                else:
                    results_trees.append([[index], 0])

    # count automorphism for a single tree (we already computed the amount of automorphisms for pairs or more)
    if decision:
        for result in results_trees:
            if result[1] == 0:
                check_graphs = [trees[i] for i in [result[0][0], result[0][0]]]
                _, automorphisms = compare_trees(check_graphs)
                result[1] = automorphisms

    return results_trees
