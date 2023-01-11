"""A simple implementation of the counting sort algorithm.

Counting sort was originally described by H. Seward in 1959 in his Master's thesis under
the name "Floating Digital Sort".

Reference:
- H. Seward, "Information sorting in the application of electronic digital computers to
business operations", Dissertation MIT (1954)

This code is based on the description of the algorithm in the following sources:
- https://en.wikipedia.org/wiki/Counting_sort
- Chapter 8 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)
"""


def counting_sort(A, k):
    """Sort the given array with the counting sort algorithm.

    Args:
        A: the array to be sorted.
        k: the number of possible values for the keys.

    Returns:
        The sorted array.

    NOTE: Counting sort assumes that all inputs are integers between 0 and k-1 inclusive.
    """
    n = len(A)
    counts = [0 for _ in range(k)]
    output = [None for _ in range(n)]
    for key in A:
        counts[key] += 1
    for i in range(1, k):
        counts[i] += counts[i - 1]
    for key in reversed(A):
        output[counts[key] - 1] = key
        counts[key] = counts[key] - 1
    return output


def main():
    A = [5, 2, 3, 1, 0, 2, 2, 4]
    # the number of possible keys (which range from 0 to k - 1)
    k = 6
    print("Array to be sorted:")
    print(A)
    B = counting_sort(A, k=k)
    print("Array sorted with counting sort:")
    print(B)

    """
    Print out >>>

    Array to be sorted:
    [5, 2, 3, 1, 0, 2, 2, 4]
    Array sorted with counting sort:
    [0, 1, 2, 2, 2, 3, 4, 5]
    """


if __name__ == "__main__":
    main()
