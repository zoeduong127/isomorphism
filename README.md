# module7_graph-isomorphism

## Description
This is the project in module 7 for TCS & AM where we have to solve GI problem and #Aut problem with the given graphs (regardless of sizes and types).

## How to start
Download the whole project and open extracted folder with your preferred Python IDE. 

Make sure you put the graph instances in the same folder with the `final.py` file.

To run the test instances, navigate to `final.py` file. There are three conditions to run (all conditions are set to **True** by default): 

- automorphisms:
If you want to calculate how many automorphisms,
you can set this to **True**. Otherwise, set it to **False** to solve only GI problem.

- fast_clr:
If you want to use 'Fast Color refinement' function,
you can set this to **True**. Otherwise, set it to **False** to use standard color refinement.

- twins:
If you want to preprocess by recognizing <mark>**twins**</mark>,
you can set this to **True**. Otherwise, set it to **False** to run without twins pre-processing.

For testing, you need to rename the variable 
`filename` into your actual file name. 

For example, you can set as below:

```python
filename = "basicAut1.grl"
```

## Author acknowledgement
- Tijn Minks <br> t.s.minks@student.utwente.nl
- Huyen Duong duongthuhuyen@student.utwente.nl
- Khanh Nguyen nguyenhoangnamkhanh@student.utwente.nl
- Shun Nishijima s.nishijima@student.utwente.nl


