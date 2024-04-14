import math
from twins_recognition import *


def twins_initialization(graphs, dl, il, fal_twins, twins):
    number = len(graphs)
    coloring_vertex_keys = [{} for _ in range(number)]
    coloring_color_keys = [{0: set()} for _ in range(number)]
    nb_dict = [{} for _ in range(number)]
    if dl and il:
        for index1, vertex1 in enumerate(dl):
            coloring_vertex_keys[0][vertex1] = index1 + 1
        for index2, vertex2 in enumerate(il):
            coloring_vertex_keys[1][vertex2] = index2 + 1
    check_false, check_true, save_clrs_false, save_clrs_true = [], [], [], []
    for graph in range(number):
        max_clr = len(dl)
        for a in fal_twins[graph]:
            deg_length = [list(a)[0].degree, len(a)]
            if deg_length not in check_false:
                check_false.append(deg_length)
                save_clrs = []
                for ver in a:
                    max_clr += 1
                    save_clrs.append(max_clr)
                    if ver not in dl and graph == 0 or ver not in il and graph == 1 or graph > 1:
                        coloring_vertex_keys[graph][ver] = max_clr
                save_clrs_false.append(save_clrs)
            else:
                clrs_needed = save_clrs_false[check_false.index(deg_length)]
                for ver3, clr in zip(a, clrs_needed):
                    if ver3 not in dl and graph == 0 or ver3 not in il and graph == 1 or graph > 1:
                        coloring_vertex_keys[graph][ver3] = clr
        for b in twins[graph]:
            deg_length2 = [list(b)[0].degree, len(b)]
            if deg_length2 not in check_true:
                check_true.append(deg_length2)
                save_clrs2 = []
                for ver2 in b:
                    max_clr += 1
                    save_clrs2.append(max_clr)
                    if ver2 not in dl and graph == 0 or ver2 not in il and graph == 1 or graph > 1:
                        coloring_vertex_keys[graph][ver2] = max_clr
                save_clrs_true.append(save_clrs2)
            else:
                clrs_needed2 = save_clrs_true[check_true.index(deg_length2)]
                for ver4, clr2 in zip(b, clrs_needed2):
                    if ver4 not in dl and graph == 0 or ver4 not in il and graph == 1 or graph > 1:
                        coloring_vertex_keys[graph][ver4] = clr2
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
        if not coloring_color_keys[graph][0]:
            coloring_color_keys[graph].pop(0)
    return coloring_vertex_keys, coloring_color_keys, nb_dict


def twins_colorref(graphs, auto):
    isomorphisms = []
    all_graphs = list(graphs.values())

    f_twins = findFalseTwinsGraphs(all_graphs)
    t_twins = findTrueTwinsGraphs(all_graphs)

    needed = [i for i in range(len(all_graphs))]
    indexing = {i: k for i, k in zip(graphs.keys(), needed)}
    clr_vertex_init, clr_color_init, neighbours = twins_initialization(all_graphs, [], [], f_twins, t_twins)
    compensation_for_twins = []
    for gr in range(len(graphs)):
        comp = 1
        for pair in f_twins[gr]:
            comp *= math.factorial(len(pair))
        for pair2 in t_twins[gr]:
            comp *= math.factorial(len(pair2))
        compensation_for_twins.append(comp)
    for graph in graphs.keys():
        if not isomorphisms:
            isomorphisms.append([[graph], 0])
        else:
            for compare_graph in range(len(isomorphisms)):
                other_graph = isomorphisms[compare_graph][0][0]
                test_graphs = [graphs[i] for i in [other_graph, graph]]
                if len(test_graphs[0].vertices) != len(test_graphs[1].vertices):
                    clr_color = [{0: []}, {1: []}]
                elif compensation_for_twins[indexing[graph]] != compensation_for_twins[indexing[other_graph]]:
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
                        isomorphisms[compare_graph][1] = 1 * compensation_for_twins[indexing[graph]]
                        break
                    else:
                        fl_twins = [f_twins[p] for p in [indexing[other_graph], indexing[graph]]]
                        tr_twins = [t_twins[p] for p in [indexing[other_graph], indexing[graph]]]
                        automorphisms = branching([], [], test_graphs, clr_color, auto, fl_twins, tr_twins)
                        if automorphisms > 0:
                            isomorphisms[compare_graph][0].append(graph)
                            isomorphisms[compare_graph][1] = automorphisms * compensation_for_twins[indexing[graph]]
                            break
                        elif compare_graph < len(isomorphisms) - 1:
                            continue
                        else:
                            isomorphisms.append([[graph], 0])
                elif compare_graph < len(isomorphisms) - 1:
                    continue
                else:
                    isomorphisms.append([[graph], 0])
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
                    duo_f_twins, duo_twins = [f_twins[index], f_twins[index]], [t_twins[index], t_twins[index]]
                    aut = branching([], [], [all_graphs[index], all_graphs[index]],
                                    [clr_color2[0], clr_color2[0]], auto, duo_f_twins, duo_twins)
                    isomorphisms[iso][1] = aut * compensation_for_twins[index]
    return isomorphisms


