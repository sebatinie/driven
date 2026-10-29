import threading
import time

class SharedCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            temp = self.count
            time.sleep(0.0001)
            self.count = temp + 1
    
    def get_count(self):
        return self.count

def worker(counter, thread_id, iterations):
    for i in range(iterations):
        counter.increment()
    print(f"Thread {thread_id} completed")

if __name__ == "__main__":
    counter = SharedCounter()
    threads = []
    num_threads = 5
    iterations_per_thread = 100
    
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(counter, i, iterations_per_thread))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    result = counter.get_count()
    print(f"Final count: {result}")
    print(f"Expected count: {num_threads * iterations_per_thread}")