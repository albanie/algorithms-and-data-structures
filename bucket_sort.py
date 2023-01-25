"""A simple implementation of the bucket sort algorithm.

Bucket sort is a distribution algorithm that involves three steps:
1. Scatter - distribute keys to buckets
2. Sort - sort keys within each bucket
3. Gather - gather the sorted keys in order

This code is based on the description of the algorithm in the following sources:
- https://en.wikipedia.org/wiki/bucket_sort
- Chapter 8 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)
"""


def bucket_sort(A: list):
    """Sort the given input A using bucket sort.

    Args:
        A: the array to be sorted.

    Returns:
        The sorted array.
    """
    num_buckets = len(A)
    buckets = [[] for _ in range(num_buckets)]
    for key in A:   # scatter
        buckets[int(num_buckets * key)].append(key)
    for bucket in buckets:
        insertion_sort(bucket)
    return [x for bucket in buckets for x in bucket]  # gather


def insertion_sort(A: list):
    """Sort the given input A using insertion sort.

    Args:
        A: the array to be sorted.

    Returns:
        The sorted array.
    """
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
    return A


def main():
    A = [0.21, 0.4, 0.18, 0.8, 0.13]
    # the number of digits in each key
    print("Array to be sorted:")
    print(A)
    A = bucket_sort(A)
    print("Array sorted with bucket sort:")
    print(A)

    """
    Print out >>>

    Array to be sorted:
    [0.21, 0.4, 0.18, 0.8, 0.13]
    Array sorted with bucket sort:
    [0.13, 0.18, 0.21, 0.4, 0.8]
    """


if __name__ == "__main__":
    main()
