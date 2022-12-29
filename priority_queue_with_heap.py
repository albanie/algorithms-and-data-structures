"""An implementation of a priority queue with a (binary) max-heap.

Heaps were originally introduced in 1964 by J. W. J. Williams in the context of
the Heapsort algorithm.

Reference:
- J. Williams, "Algorithm 232 – Heapsort", Communications of the ACM (1964)

The code draws inspiration from descriptions of Priority Queues and Binary Heaps:
- Chapter 8 of Elementary Algorithms by Liu Xinyu https://github.com/liuxinyu95/AlgoXY
- Chapter 6 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)

Note: this implementation assumes all keys are unique.

If you would like to read a "production quality" version of a priority queue you
may find the cpython implementation interesting:
https://github.com/python/cpython/blob/3.11/Lib/heapq.py

"""

def left_child(i: int) -> int:
    """Compute the index of the left child of node i.

    Args:
        i: the index of the node.

    Returns:
        The index of the left child of node i.
    """
    return 2 * i + 1


def right_child(i: int) -> int:
    """Compute the index of the right child of node i.

    Args:
        i: the index of the node.

    Returns:
        The index of the right child of node i.
    """
    return 2 * i + 2


def parent(i: int) -> int:
    """Compute the index of the parent of node i.

    Args:
        i: the index of the node.

    Returns:
        The index of the parent of node i.
    """
    return (i - 1) // 2


def max_heapify(A: list, heap_size: int, i: int):
    left = left_child(i)
    right = right_child(i)
    max_i = i
    if left < heap_size and A[left]["key"] > A[max_i]["key"]:
        max_i = left
    if right < heap_size and A[right]["key"] > A[max_i]["key"]:
        max_i = right
    if max_i != i:
        A[i], A[max_i] = A[max_i], A[i]
        max_heapify(A, heap_size, max_i)


def build_max_heap(A):
    heap_size = len(A)
    for i in range(heap_size // 2 - 1, -1, -1):
        max_heapify(A, heap_size, i)


class MaxPriorityQueue:

    def __init__(self, A: list):
        self.A = A
        self.heap_size = len(A)

    def get_maximum(self):
        """Return the maximum value in the priority queue.

        Returns:
            The maximum value in the priority queue.
        """
        return self.A[0]["value"]

    def pop_max(self):
        """Remove the maximum value from the priority queue.

        Returns:
            The maximum value in the priority queue.
        """
        max_value = self.get_maximum()
        self.A[0] = self.A[self.heap_size - 1]
        self.heap_size -= 1
        max_heapify(self.A, self.heap_size, 0)
        return max_value

    def increase_key(self, key, value):
        """Increase the key of the value in the priority queue.

        Args:
            key: the new key of the value
            value: the value to increase the key of
        """
        # locate the position of `value` in the underlying array
        i = 0
        while i < self.heap_size and self.A[i]["value"] != value:
            i += 1
        assert key >= self.A[i]["key"], f"requested to decrease key to {key}"
        assert key >= self.A[i]["key"], f"requested to decrease key {self.A[i]['key']} to {key}"
        self.A[i]["key"] = key # increase the key
        while i > 0 and self.A[i]["key"] > self.A[parent(i)]["key"]:
            self.A[i], self.A[parent(i)] = self.A[parent(i)], self.A[i]
            i = parent(i)

    def insert(self, key, value):
        """Insert value with given key into the priority queue

        Args:
            key: the key of the value to insert
            value: the value to insert
        """
        if self.heap_size == len(self.A):
            # expand underlying array to avoid heap overflow
            self.A.append(None)
        # use key that is guaranteed to be valid
        initial_key = float("-inf")
        self.A[self.heap_size] = {"key": initial_key, "value": value}
        self.heap_size += 1
        self.increase_key(key, value)

    def __repr__(self):
        summary = "\n".join(str(x) for x in self.A[:self.heap_size])
        return f"MaxPriorityQueue containing:\n{summary}"


def main():
    # pylint: disable=line-too-long
    # flake8: noqa: E501

    inital_queue = [
        # {"key": 0, "value": "red"},
    ]
    max_priority_queue = MaxPriorityQueue(A=inital_queue)
    print("Initial priority queue:")
    print(max_priority_queue)

    max_priority_queue.insert(key=3, value="green")
    max_priority_queue.insert(key=2, value="yellow")
    max_priority_queue.insert(key=4, value="blue")
    max_priority_queue.insert(key=-1, value="mauve")
    print("\nPriority queue after insertions:")
    print(max_priority_queue)

    print(f"\nPopped max:", max_priority_queue.pop_max())
    print(f"Popped max:", max_priority_queue.pop_max())
    print("\nPriority queue after pop max calls:")
    print(max_priority_queue)

    """
    Print out >>>

    Initial priority queue:
    MaxPriorityQueue containing:
    {'key': 0, 'value': 'red'}

    Priority queue after insertions:
    MaxPriorityQueue containing:
    {'key': 4, 'value': 'blue'}
    {'key': 3, 'value': 'green'}
    {'key': 2, 'value': 'yellow'}
    {'key': 0, 'value': 'red'}
    {'key': -1, 'value': 'mauve'}

    Popped max: blue
    Popped max: green

    Priority queue after pop max calls:
    MaxPriorityQueue containing:
    {'key': 2, 'value': 'yellow'}
    {'key': 0, 'value': 'red'}
    {'key': -1, 'value': 'mauve'}
    """

if __name__ == "__main__":
    main()
