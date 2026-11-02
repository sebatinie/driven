import time
from concurrent.futures import ProcessPoolExecutor


def cpu_bound_task(n):
    total = 0

    for i in range(n):
        total += i * i

    return total


def sequential_execution(tasks):
    start = time.time()

    results = [cpu_bound_task(task) for task in tasks]

    elapsed = time.time() - start

    print(f"Sequential execution time: {elapsed:.2f} seconds")

    return results, elapsed


def parallel_execution(tasks):
    start = time.time()

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_bound_task, tasks))

    elapsed = time.time() - start

    print(f"Multiprocessing execution time: {elapsed:.2f} seconds")

    return results, elapsed


def main():
    tasks = [10_000_000] * 4

    print("Starting CPU-bound workload...")

    _, sequential_time = sequential_execution(tasks)

    _, parallel_time = parallel_execution(tasks)

    print("\n=== Performance Summary ===")
    print(f"Sequential:      {sequential_time:.2f} seconds")
    print(f"Multiprocessing: {parallel_time:.2f} seconds")

    if parallel_time < sequential_time:
        print(
            "Multiprocessing performed better because "
            "multiple CPU cores were utilized."
        )
    else:
        print(
            "Performance gain was limited by system resources "
            "or workload characteristics."
        )


if __name__ == "__main__":
    main()