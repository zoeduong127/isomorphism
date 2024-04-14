from preprocessing import *
from utils import *
from tree import isomorphism_algorithm
from complete_edgeless_graphs import *
from fast_coloring import fast_colorref
from standard_coloring import basic_colorref
from twins_recognition import *
from twins_coloring import twins_colorref


def preprocess(graphs):
    # Split the graphs in three dictionaries: trees, complete/edgeless, and other graphs.
    trees_recognized = recognize_trees(graphs)
    trees, complete_edgeless, remaining = {}, {}, {}
    
    for index, graph in enumerate(graphs):
        if trees_recognized[index]:
            trees[index] = graph
        else:
            if isCompleteGraph(graph) or isEdgelessGraph(graph):
                complete_edgeless[index] = graph
            else:
                remaining[index] = graph
    return trees, complete_edgeless, remaining


def run(file, decision, fast, twin):
    # First read the graphs.
    graphs = read_file(file)
    # Then distinguish trees, complete/edgeless, and the other graphs.
    trees, easy_automorphism, other_graphs = preprocess(graphs)
    # Initialize empty lists for the three different categories of results.
    results_trees, results_easy, results_other = [], [], []

    # Compute which graphs are isomorphic and the number of automorphisms for each category.
    if trees:
        results_trees = isomorphism_algorithm(trees, decision)
    if easy_automorphism:
        results_easy = easy_isomorphism(easy_automorphism)
    if other_graphs:
        if fast:
            if twin:
                results_other = twins_colorref(other_graphs, decision)
            else:
                results_other = fast_colorref(other_graphs, decision)
        else:
            results_other = basic_colorref(other_graphs, decision)

    # Add the three categories together, so we have one list with the combined results.
    result = results_trees + results_easy + results_other

    return sorted(result)


if __name__ == "__main__":
    # If True we compute the number of automorphisms. If False we do not.
    automorphisms = True
    # If True we use fast colorref with a branching rule. If False we use standard colorref without branching rule.
    fast_clr = True
    # If True we use twins recognition. If False we use no twins' recognition.
    twins = True
    filename = 'Sample_files/basicAut2.gr'
    # path = f'TestInstances/{filename}'
    print(f'Filename: {filename}')

    start = timeit.default_timer()
    results = run(filename, automorphisms, fast_clr, twins)
    print_result(automorphisms, results)
    end = timeit.default_timer()
    print(f'Total computation time: {end - start}')
