"""
This file contains fast color refinement functions. 
"""

from utils import * 


# Function that is used for the initialization of the colouring. Uniform colouring, except if there are vertices in
# the D and I list for the branching. Also compute a dictionary with a vertex as key and then a list
# of its neighbours as its value. This will be used later, so we don't have to compute it over and over again.
def fast_initialization(graphs, dl, il):
    number = len(graphs)
    coloring_vertex_keys = [{} for _ in range(number)]
    coloring_color_keys = [{0: set()} for _ in range(number)]
    nb_dict = [{} for _ in range(number)]
    if dl and il:
        for index1, vertex1 in enumerate(dl):
            coloring_vertex_keys[0][vertex1] = index1 + 1
        for index2, vertex2 in enumerate(il):
            coloring_vertex_keys[1][vertex2] = index2 + 1
    for graph in range(number):
        for v in graphs[graph].vertices:
            nb = v.neighbours
            nb_dict[graph][v] = nb
            if v not in coloring_vertex_keys[graph]:
                coloring_vertex_keys[graph][v] = 0
                coloring_color_keys[graph][0].add(v)
            else:
                color = coloring_vertex_keys[graph][v]
                if color not in coloring_color_keys[graph]:
                    coloring_color_keys[graph][color] = {v}
                else:
                    coloring_color_keys[graph][color].add(v)
    return coloring_vertex_keys, coloring_color_keys, nb_dict


# The function you call, when you want to check if graphs are isomorphic and count the number of automorphisms.
# Only compares at most two graphs at a time, but input can of course be more graphs.
def fast_colorref(graphs, auto):
    isomorphisms = []
    all_graphs = list(graphs.values())
    needed = [i for i in range(len(all_graphs))]
    indexing = {i: k for i, k in zip(graphs.keys(), needed)}
    # Create the initial coloring (uniform).
    clr_vertex_init, clr_color_init, neighbours = fast_initialization(all_graphs, [], [])
    # Compare graphs to see if they are isomorphic. Only need to compare it with one graph in each class.
    for graph in graphs.keys():
        if not isomorphisms:
            isomorphisms.append([[graph], 0])
        else:
            for compare_graph in range(len(isomorphisms)):
                other_graph = isomorphisms[compare_graph][0][0]
                test_graphs = [graphs[i] for i in [other_graph, graph]]
                if len(test_graphs[0].vertices) != len(test_graphs[1].vertices):
                    clr_color = [{0: []}, {1: []}]
                else:
                    clr2_init = [clr_color_init[j].copy() for j in [indexing[other_graph], indexing[graph]]]
                    clr2_vertex = [clr_vertex_init[j].copy() for j in [indexing[other_graph], indexing[graph]]]
                    neighbours2 = [neighbours[k] for k in [indexing[other_graph], indexing[graph]]]
                    clr_color = fast_coloring(test_graphs, clr2_init, clr2_vertex, neighbours2)
                graph_colored_1 = {k: len(v) for k, v in clr_color[0].items()}
                graph_colored_2 = {k: len(v) for k, v in clr_color[1].items()}
                if graph_colored_1 == graph_colored_2:
                    if len(graph_colored_1) == len(list(graphs[other_graph].vertices)):
                        isomorphisms[compare_graph][0].append(graph)
                        isomorphisms[compare_graph][1] = 1
                        break
                    else:
                        automorphisms = branching([], [], test_graphs, clr_color, auto)
                        if automorphisms > 0:
                            isomorphisms[compare_graph][0].append(graph)
                            isomorphisms[compare_graph][1] = automorphisms
                            break
                        elif compare_graph < len(isomorphisms) - 1:
                            continue
                        else:
                            isomorphisms.append([[graph], 0])
                elif compare_graph < len(isomorphisms) - 1:
                    continue
                else:
                    isomorphisms.append([[graph], 0])
    # If a graph is not isomorphic to any other graph in the file, we did not compute the amount of automorphisms yet,
    # therefore we should still do this if the auto variable is set to True.
    if auto:
        for iso in range(len(isomorphisms)):
            check = isomorphisms[iso][0]
            if len(check) == 1:
                index = indexing[check[0]]
                clr_color2 = fast_coloring([all_graphs[index]], [clr_color_init[index].copy()],
                                           [clr_vertex_init[index].copy()], [neighbours[index]])
                if len(clr_color2[0]) == len(list(all_graphs[index].vertices)):
                    isomorphisms[iso][1] = 1
                else:
                    aut = branching([], [], [all_graphs[index], all_graphs[index]],
                                    [clr_color2[0], clr_color2[0]], auto)
                    isomorphisms[iso][1] = aut
    return isomorphisms


