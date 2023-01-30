"""A parallel implementation of the Fibonacci sequence.

This code is based on the description of the algorithm in the following sources:
- https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/resources/mit6_172f18_lec7/
- Chapter 26 of T. H. Cormen, et al., "Introduction to algorithms", MIT press (2022)

Notes:
This implementation uses ThreadPoolExecutor to implement spawning/joining of threads.
If you run it with a standard CPython variant the parallel version will be slower than
the serial version. This is because the GIL effectively serializes the execution of the
threads. However, if you run it with Sam Gross' nogil version (install instructions here
https://github.com/colesbury/nogil) then you should see a speed up on a multicore machine.
"""
import time
import sys
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

# find the number of cores on the current system
MAX_THREADS = mp.cpu_count()


def fib_serial(n):
    """Compute the nth Fibonacci number in a serial fashion.

    Args:
        n: the index of the Fibonacci number to compute.
    Returns:
        The nth Fibonacci number.
    """
    if n < 2:
        return n
    x = fib_serial(n - 1)
    y = fib_serial(n - 2)
    return x + y


def fib_parallel(n, try_parallel=True):
    """Compute the nth Fibonacci number in a parallel fashion.

    Args:
        n: the index of the Fibonacci number to compute.
        try_parallel: whether to try to spawn a thread to compute the result.

    Returns:
        The nth Fibonacci number.

    Notes:
    1. The `try_parallel` argument is a slightly ugly hack to make the code faster.
    It is used to avoid calling threading.activeCount() in every recursive call (which is
    pretty slow and ends up dominating the recursion).

    2. We use "coarsening" - we don't spawn a new thread for every recursive call. Instead,
    we spawn new threads until we reach a certain threshold (MAX_THREADS). This is to avoid
    too much overhead from spawning threads (and checking for thread counts).
    """
    if n < 2:
        return n

    # only retrieve the thread count if we are potentially going to spawn another thread
    # (since retrieving the thread count is expensive)
    if try_parallel:
        thread_count = threading.activeCount()

    # We apply some coarsening (i.e. don't go too bonkers with the number of threads)
    if try_parallel and thread_count <= MAX_THREADS:
        with ThreadPoolExecutor() as executor:
            x_future = executor.submit(fib_parallel, n - 1)
            y = fib_parallel(n - 2)
        x = x_future.result()  # note that this blocks until x is ready
    else:
        # Now we've used all our threads, so we just do the computation serially for
        # the remainder of the recursion.
        x = fib_parallel(n - 1, try_parallel=False)
        y = fib_parallel(n - 2, try_parallel=False)
    return x + y


def main():
    target = 34

    start_time = time.perf_counter()
    res = fib_serial(target)
    end_time = time.perf_counter()
    print(f"serial fibonacci (n={target}): {res}) {end_time - start_time} secs")

    start_time = time.perf_counter()
    res = fib_parallel(target)
    end_time = time.perf_counter()

    nogil = getattr(sys.flags, "nogil", False)
    status = "using nogil" if nogil else "using the GIL"
    print(f"parallel fibonacci (n={target}): {res}) {end_time - start_time} secs {status}")

    """
    Print out >>>

    serial fibonacci (n=34): 5702887) 1.134940978 secs
    parallel fibonacci (n=34): 5702887) 0.45259864299999997 secs using nogil
    """


if __name__ == "__main__":
    main()
