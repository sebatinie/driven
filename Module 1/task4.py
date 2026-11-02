import concurrent.futures
import logging
import threading
import time
from multiprocessing import Manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------
# Shared State
# ----------------------------

class SharedState:
    def __init__(self):
        self._lock = threading.Lock()
        self.results = {}

    def update(self, task_id, value):
        with self._lock:
            self.results[task_id] = value

    def snapshot(self):
        with self._lock:
            return dict(self.results)


# ----------------------------
# CPU-bound Task
# ----------------------------

def cpu_bound_task(task_id, n, cancel_flag):
    """
    Simulates CPU-intensive computation.
    Checks for cancellation periodically and exits cleanly.
    """

    result = 0

    for i in range(n):
        if cancel_flag.is_set():
            logging.warning(
                f"CPU task {task_id} cancelled at iteration {i}"
            )
            print(f"[CPU] Task {task_id} cancelled at iteration {i}")
            return None

        # CPU-intensive computation
        result += i * i

        # Periodic cancellation check
        if i % 10000 == 0:
            pass
        print(f"[CPU] Task {task_id} completed.")
    return result

def io_bound_task(task_id, duration):
    print(f"[IO] Task {task_id} started. Duration = {duration}s")

    time.sleep(duration)

    print(f"[IO] Task {task_id} completed successfully.")
    return f"IO-{task_id}-completed"


# ----------------------------
# Orchestrator
# ----------------------------

def process_work(items):

    shared_state = SharedState()

    # Shared cancellation event for CPU workers
    cancel_flag = Manager().Event()

    cpu_futures = {}
    io_futures = {}

    with concurrent.futures.ProcessPoolExecutor() as process_pool, \
         concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_pool:

        # Route tasks
        for item in items:

            if item["type"] == "cpu":

                print(
                    f"Routing {item['id']} "
                    f"to ProcessPoolExecutor (CPU-bound)"
                )

                future = process_pool.submit(
                    cpu_bound_task,
                    item["id"],
                    item["iterations"],
                    cancel_flag
                )

                cpu_futures[future] = item

            elif item["type"] == "io":

                print(
                    f"Routing {item['id']} "
                    f"to ThreadPoolExecutor (IO-bound)"
                )

                future = thread_pool.submit(
                    io_bound_task,
                    item["id"],
                    item["duration"]
                )

                io_futures[future] = item

        # Simulate cancellation
        time.sleep(0.1)

        print("\nRequesting cancellation of CPU tasks...\n")
        cancel_flag.set()

        # Collect CPU results
        for future, item in cpu_futures.items():

            try:
                result = future.result()

                if result is not None:
                    shared_state.update(item["id"], result)
                    print(f"✓ Stored result for {item['id']}")
                else:
                    print(
                        f"✗ No result stored for "
                        f"{item['id']} (cancelled)"
                    )

            except Exception as e:
                print(f"CPU task {item['id']} failed: {e}")

        # Collect IO results with timeout
        for future, item in io_futures.items():

            try:
                result = future.result(timeout=2)

                shared_state.update(item["id"], result)

                print(
                    f"✓ Stored IO result for "
                    f"{item['id']}"
                )

            except concurrent.futures.TimeoutError:
                print(
                    f"✗ IO task {item['id']} "
                    f"exceeded timeout limit"
                )

            except Exception as e:
                print(
                    f"IO task {item['id']} failed: {e}"
                )

    return shared_state.snapshot()


# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":

    workload = [
        {
            "id": "cpu1",
            "type": "cpu",
            "iterations": 50_000_000
        },
        {
            "id": "cpu2",
            "type": "cpu",
            "iterations": 50_000_000
        },
        {
            "id": "io1",
            "type": "io",
            "duration": 1
        },
        {
            "id": "io2",
            "type": "io",
            "duration": 3
        }
    ]

    results = process_work(workload)

    print("\n========== FINAL RESULTS ==========")
    print(results)

    print("\nValidation Checks")

    if "cpu1" not in results:
        print("**cpu1 was cancelled and did not modify shared state")

    if "cpu2" not in results:
        print("**cpu2 was cancelled and did not modify shared state")

    if "io1" in results:
        print("**io1 completed successfully")

    if "io2" in results:
        print("**io2 completed successfully")