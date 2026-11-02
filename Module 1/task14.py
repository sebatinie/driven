import threading


class ThreadSafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self, times):
        for _ in range(times):
            with self.lock:
                self.count += 1

    def get_count(self):
        with self.lock:
            return self.count


def worker(counter, iterations):
    counter.increment(iterations)


counter = ThreadSafeCounter()
threads = []

for i in range(5):
    t = threading.Thread(
        target=worker,
        args=(counter, 1000)
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final count: {counter.get_count()}")
print("Expected: 5000")

if counter.get_count() == 5000:
    print("PASS: Counter is thread-safe")
else:
    print("FAIL: Race condition detected")