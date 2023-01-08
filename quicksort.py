"""Simple implementations of the quicksort algorithm.

Quicksort was originally published by Tony Hoare in 1961

- Reference:
- T. Hoare, "Quicksort", Communications of the ACM (1961)

This code is based on the description of the algorithm in the following sources:
- Chapter 7 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)
- https://en.wikipedia.org/wiki/Quicksort
"""


def lomuto_partition(A: list, low: int, high: int) -> int:
    """Partition the array A[low:high+1] around the pivot A[high]
    using the Lomuto scheme.

    Args:
        A: the array to be partitioned.
        low: the index of the zeroth element of the subarray to be partitioned.
        high: the index of the last element of the subarray to be partitioned.

    Returns:
        The index of the pivot after partitioning.
    """
    pivot = high
    pivot_val = A[pivot]
    i = low
    for j in range(low, high):
        if A[j] <= pivot_val:
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[pivot] = A[pivot], A[i]
    return i


def quicksort_with_lomuto_partition(A: list, low: int = 0, high: int = None):
    """Sort the array A[low:high+1] using the quicksort algorithm with the
    partition scheme of Lomuto.

    Args:
        A: the array to be sorted.
        low: the index of the zeroth element of the subarray to be sorted.
        high: the index of the last element of the subarray to be sorted.
    """
    if high is None:
        high = len(A) - 1
    if low < high:
        pivot = lomuto_partition(A, low, high)
        quicksort_with_lomuto_partition(A, low, pivot - 1)
        quicksort_with_lomuto_partition(A, pivot + 1, high)


def hoare_partition(A: list, low: int, high: int) -> int:
    """Partition the array A[low:high+1] around the pivot A[low] using
    the Hoare scheme.

    Args:
        A: the array to be partitioned.
        low: the index of the zeroth element of the subarray to be partitioned.
        high: the index of the last element of the subarray to be partitioned.

    Returns:
        The index of the pivot after partitioning.

    Note: this is not quite the same as the Hoare partition scheme described in
    the original paper by Hoare. Hoare uses a random pivot, but this implementation
    (which follows CLRS) uses the zeroth element of the subarray as the pivot.
    """
    pivot_val = A[low]
    i = low - 1
    j = high + 1
    while True:
        while True:
            i += 1
            if A[i] >= pivot_val:
                break
        while True:
            j -= 1
            if A[j] <= pivot_val:
                break
        if i >= j:
            return j
        A[i], A[j] = A[j], A[i]


def quicksort_with_hoare_partition(A: list, low: int = 0, high: int = None):
    """Sort the array A[low:high+1] using the quicksort algorithm with the
    partition scheme of Hoare.

    Args:
        A: the array to be sorted.
        low: the index of the zeroth element of the subarray to be sorted.
        high: the index of the last element of the subarray to be sorted.
    """
    if high is None:
        high = len(A) - 1
    if low < high:
        pivot = hoare_partition(A, low, high)
        # NOTE: we use pivot instead of pivot - 1 for the left recursion
        quicksort_with_hoare_partition(A, low, pivot)
        quicksort_with_hoare_partition(A, pivot + 1, high)


def main():
    # pylint: disable=line-too-long
    # flake8: noqa: E501

    sample_list = [5, 2, 3, 1, 0]

    # use a copy to demonstrate the effect of quicksort (lomuto partition)
    A = sample_list[:]
    print("Array to be sorted:")
    print(A)

    quicksort_with_lomuto_partition(A)
    print("Array sorted with quicksort (lomuto partition):")
    print(A)

    B = sample_list[:]
    quicksort_with_hoare_partition(B)
    print("Array sorted with quicksort (hoare partition):")
    print(B)
    """
    Print out >>>

    Array to be sorted:
    [5, 2, 3, 1, 0]
    Array sorted with quicksort (lomuto partition):
    [0, 1, 2, 3, 5]
    Array sorted with quicksort (hoare partition):
    [0, 1, 2, 3, 5]
    """

if __name__ == "__main__":
    main()
