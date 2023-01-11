# Introduction to data structures and algorithms

This repo aims to provide minimalist implementations of data structures and algorithms in Python. The bare necessities. Each data structure is accompanied by a video lecture (and pdf slides).

## Data structures, algorithms and concepts

### Big O notation (and $\Theta$, $\Omega$, $o$, $\omega$ too)

- :movie_camera: [video lecture](https://www.youtube.com/watch?v=nsIQyK4Gf48)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-10-big-o-notation-and-its-companions.pdf)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-10-big-o-notation-and-its-companions/)

### Binary Search Trees

- :movie_camera: [video lecture](https://youtu.be/0woI8l0ZWmA)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-10-brief-guide-to-binary-search-trees.pdf)
- :hammer: [binary_search_tree.py](binary_search_tree.py)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-10-brief-guide-to-binary-search-trees/)

### Red-Black Trees

- :movie_camera: [video lecture](https://youtu.be/t-oiZnplv7g)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-12-brief-guide-to-red-black-trees.pdf)
- :hammer: [red_black_tree.py](red_black_tree.py)
- :hammer: [script.js (D3 visualisation)](visualisations/script.js)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-12-brief-guide-to-red-black-trees/)

### B-trees

- :movie_camera: [video lecture](https://youtu.be/7MqaHGWRS3E)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-12-brief-guide-to-b-trees.pdf)
- :hammer: [btree.py](btree.py) ([visualisation of outputs](graphviz-walkthroughs/btree.md))
- :fountain_pen: [detailed references](http://samuelalbanie.com/digests/2022-12-brief-guide-to-b-trees)

### Hash Tables

- :movie_camera: [video lecture](https://www.youtube.com/watch?v=r1XZGP5ppqQ)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-09-brief-guide-to-hash-tables.pdf)
- :hammer: [hash_table.py](hash_table.py)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-09-brief-guide-to-hash-tables/)

### Heapsort and Binary Heaps

- :movie_camera: [video lecture](https://youtu.be/ryRfapIQHW0)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-12-brief-guide-to-heapsort-and-binary-heaps.pdf)
- :hammer: [heapsort.py](heapsort.py) (related topic: [priority_queue_with_heap.py](priority_queue_with_heap.py))
- :fountain_pen: [detailed references](http://samuelalbanie.com/digests/2022-12-brief-guide-to-heapsort-and-binary-heaps)

### Quicksort

- :movie_camera: [video lecture](https://youtu.be/kbiKn1K08RM)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2023-01-brief-guide-to-quicksort.pdf)
- :hammer: [quicksort.py](quicksort.py)
- :fountain_pen: [detailed references](http://samuelalbanie.com/digests/2023-01-brief-guide-to-quicksort)

### Lower Bounds for Comparison Sorts

- :movie_camera: [video lecture](https://youtu.be/JWSiXs9aB5U)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2023-01-2023-01-brief-guide-to-comparison-sorting-lower-bounds.pdf)
- :fountain_pen: [detailed references](http://samuelalbanie.com/digests/2023-01-brief-guide-to-comparison-sorting-lower-bounds)

### Counting Sort

- :hammer: [counting_sort.py](counting_sort.py)

### Foundation models for code

Until recently, code for implementing data structures was largely written by hand. As of 2021, there have been exploratory efforts to employ neural networks for the task of generating code from natural language descriptions (this approach underpins the GitHub Copilot tool, for example). If you'd like to learn more, the video below describes Codex, a popular foundation model for code generation.

- :movie_camera: [YouTube video](https://www.youtube.com/watch?v=Wc7dcwF7QaA)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-07-codex.pdf)
- :page_facing_up: [arxiv paper](https://arxiv.org/abs/2107.03374)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-07-codex/)

## Further background

### Row-major order vs column-major order

- :movie_camera: [video lecture](https://youtu.be/b5lYGvcBjy4)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-09-row-major-vs-column-major.pdf)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-09-row-major-vs-column-major/)

### Why numbering should start at zero (according to Dijkstra)

- :movie_camera: [video lecture](https://youtu.be/saZnPDPyQHA)
- :bar_chart: [slides (pdf)](https://samuelalbanie.com/files/digest-slides/2022-09-why-numbering-should-start-at-zero-dijkstra.pdf)
- :fountain_pen: [detailed references](https://samuelalbanie.com/digests/2022-09-why-numbering-should-start-at-zero-dijkstra/)

## Further resources

### Books

The books below represent (in my opinion) high-quality learning/reference materials. 

- :orange_book: [Introduction to Algorithms (a.k.a "CLRS")](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) by Thomas H. Cormen et al.  - this was the primary reference used when developing the materials above. If you have a local library, it's worth checking in case they have a copy.
- :green_book: [algorithms.wtf](http://algorithms.wtf/) by Jeff Erickson (open-source)
- :green_book: + :hammer: [Elementary Algorithms](https://github.com/liuxinyu95/AlgoXY) by Liu Xinyu (open-source)
- :orange_book: [The Art of Computer Programming](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) by Donald E. Knuth. This is a series of books rather than a single book. The content is engaging, humorous and extraordinarily comprehensive. It is perhaps most useful as a reference for deep dives on topics, rather than an introductory learning resource (simply because the level of detail is so high).

### Visualisations

#### Red-black trees
![red-black tree growth gif](visualisations/red-black-tree-growth.gif)

#### B-trees
![btree visualisation](figs/btree.png)


## Requirements for install

To visualise the trees, you'll need to have a copy of pygraphviz:

```bash
conda install -c anaconda graphviz
pip install pygraphviz
```

## Additional comments

The repo is a work in progress. It aims to provide a reference for learning, not code for production (it has not been extensively tested to handle all edge cases). Pull requests are welcome.
