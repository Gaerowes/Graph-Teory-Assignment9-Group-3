# Graph-Theory-Assignment9-Group-3

Implementation of Planarity Checking Algorithms for the Graph Theory course at Institut Teknologi Sepuluh Nopember (ITS).

---

## 1. Identity

**Informatics ITS Graph Theory Class — Group 3**

| Name | Student ID |
|---|---|
| Dzulfiqar Rafi'ussunnah | 5025251011 |
| Padhang Abiyu Fikri | 5025251014 |
| Aditya Lingga Mardika | 5025251158 |
| Muhammad Faris Alfarrel | 5025251002 |

---

## 2. Short Explanation About Algorithms

This project implements two distinct algorithms to determine whether a given graph is planar.

A **Planar Graph** is a graph that can be drawn on a plane such that no two edges intersect, except at their shared endpoints.

The algorithms implemented in this project are:

### 2.1 [First Algorithm Name]

[Insert the name of the first planarity checking algorithm.]

**Short Explanation:**

[Explain how the algorithm determines whether a graph is planar. Describe its main steps, approach, and how it identifies or constructs a planar embedding.]

### 2.2 Left-Right Planarity Testing Algorithm

The Left-Right Planarity Testing Algorithm determines whether a graph is planar by analyzing the relative positions of edges during a depth-first search (DFS).

The algorithm uses a DFS tree and maintains constraints that describe the relative left-right ordering of edges.

The main steps are:

1. Perform a depth-first search (DFS) on the graph.
2. Construct a DFS tree and identify back edges.
3. Calculate the low-point values of vertices.
4. Process the edges in a specific order while maintaining left-right constraints.
5. Test whether the constraints can be satisfied without creating edge crossings.

If the constraints are consistent, the graph is planar. Otherwise, the graph is non-planar.

---

## 3. Prerequisites to Run the Code

The following software and tools are required to run the implementations:

- Python 3.x or another supported programming language.
- Required libraries or dependencies (if any).
- Git (optional, for cloning the repository).

### Dependencies

the implementation uses only standard libraries.

---

## 4. Instructions to Run the Code

### 4.1 Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Gaerowes/Graph-Theory-Assignment9-Group-3.git
```

Navigate to the project directory:

```bash
cd Graph-Theory-Assignment9-Group-3
```

### 4.2 Prepare the Input

Prepare the graph input according to the format required by the implementation.

The input should contain the number of vertices, the number of edges, and the edge list.

Example:

```text
0 1
0 2
0 3
0 4
1 2
1 3
1 4
2 3
2 4
3 4
```

### 4.3 Run the First Algorithm

```bash
python [first_algorithm].py < input.txt
```

### 4.4 Run the Second Algorithm

```bash
python planarity_lr.py k5.txt
```


---

## 5. Input for Sample Run

The following input is used to demonstrate the execution of the implemented algorithms.

### Sample Input

```text
0 1
0 2
0 3
0 4
1 2
1 3
1 4
2 3
2 4
3 4
```

### Expected Result

```text
The result indicates whether the input graph is planar or non-planar.
```


---

## 6. Result of Sample Run

The following section presents the execution results of the implemented algorithms.

### 6.1 [First Algorithm Name]

**Sample Output:**

```text
[Insert sample output here]
```

**Execution Screenshot:**

![First Algorithm Result](images/first_algorithm_result.png)

### 6.2 Left-Right Planarity Testing Algorithm

**Sample Output:**

```text
NON-PLANAR
```

**Execution Screenshot:**

<img width="650" height="87" alt="image" src="https://github.com/user-attachments/assets/b601424c-7c7a-4a32-8857-c8444fee287c" />


---

## 7. AI Tools Usage Disclosure

AI tools were used as an assistance tool during the development and documentation process.

The use of AI included:

- Assisting with the understanding of planarity checking algorithms.
- Supporting the preparation and improvement of README documentation.

All implementations, algorithm explanations, and execution results were reviewed and verified by the group members.

---

## 8. Conclusion

This project implements two distinct algorithms for checking the planarity of a graph.

The implementations demonstrate different approaches to determining whether a graph can be embedded in a plane without edge crossings.

The project provides an opportunity to understand graph planarity and the application of graph algorithms in computational problems.

---

