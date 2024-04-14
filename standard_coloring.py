"""
This file contains all functions needed for standard color refinement.
"""
from preprocessing import * 


# Function that is used for the initialization of the colouring. Uniform colouring, except if there are vertices in
# the D and I list for the branching. Also compute a dictionary with a vertex as key and then a list
# of its neighbours as its value. This will be used later, so we don't have to compute it over and over again.
def initialization(graphs, D, I):
    number = len(graphs)
    coloring_vertex_keys = [{} for _ in range(number)]
    coloring_color_keys = [{0: []} for _ in range(number)]
    nb_list = [{} for _ in range(number)]
    if D and I:
        for index1, vertex1 in enumerate(D):
            coloring_vertex_keys[0][vertex1] = index1 + 1
        for index2, vertex2 in enumerate(I):
            coloring_vertex_keys[1][vertex2] = index2 + 1
    for graph in range(number):
        for v in graphs[graph].vertices:
            neighbours = v.neighbours
            nb_list[graph][v] = neighbours
            if v not in coloring_vertex_keys[graph]:
                coloring_vertex_keys[graph][v] = 0
                coloring_color_keys[graph][0].append(v)
            else:
                color = coloring_vertex_keys[graph][v]
                if color not in coloring_color_keys[graph]:
                    coloring_color_keys[graph][color] = [v]
                else:
                    coloring_color_keys[graph][color].append(v)
    return coloring_vertex_keys, coloring_color_keys, nb_list


# The function you call, when you want to check if graphs are isomorphic and count the number of automorphisms.
# Only compares two graphs at a time, which will hopefully be useful for fast color refinement.
def basic_colorref(graphs, auto):
    isomorphic_list = []
    all_graphs = list(graphs.values())
    needed = [i for i in range(len(all_graphs))]
    indexing = {i: k for i, k in zip(graphs.keys(), needed)}

    clr_vertices_init, clr_color_init, neighbours_list = initialization(all_graphs, [], [])
    for graph in graphs.keys():
        if not isomorphic_list:
            isomorphic_list.append([[graph], 0])
        else:
            for compare_graph in range(len(isomorphic_list)):
                other_graph = isomorphic_list[compare_graph][0][0]
                test_graphs = [graphs[i] for i in [other_graph, graph]]
                if len(test_graphs[0].vertices) != len(test_graphs[1].vertices):
                    clr_color = [{0: []}, {1: []}]
                else:
                    clr2_init = [clr_color_init[j].copy() for j in [indexing[other_graph], indexing[graph]]]
                    vertex2_init = [clr_vertices_init[p].copy() for p in [indexing[other_graph], indexing[graph]]]
                    neighbours2 = [neighbours_list[k] for k in [indexing[other_graph], indexing[graph]]]
                    clr_vertices, clr_color = coloring(test_graphs, clr2_init, vertex2_init, neighbours2)
                graph_coloured_1 = {k: len(v) for k, v in clr_color[0].items()}
                graph_coloured_2 = {k: len(v) for k, v in clr_color[1].items()}
                if graph_coloured_1 == graph_coloured_2:
                    if len(graph_coloured_1) == len(list(graphs[other_graph].vertices)):
                        isomorphic_list[compare_graph][0].append(graph)
                        isomorphic_list[compare_graph][1] = 1
                        break
                    else:
                        automorphisms = count_isomorphisms([], [], test_graphs, clr_color, auto)
                        if automorphisms > 0:
                            isomorphic_list[compare_graph][0].append(graph)
                            isomorphic_list[compare_graph][1] = automorphisms
                            break
                        elif compare_graph < len(isomorphic_list) - 1:
                            continue
                        else:
                            isomorphic_list.append([[graph], 0])
                elif compare_graph < len(isomorphic_list) - 1:
                    continue
                else:
                    isomorphic_list.append([[graph], 0])
    
    if auto:
        for iso in range(len(isomorphic_list)):
            check = isomorphic_list[iso][0]
            if len(check) == 1:
                index = indexing[check[0]]
                clr_vertices2, clr_color2 = coloring([graphs[index]], [clr_color_init[index]],
                                                     [clr_vertices_init[index]],
                                                     [neighbours_list[index]])
                if len(clr_color2[0]) == len(list(graphs[index].vertices)):
                    isomorphic_list[iso][1] = 1
                else:
                    test = [graphs[i] for i in [index, index]]
                    aut = count_isomorphisms([], [], test, [clr_color2[0], clr_color2[0]], auto)
                    isomorphic_list[iso][1] = aut
    return isomorphic_list


