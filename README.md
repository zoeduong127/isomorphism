# module7_graph-isomorphism

## How to start

To run the test instances, we use "final.py" file.
There are three conditions to run "final.py".

- fast:
If you want to run 'Fast Color refinement' function,
you can set this to "True".
- twins:
If you want to run 'twins' function,
you can set this to "True".
- automorphism:
If you want to calculate how many automorphisms with 'automorphism' function,
you can set this to "True".

For testing, you need to set the filename from the test instances.
For example, you can set like below.

```python
filename = "test/basicAut1.gr"
```

## Test and Deploy

When you run the code,
the code will do preprocessing checks as well.
It checks whether

- trees:
It runs specific algorithms for tree types of graphs
- Complete Graph:
It runs "easy_isomorphism" function instead of complicated isomorphism_algorithm.
To make it faster.
- others:
It runs "Basic Color Refinement"

## Description
