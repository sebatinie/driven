import threading
import time
from concurrent.futures import ThreadPoolExecutor


def cpu_bound_task(n):
    """
    CPU-intensive task.
    """
    total = 0

    for i in range(n):
        total += i * i

    return total


def single_threaded_execution(iterations, n):
    """
    Execute CPU-bound task sequentially.
    """
    start_time = time.time()

    for _ in range(n):
        cpu_bound_task(iterations)

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"\nSingle-threaded execution completed in {execution_time:.4f} seconds")

    return execution_time


def multi_threaded_execution(iterations, n, num_threads):
    """
    Execute CPU-bound task using threads.
    """
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(cpu_bound_task, iterations)
            for _ in range(n)
        ]

        for future in futures:
            future.result()

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Multi-threaded execution completed in {execution_time:.4f} seconds")

    return execution_time


def main():
    iterations = 10_000_000
    n = 5
    num_threads = 4

    print("=== GIL Demonstration: CPU-Bound Task ===")
    print(f"Iterations per task : {iterations}")
    print(f"Number of tasks     : {n}")
    print(f"Number of threads   : {num_threads}")

    single_time = single_threaded_execution(iterations, n)

    multi_time = multi_threaded_execution(
        iterations,
        n,
        num_threads
    )

    print("\n=== Performance Comparison ===")
    print(f"Single-threaded Time : {single_time:.4f} seconds")
    print(f"Multi-threaded Time  : {multi_time:.4f} seconds")

    if multi_time >= single_time:
        print("\nObservation:")
        print("Threaded execution is slower or similar in performance.")
        print("Reason: Python's Global Interpreter Lock (GIL) allows")
        print("only one thread to execute Python bytecode at a time.")
        print("For CPU-bound tasks, threads compete for the GIL,")
        print("causing context-switching overhead without true parallelism.")
        print("Recommendation: Use multiprocessing for CPU-intensive work.")
    else:
        print("\nObservation:")
        print("A slight improvement was observed, likely due to")
        print("system-specific scheduling effects.")
        print("For CPU-bound workloads, multiprocessing is still")
        print("the preferred approach.")


if __name__ == "__main__":
    main()