# The actual fast color refinement. Input should always be for either two graphs or one graph. The input is one
# or two graphs with an initial partition (two dictionaries, one of the form {color: [vertices]} and one of the
# form {vertex: color}. We also give a dictionary with a vertex as key and the neighbours of that vertex as value,
# because we use this a lot and in this way we don't have to compute the neighbours over and over again.
def fast_coloring(graphs, clr_init, ver_init, neighbours_list):
    number_graphs = len(graphs)
    partition = clr_init
    # Look at what the current colors are and put them in the queue. Later on we only add new colors to the queue for
    # the first graph, because if they are isomorphic, the second graph would add the exact same colors,
    # and we only have to add them once.
    color_i_init = list(clr_init[0].keys())
    queue = color_i_init
    # Look at the current max color, so we know what new color to make if we split a color class.
    max_color = max(color_i_init)
    max_list = [max_color for _ in range(number_graphs)]
    check = [set(), set()]
    # While the queue is not empty, we run the coloring. Once it is empty we return the coarsest stable partition.
    while queue:
        # If we have two graphs, we need a way to check during the process if they still have the same partition.
        # If not, we return some coloring, which indicates that they are not isomorphic. We do this using a check set.
        # The check set should be the same for two graphs in each iteration if they want to be isomorphic.
        if number_graphs == 2:
            if check[0] != check[1]:
                return [{0: []}, {1: []}]
        # Take the first color out of the queue.
        clr = queue.pop(0)
        check = [set(), set()]
        # Now for either one graph or two graphs we will refine the current partition.
        for gr in range(number_graphs):
            count, reverse_count, seen, refine = {}, {}, set(), set()
            # We start off by looking at each vertex in the color class we just took out of the queue and
            # for each of its neighbours we do +1. So, we want to check how many neighbours each vertex has in
            # this color class we just took out of the queue, but in such a way that we don't have to check each vertex.
            for v in partition[gr][clr]:
                for u in neighbours_list[gr][v]:
                    if u not in seen:
                        clr_class = ver_init[gr][u]
                        check[gr].add(clr_class)
                        # If a color class in of length one, we can't split it up anymore, so we don't add it.
                        if len(partition[gr][clr_class]) > 1:
                            refine.add(clr_class)
                            count[u] = 1
                            seen.add(u)
                    else:
                        count[u] += 1
            # Once we have a dict with a vertex as key and the amount of neighbours in the color class as value,
            # we 'reverse' this. We make the values the key and have a set of all vertices with this 'color degree'
            # as the value. Then we sort the keys and the color classes we want to refine, because we want to be
            # consistent for both graphs (if the input is two graphs).
            for key, value in count.items():
                if value not in reverse_count:
                    reverse_count[value] = {key}
                else:
                    reverse_count[value].add(key)
            c_degrees = sorted(reverse_count.items())
            refine_ordered = sorted(list(refine))
            # Now we will refine the old color classes we need to refine and look carefully at which color classes
            # we should add to the queue (which we only add to the queue for the first graph as mentioned before).
            for c_i in refine_ordered:
                add_queue = []
                rest = partition[gr].pop(c_i)
                # Take the color class out of the partition and take the intersection with an item in 'refine ordered'.
                # We might still not split the class, in this case we add it back to the partition.
                # If we do split a class we have to make a new color for one of the parts and use the old color
                # for the other one.
                for c_deg, split in c_degrees:
                    if not rest:
                        break
                    # Take intersection.
                    new = rest & split
                    # If we do not split, we add it back and continue.
                    if new == rest and not add_queue:
                        partition[gr][c_i] = new
                        rest = rest - split
                        continue
                    # If the intersection is empty we also continue.
                    if not new:
                        continue
                    # Take the difference, to get the remaining elements of the color class we just split up.
                    rest = rest - split
                    # If there is still a rest we use a new color and add it to the partitioning and add the length
                    # of the new class + the color to the add_queue list. Which are possible colors we might
                    # add later to the queue.
                    if rest:
                        max_list[gr] += 1
                        new_color = max_list[gr]
                        partition[gr][new_color] = new
                        for j in new:
                            ver_init[gr][j] = new_color
                        add_queue.append([len(new), new_color])
                    # If there is no rest, we can just use the old color for this part of the split up class.
                    # If this color is currently not in the queue we also add it to add_queue.
                    else:
                        partition[gr][c_i] = new
                        if c_i not in queue:
                            add_queue.append([len(new), c_i])
                # There are cases where there still is a rest remaining, so we add this to the partition again.
                if rest:
                    partition[gr][c_i] = rest
                    if c_i not in queue:
                        add_queue.append([len(rest), c_i])
                # Now we check which colors we should add to the queue. If there is only one element in add_queue,
                # we do not have a choice, and we add this color to the queue. Else we append all colors in
                # the queue except the one with the largest est of vertices.
                if add_queue and gr == 0:
                    if len(add_queue) > 1:
                        d = sorted(add_queue)
                        for q in d[:-1]:
                            queue.append(q[1])
                    else:
                        queue.append(add_queue[0][1])
    return partition


# The recursive part of the coloring, the branching. Calls the fast coloring function again and again,
# but with certain vertices mapped to each other at the start (D and I list). We keep checking if they are isomorphic
# to each other and if there coloring is discrete.
def branching(d_list, i_list, graphs2, old_coloring, automorphism):
    num_vertices_per_color_1 = {k: len(v) for k, v in old_coloring[0].items()}
    num_vertices_per_color_2 = {k: len(v) for k, v in old_coloring[1].items()}
    if num_vertices_per_color_1 != num_vertices_per_color_2:
        return 0
    if len(num_vertices_per_color_1) == len(graphs2[0].vertices):
        return 1
    d_sequence = d_list.copy()
    colors_graph1 = old_coloring[0].copy()
    colors_graph2 = old_coloring[1].copy()
    
    multi_colors = {k: v for (k, v) in colors_graph1.items() if len(v) > 1}
    # Branching rule.
    key = get_most_vertices_color(multi_colors, True)
    x = sorted(list(colors_graph1[key]), key=lambda vertex: vertex.label)[0]
    d_sequence.append(x)

    num = 0
    for y in colors_graph2[key]:
        i_sequence = i_list.copy()
        i_sequence.append(y)
        initial_v, initial_c, neigh = fast_initialization(graphs2, d_sequence, i_sequence)
        clr_color_end = fast_coloring(graphs2, initial_c, initial_v, neigh)
        num += branching(d_sequence, i_sequence, graphs2, clr_color_end, automorphism)
        if num > 0 and not automorphism:
            return num
    return num
