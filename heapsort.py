"""An implementation of heapsort in Python.

Heapsort was originally introduced in 1964 by J. W. J. Williams and refined by
R. W. Floyd in 1964 to use in-place sorting.

References:
- J. Williams, "Algorithm 232 – Heapsort", Communications of the ACM (1964)
- R. Floyd, "Algorithm 245 – Treesort 3", Communications of the ACM (1964)

The code draws inspiration from several descriptions of Heapsort:
- Chapter 8 of Elementary Algorithms by Liu Xinyu https://github.com/liuxinyu95/AlgoXY
- Chapter 6 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)

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
    if left < heap_size and A[left] > A[max_i]:
        max_i = left
    if right < heap_size and A[right] > A[max_i]:
        max_i = right
    if max_i != i:
        A[i], A[max_i] = A[max_i], A[i]
        max_heapify(A, heap_size, max_i)


def build_max_heap(A):
    heap_size = len(A)
    for i in range(heap_size // 2 - 1, -1, -1):
        max_heapify(A, heap_size, i)


def heapsort(A):
    """An in-place implementation of heapsort."""
    build_max_heap(A)
    heap_size = len(A)
    while heap_size > 1:
        A[0], A[heap_size - 1] = A[heap_size - 1], A[0]
        heap_size = heap_size - 1
        max_heapify(A, heap_size, 0)


def naive_heapsort(A):
    """A naive implementation of heapsort that requires additional memory"""
    build_max_heap(A)
    heap_size = len(A)
    sorted_A = [None for _ in range(len(A))]
    while heap_size > 1:
        sorted_A[heap_size - 1] = A[0]
        A[0], A[heap_size - 1] = A[heap_size - 1], A[0]
        heap_size = heap_size - 1
        max_heapify(A, heap_size, 0)
    sorted_A[0] = A[0]
    return sorted_A


def main():
    # pylint: disable=line-too-long
    # flake8: noqa: E501

    sample_list = [3, 2, 1, 8, 9, 12, 4, 5, 6, 7, 10, 11]

    # use a copy to demonstrate the effect of heapsort
    A = sample_list[:]
    print("Array to be sorted:")
    print(A)

    heapsort(A)
    print("Sorted array:")
    print(A)

    # use another copy to demonstrate the effect of naive_heapsort
    B = sample_list[:]
    print("Array to be sorted:")
    print(B)

    print("Sorted array with naive heapsort:")
    print(naive_heapsort(B))
    """
    Print out >>>

    Array to be sorted:
    [3, 2, 1, 8, 9, 12, 4, 5, 6, 7, 10, 11]
    Sorted array:
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    Array to be sorted:
    [3, 2, 1, 8, 9, 12, 4, 5, 6, 7, 10, 11]
    Sorted array with naive heapsort:
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """


if __name__ == "__main__":
    main()
