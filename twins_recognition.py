from graph_io import *
import timeit


def findFalseTwinsGraph(graph):
    twins = []  # Set to store pairs of twin vertices
    twins_num = []
    neighbours_freq = {}
    ver_dict = {}
    num_ver = {}
    i = 0
    for vertex in graph.vertices:
        ver_dict[vertex] = i
        num_ver[i] = vertex
        i += 1

    for vertex in graph.vertices:
        neighbours = set(vertex.neighbours)
        neighbour_ids = [ver_dict[neighbor] for neighbor in neighbours]
        # Sort the list of neighbor IDs
        neighbour_ids.sort()
        # Convert the sorted list of neighbor IDs to a tuple for hashability
        neighbour_key = tuple(neighbour_ids)

        if neighbour_key in neighbours_freq:
            # If the neighborhood already exists, mark vertices as twins
            neighbours_freq[neighbour_key].append(ver_dict[vertex])
        else:
            # Store the frequency of this neighborhood
            neighbours_freq[neighbour_key] = [ver_dict[vertex]]

    for twin in neighbours_freq.values():
        if (len(twin) > 1):
            twin.sort()
            twin = tuple(twin)
            twins_num.append(twin)
            twins_num = list(set(twins_num))
            twins_num.sort()
    # print(twins_num)
    for t in twins_num:
        twin = []
        for tt in t:
            twin.append(num_ver[tt])
        twins.append(twin)
    # print("the number of Ftwins are ",len(twins))

    return twins


def findFalseTwinsGraphs(graphs):
    twins_list = []

    for graph in graphs:
        twins = findFalseTwinsGraph(graph)
        twins_list.append(twins)

    return twins_list


def findTrueTwinsGraphs(graphs):
    twins_list = []

    for graph in graphs:
        twins = findTrueTwinsGraph(graph)
        twins_list.append(twins)

    return twins_list


def findTrueTwinsGraph(graph):
    twinsT = []  # Set to store tuples of twin vertices
    twins_num_T = []
    vertex_twins = {}
    checked = set()
    vertex_num = {}
    num_vertex = {}
    i = 0
    for vertex in graph.vertices:
        vertex_num[vertex] = i
        num_vertex[i] = vertex
        i += 1

    for v in graph.vertices:
        if v not in checked:
            neighbours = set(v.neighbours)
            for n in neighbours:
                neighbours.remove(n)
                otherNeighbours = set(n.neighbours)
                otherNeighbours.remove(v)
                if neighbours == otherNeighbours:
                    if v in vertex_twins.keys():
                        vertex_twins[v].append(vertex_num[n])
                        # print(vertex_twins)
                    else:
                        vertex_twins[v] = [vertex_num[n]]
                        # print(vertex_twins)
                neighbours.add(n)
            #checked.add(n)
    checked.add(v)
    for k in vertex_twins.keys():
        twinT = [vertex_num[k]]
        twinT.extend(vertex_twins[k])
        twinT.sort()
        twinT = tuple(twinT)
        twins_num_T.append(twinT)
        twins_num_T = list(set(twins_num_T))
        twins_num_T.sort()
    # print(twins_num_T)

    for t in twins_num_T:
        twin = []
        for tt in t:
            twin.append(num_vertex[tt])
        twinsT.append(twin)
    # print("the number of twins are ", len(twinsT))

    return twinsT


if __name__ == "__main__":
    start = timeit.default_timer()
    # filename = 'SampleGraphsFastColorRefinement/threepaths10240.gr'
    filename = 'SampleSetBranching/regulartwins.grl'
    # filename = 'twins_test_graphs.grl'
    with open(filename) as g:
        graphs = load_graph(g, read_list=True)[0]

    print("TrueTwins:", findTrueTwinsGraphs(graphs)[3], '\n')
    # print("FalseTwins:", findFalseTwinsGraphs(graphs)[0])
    end = timeit.default_timer()
    print(end - start)
