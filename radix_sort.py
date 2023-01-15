"""A simple implementation of the radix sort algorithm.

Radix sort is a "folk" algorithm, i.e. it is not based on a specific paper, that
incorporates several ideas. Typically it uses counting sort as a subroutine (as
we do here), but other stable sorting algorithms can be used as well.

This code is based on the description of the algorithm in the following sources:
- https://en.wikipedia.org/wiki/Radix_sort
- Chapter 8 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)
"""

def counting_sort_on_digit(A, k, d, digit_pos):
    """Sort the given array with the counting sort algorithm on the given digit.

    Args:
        A: the array to be sorted.
        k: the number of possible values for the keys.
        d: the number of digits in the keys.
        digit_pos: the position of the digit to sort on

    Returns:
        The sorted array.

    NOTE: Counting sort assumes that all inputs are tuples of integers between
    0 and k-1 inclusive.
    """

    def subkey(key):
        """Helper function to extract the digit at the given position from the key."""
        str_key = str(key).zfill(d)
        return int(str_key[digit_pos])

    n = len(A)
    counts = [0 for _ in range(k)]
    output = [None for _ in range(n)]
    for key in A:
        counts[subkey(key)] += 1
    for i in range(1, k):
        counts[i] += counts[i - 1]
    for key in reversed(A):
        output[counts[subkey(key)] - 1] = key
        counts[subkey(key)] = counts[subkey(key)] - 1
    return output


def radix_sort_lsd(A, d, k):
    """Sort the given array with the radix sort algorithm using a
    least significant digit (LSD) ordering.

    Args:
        A: the array to be sorted.
        d: the number of digits in the keys.
        k: the number of possible digit values

    Returns:
        The sorted array.
    """
    for digit_pos in range(d - 1, -1, -1):
        # we use counting sort as our stable sort
        A = counting_sort_on_digit(A, k, d, digit_pos)
    return A


def main():
    A = [314, 712, 612, 201, 111]
    # the number of digits in each key
    d = 3
    k = 8
    print("Array to be sorted:")
    print(A)
    B = radix_sort_lsd(A, d=d, k=k)
    print("Array sorted with radix sort (LSD):")
    print(B)

    """
    Print out >>>

    Array to be sorted:
    [314, 712, 612, 201, 111]
    Array sorted with radix sort (LSD):
    [111, 201, 314, 612, 712]
    """


if __name__ == "__main__":
    main()