def coloring(graphs, clr_init, ver_init, neighbours_list):
    clr_color = clr_init
    clr_vertices = ver_init
    number_graphs = len(graphs)
    finished = [False for _ in range(number_graphs)]
    while False in finished:
        new_clr_color = [{} for _ in range(number_graphs)]
        new_clr_vertices = [{} for _ in range(number_graphs)]
        all_colors = []
        for k in clr_color:
            all_colors.extend(list(k.keys()))
        all_colors = list(set(all_colors))
        max_color = max(all_colors)
        for color in all_colors:
            clr_seen = {}
            for gr in range(number_graphs):
                if finished[gr] is False:
                    if color not in clr_color[gr]:
                        continue
                    v = clr_color[gr][color]
                    for vertex in v:
                        next_neighbours = sorted([clr_vertices[gr][nb] for nb in neighbours_list[gr][vertex]])
                        if clr_seen != {}:
                            if next_neighbours in clr_seen.values():
                                key = list(clr_seen.keys())[list(clr_seen.values()).index(next_neighbours)]
                                if key in new_clr_color[gr].keys():
                                    new_clr_color[gr][key].append(vertex)
                                    new_clr_vertices[gr][vertex] = key
                                else:
                                    new_clr_color[gr][key] = [vertex]
                                    new_clr_vertices[gr][vertex] = key
                            else:
                                max_color += 1
                                new_color = max_color
                                clr_seen[new_color] = next_neighbours
                                new_clr_color[gr][new_color] = [vertex]
                                new_clr_vertices[gr][vertex] = new_color
                        else:
                            clr_seen[color] = next_neighbours
                            new_clr_color[gr][color] = [vertex]
                            new_clr_vertices[gr][vertex] = color
                else:
                    new_clr_color[gr] = clr_color[gr]
                    new_clr_vertices[gr] = clr_vertices[gr]
        for g in range(number_graphs):
            if len(clr_color[g]) == len(new_clr_color[g]):
                finished[g] = True
        clr_color = new_clr_color
        clr_vertices = new_clr_vertices
    return clr_vertices, clr_color


# The recursive part of the branching, calls the coloring function again and again, but with certain vertices mapped to
# each other at the start (D and I list).
def count_isomorphisms(d_list, i_list, graphs2, old_coloring, automorphism):
    d_sequence = d_list.copy()
    num_vertices_per_color_1 = {k: len(v) for k, v in old_coloring[0].items()}
    num_vertices_per_color_2 = {k: len(v) for k, v in old_coloring[1].items()}
    if num_vertices_per_color_1 != num_vertices_per_color_2:
        return 0
    if len(num_vertices_per_color_1) == len(graphs2[0].vertices):
        return 1
    colors_graph1 = old_coloring[0]
    colors_graph2 = old_coloring[1]
    multi_colors = {k: v for (k, v) in colors_graph1.items() if len(v) > 1}
    key = list(multi_colors.keys())[0]
    x = colors_graph1[key][0]
    d_sequence.append(x)
    num = 0
    for y in colors_graph2[key]:
        i_sequence = i_list.copy()
        i_sequence.append(y)
        initial_v, initial_c, neigh = initialization(graphs2, d_sequence, i_sequence)
        clr_vertices_end, clr_color_end = coloring(graphs2, initial_c, initial_v, neigh)
        num += count_isomorphisms(d_sequence, i_sequence, graphs2, clr_color_end, automorphism)
        if num > 0 and not automorphism:
            return num
    return num
