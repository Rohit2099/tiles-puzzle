# Sliding-Tile Puzzle

## Problem Statement:

The sliding-tile puzzle consists of:

-   **Three black tiles** (represented as `B`).
-   **Three white tiles** (represented as `W`).
-   An **empty space** (represented as `_`).

### Puzzle Rules:

1. A tile may move into an adjacent empty location. This has a cost of **1**.
2. A tile can hop over one or two other tiles into the empty position. The cost is equal to the number of tiles jumped over.

### Goal:

The goal is to move all the white tiles to the left of all the black tiles. The position of the empty space is **not important** in the final configuration.

---

## Questions:

### Q1.1: Puzzle Implementation

-   **Task:** Implement the sliding-tile puzzle that accepts any valid configuration of the tiles (W, B, \_) as the input and solves the puzzle.

### Q1.2: Heuristic Search Algorithm

-   **Task:** Propose and implement a heuristic search algorithm for the puzzle. The heuristic should help in solving the puzzle more efficiently by guiding the search towards the goal state.

### Q1.3: Cost Comparison

-   **Task:** Compare the costs involved in both cases (adjacent movement and jumping over other tiles) for the same input configuration.

### Q1.4: State Space Representation

-   **Task:** Display the entire state space as a diagram and highlight the path with the lowest cost.

### Q1.5: Goal Configurations and Inferences

-   **Task:** Generate all possible goal configurations and their associated costs for a given input configuration.
-   **Inference:** Suggest an inference regarding the position of the empty space in relation to the cost involved. Provide examples and support your claim with program-generated outputs.

## Components

The code includes the following key components for solving the puzzle:

1. **Breadth-First Search (BFS)**
2. **A\* Search**
3. **A\* Search for generating all goals**

### 1. Breadth-First Search (BFS)

-   To solve the puzzle using BFS, **uncomment** the following lines:
    -   **Line 498**: `puzzle.solveBfs(print_tree=True)`
    -   **Line 499**: `puzzle.getSolutionBfs()`
-   **Optional**: Set `print_tree=True` or `print_tree=False` to control whether the entire search space is displayed (Warning: Large output).

### 2. A\* Search

-   To solve the puzzle using A\*, **uncomment** the following lines:
    -   **Line 500**: `puzzle.solveAStar(print_tree=True)`
    -   **Line 501**: `puzzle.getSolutionAStar()`
-   **Optional**: Set `print_tree=True` or `print_tree=False` to control whether the entire search space is displayed.

### 3. A\* Search for All Goals

-   To generate all possible goals using A\*, **uncomment** the following lines:
    -   **Line 502**: `puzzle.generateAllGoalsAStar(print_tree=True)`
    -   **Line 503**: `puzzle.printAllGoals()`
-   **Optional**: Set `print_tree=True` or `print_tree=False` to control whether the entire search space is displayed.

## Execution

1. Navigate to the directory where the Python file (`puzzle.py`) is located.
2. Run the following command in your terminal:
    ```bash
    python3 puzzle.py
    ```
