# Price Tracker Explanation for Real-Time Price Monitoring

### Implementation Rules
- Use only basic Python data structures (lists, tuples)
- No hash-based lookups (dictionaries, sets)
- No built-in search or sorting utilities
- Implement all algorithms manually using loops and conditionals

## Design Reasoning

Initially, when approaching this problem, the first step was to identify which algorithms could potentially satisfy 
the requirements and efficiently support the operations. I considered whether a single algorithm would be sufficient
to meet these requirements or whether a combination of two or more algorithms would be necessary to achieve an 
effective solution.

- **Point update** — a price changes for one period
- **Point query** — read the price for one period
- **Range query** — aggregate over consecutive periods
- **Range/global extreme** — min or max without scanning everything

### 1. Array + Binary Heap

The initial intuition was to combine an array, providing O(1) point lookups and updates by index, with a binary heap 
to achieve O(1) access to the minimum or maximum value. However, supporting both minimum and maximum queries would 
require maintaining two separate heaps alongside the array, keeping all three structures synchronised. This introduces
additional complexity and increases the risk of inconsistencies during updates.

Furthermore, binary heaps are designed for priority-based operations rather than indexed updates. If a specific 
settlement period needs to be modified, the heap must first be searched to locate the corresponding element, which 
requires O(n) time. Once located, the update operation itself can be performed in O(log n) time to restore the 
heap property. Therefore, the overall complexity of updating an arbitrary settlement period becomes O(n), however 
if location is known then it is O(log n).

| Operation | Array + Binary Heap |
| --------- |--------------------:|
| Get min  |                O(1) |
| Get max  |                O(1) |
| Insert    |            O(log n) |
| Delete    |            O(log n) |
| Search    |    O(n) or O(log n) |

- Space complexity: O(n)

### 2. Skip List

A skip list is a probabilistic data structure that provides average-case O(log n) time complexity for searching, 
inserting, and deleting elements in a sorted sequence. Without a tail pointer, retrieving the maximum price would
require traversing the upper levels of the skip list, resulting in an average time complexity of O(log n).

Adding a tail pointer reduces the time needed to access the maximum value, but it introduces additional memory 
overhead. Despite this extra cost, skip lists have the advantage of supporting efficient concurrent access, 
making them useful in applications where multiple processes or threads need to interact with the data structure
simultaneously.

| Operation |                            Skip list |
| --------- |-------------------------------------:|
| Get min  |                                 O(1) |
| Get max  | O(1) with tail pointer else O(log n) |
| Insert    |                             O(log n) |
| Delete    |                             O(log n) |
| Search    |                             O(log n) |

- Expected space complexity: O(n)
- Worst-case space complexity: O(n log n)

### 3. Red-Black Tree (Dynamic Ordered Data)

A self-balancing BST provides guaranteed O(log n) time complexity for insertions, updates, and lookups while 
maintaining elements in sorted order. However, efficiently accessing the minimum and maximum values requires 
additional pointers, which increases memory overhead. These structures are also more complex to implement due to 
their balancing operations, making them harder to maintain, test, and debug. Furthermore, depending on the tree 
layout and memory allocation, Red-Black trees may experience poor cache locality, potentially reducing real-world
performance despite strong theoretical efficiency.

| Operation |                  Red-Black Tree |
| -------- |--------------------------------:|
| Get min  | O(1) with pointer else O(log n) |
| Get max  | O(1) with pointer else O(log n) |
| Insert   |                        O(log n) |
| Delete   |                        O(log n) |
| Search   |                        O(log n) |

- Space complexity: O(n)

### 4. Segment Tree — Chosen

Uses an iterative approach based on a divide-and-conquer strategy, allowing efficient range-based queries and making
it well suited for storing and retrieving aggregate statistics across intervals. The array-based structure also 
provides good cache locality, as data is stored contiguously in memory, improving practical performance. However,
one drawback is the additional memory overhead required for storing the tree structure, resulting in O(2n) space 
in the standard implementation, which simplifies to O(n).

| Operation | Segment Tree |
|---------|-------------:|
| Get min |         O(1) |
| Get max |         O(1) |
| Insert  |     O(log n) |
| Delete  |     O(log n) |
| Search  |     O(log n) |

- Space complexity: O(n)


- **Point update** in O(log n)
- **Point lookup** in O(1)
- **Range query** in O(n)
- **Range/global extreme** in O(1)


Segment tree, I believe perhaps might be a better algorithm to implement for this task: it meets all four requirements 
with logarithmic bounds and is materially simpler to implement correctly than a red-black tree, given a fixed set of
periods and the constraint to build everything from lists and loops. However, both red-black tree and segment tree 
solve different problems so it depends on what future implementation is required
