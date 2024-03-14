from graph_io import *
import os
import time


def initialization(graphs):
    number = len(graphs)
    colouring_v_keys = [{} for _ in range(number)]
    colouring_c_keys = [{} for _ in range(number)]
    nb_list = [{} for _ in range(number)]
    for graph in range(len(graphs)):
        for v in graphs[graph].vertices:
            neighbours = v.neighbours
            # degree = len(neighbours)
            nb_list[graph][v] = neighbours
            colouring_v_keys[graph][v] = 1
            if colouring_c_keys[graph] != {}:
                colouring_c_keys[graph][1].append(v)
            else:
                colouring_c_keys[graph][1] = [v]
    return colouring_v_keys, colouring_c_keys, nb_list


def basic_colorref(file):
    with open(file) as g:
        graphs = load_graph(g, read_list=True)[0]
    clr_vertices, clr_colour, neighbours_list = initialization(graphs)
    number_graphs = len(graphs)
    iterations_list = [1 for _ in range(number_graphs)]
    finished = [False for _ in range(number_graphs)]
    while False in finished:
        new_clr_colour = [{} for _ in range(number_graphs)]
        new_clr_vertices = [{} for _ in range(number_graphs)]
        all_colours = []
        for k in clr_colour:
            all_colours.extend(list(k.keys()))
        all_colours = list(set(all_colours))
        max_colour = max(all_colours)
        for colour in all_colours:
            clr_seen = {}
            for gr in range(number_graphs):
                if finished[gr] is False:
                    if colour not in clr_colour[gr]:
                        continue
                    v = clr_colour[gr][colour]
                    for vertex in v:
                        next_neighbours = sorted([clr_vertices[gr][nb] for nb in neighbours_list[gr][vertex]])
                        if clr_seen != {}:
                            if next_neighbours in clr_seen.values():
                                key = list(clr_seen.keys())[list(clr_seen.values()).index(next_neighbours)]
                                if key in new_clr_colour[gr].keys():
                                    new_clr_colour[gr][key].append(vertex)
                                    new_clr_vertices[gr][vertex] = key
                                else:
                                    new_clr_colour[gr][key] = [vertex]
                                    new_clr_vertices[gr][vertex] = key
                            else:
                                max_colour += 1
                                new_colour = max_colour
                                clr_seen[new_colour] = next_neighbours
                                new_clr_colour[gr][new_colour] = [vertex]
                                new_clr_vertices[gr][vertex] = new_colour
                        else:
                            clr_seen[colour] = next_neighbours
                            new_clr_colour[gr][colour] = [vertex]
                            new_clr_vertices[gr][vertex] = colour
                else:
                    new_clr_colour[gr] = clr_colour[gr]
        for g in range(number_graphs):
            if len(clr_colour[g]) != len(new_clr_colour[g]):
                iterations_list[g] += 1
            else:
                finished[g] = True
        clr_colour = new_clr_colour
        clr_vertices = new_clr_vertices
    output = isomorphism(graphs, clr_colour, iterations_list)
    return output


def isomorphism(graphs, final_colouring, iterations):
    check, result = [], []
    for j in range(len(final_colouring)):
        graph_coloured = {k: len(v) for k, v in final_colouring[j].items()}
        if graph_coloured in check:
            result[check.index(graph_coloured)][0].append(j)
        else:
            check.append(graph_coloured)
            if len(final_colouring[j]) == len(graphs[j].vertices):
                result.append(([j], iterations[j], True))
            else:
                result.append(([j], iterations[j], False))
    return result


if __name__ == "__main__":
    start = time.time()
    filename = 'Benchmark/CrefBenchmark6.grl'
    # filename = 'SampleGraphsBasicColorRefinement/colorref_smallexample_4_16.grl'
    print('Sets of possibly isomorphic graphs: \n{}\n'.format(basic_colorref(filename)))
    end = time.time()
    print(end - start)

    # directory = 'SampleGraphsBasicColorRefinement'
    # for filename in os.listdir(directory):
    #     if filename.endswith('.grl'):
    #         filepath = os.path.join(directory, filename)
    #         print(filepath)
    #         print('Sets of possibly isomorphic graphs: \n{}\n'.format(basic_colorref(filepath)))
