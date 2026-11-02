import threading
import time


class ThreadSafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            temp = self.count
            time.sleep(0.001)  # Simulate processing
            self.count = temp + 1

    def get_count(self):
        with self.lock:
            return self.count

    def reset(self):
        with self.lock:
            self.count = 0


def worker_task(counter, worker_id, iterations):
    for i in range(iterations):
        counter.increment()

        if i % 100 == 0:
            print(
                f"Worker {worker_id}: "
                f"Current Count = {counter.get_count()}"
            )


def main():
    counter = ThreadSafeCounter()
    threads = []

    num_workers = 5
    iterations = 200

    print("Starting worker threads...")

    for i in range(num_workers):
        thread = threading.Thread(
            target=worker_task,
            args=(counter, i, iterations)
        )

        threads.append(thread)
        thread.start()

    # Wait for all workers to finish
    for thread in threads:
        thread.join()

    final_count = counter.get_count()
    expected = num_workers * iterations

    print("\n=== Final Results ===")
    print(f"Final count: {final_count}")
    print(f"Expected count: {expected}")

    if final_count == expected:
        print("SUCCESS: Counter is thread-safe.")
    else:
        print(
            f"FAILED: Expected {expected}, "
            f"but got {final_count}"
        )


if __name__ == "__main__":
    main()