def fast_coloring(graphs, clr_init, ver_init, neighbours_list):
    number_graphs = len(graphs)
    partition = clr_init
    color_i_init = list(clr_init[0].keys())
    queue = color_i_init
    max_color = max(color_i_init)
    max_list = [max_color for _ in range(number_graphs)]
    check = [set(), set()]
    while queue:
        if number_graphs == 2:
            if check[0] != check[1]:
                return [{0: []}, {1: []}]
        clr = queue.pop(0)
        check = [set(), set()]
        for gr in range(number_graphs):
            count, reverse_count, seen, refine = {}, {}, set(), set()
            for v in partition[gr][clr]:
                for u in neighbours_list[gr][v]:
                    if u not in seen:
                        clr_class = ver_init[gr][u]
                        check[gr].add(clr_class)
                        if len(partition[gr][clr_class]) > 1:
                            refine.add(clr_class)
                            count[u] = 1
                            seen.add(u)
                    else:
                        count[u] += 1
            for key, value in count.items():
                if value not in reverse_count:
                    reverse_count[value] = {key}
                else:
                    reverse_count[value].add(key)
            c_degrees = sorted(reverse_count.items())
            refine_ordered = sorted(list(refine))
            for c_i in refine_ordered:
                add_queue = []
                rest = partition[gr].pop(c_i)
                for c_deg, split in c_degrees:
                    if not rest:
                        break
                    new = rest & split
                    if new == rest and not add_queue:
                        partition[gr][c_i] = new
                        rest = rest - split
                        continue
                    if not new:
                        continue
                    rest = rest - split
                    if rest:
                        max_list[gr] += 1
                        new_color = max_list[gr]
                        partition[gr][new_color] = new
                        for j in new:
                            ver_init[gr][j] = new_color
                        add_queue.append([len(new), new_color])
                    else:
                        partition[gr][c_i] = new
                        if c_i not in queue:
                            add_queue.append([len(new), c_i])
                if rest:
                    partition[gr][c_i] = rest
                    if c_i not in queue:
                        add_queue.append([len(rest), c_i])
                if add_queue and gr == 0:
                    if len(add_queue) > 1:
                        d = sorted(add_queue)
                        for q in d[:-1]:
                            queue.append(q[1])
                    else:
                        queue.append(add_queue[0][1])
    return partition


def branching(d_list, i_list, graphs2, old_coloring, automorphism, false_t, true_t):
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
    key = get_most_vertices_color(multi_colors, True)
    x = sorted(list(colors_graph1[key]), key=lambda vertex: vertex.label)[0]
    # key = list(multi_colors.keys())[0]
    # x = list(colors_graph1[key])[0]
    d_sequence.append(x)
    num = 0
    for y in colors_graph2[key]:
        i_sequence = i_list.copy()
        i_sequence.append(y)
        initial_v, initial_c, neigh = twins_initialization(graphs2, d_sequence, i_sequence, false_t, true_t)
        clr_color_end = fast_coloring(graphs2, initial_c, initial_v, neigh)
        num += branching(d_sequence, i_sequence, graphs2, clr_color_end, automorphism, false_t, true_t)
        if num > 0 and not automorphism:
            return num
    return num


def get_most_vertices_color(multi_colors, choice):
    """
    Return the color class that has the most vertices.

    :param multi_colors: {color: [list of corresponding vertices]}, where length of corresponding vertices > 2.
    :param choice: set to True if we want to get the color with the most vertices; otherwise False for the least.
    """
    sorted_multi_colors = dict(sorted(multi_colors.items(), key=lambda item: (len(item[1])), reverse=True))
    # sort based on the degree of the vertices
    if choice:
        return list(sorted_multi_colors.keys())[0]
    else:
        return list(sorted_multi_colors.keys())[-1]


if __name__ == "__main__":
    decision = True
    # filename = 'twins_test_graphs.grl'
    # filename = 'SampleSetBranching/regulartwins.grl'
    filename = 'SampleGraphsFastColorRefinement/threepaths10240.gr'

    start = timeit.default_timer()
    results = twins_colorref(filename, decision)
    print(filename)
    if decision:
        print("Sets of isomorphic graphs:    Number of automorphisms:")
        for res in results:
            print(f"{res[0]}{' ' * (30 - len(str(res[0])))}{res[1]}")
    else:
        print("Sets of isomorphic graphs:")
        for res in results:
            print(f"{res[0]}")
    end = timeit.default_timer()
    print(f'Total computation time: {end - start}')
