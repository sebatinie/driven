import weakref
from collections import OrderedDict


class OptimizedLRUCache:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.cache = OrderedDict()

    def _remove_dead_reference(self, weak_obj):
        """
        Automatically remove entries whose objects
        have been garbage collected.
        """
        keys_to_remove = [
            key
            for key, ref in self.cache.items()
            if ref is weak_obj
        ]

        for key in keys_to_remove:
            self.cache.pop(key, None)

    def get(self, key):
        if key not in self.cache:
            return None

        obj = self.cache[key]()

        if obj is None:
            # Object already garbage collected
            del self.cache[key]
            return None

        # Update LRU order
        self.cache.move_to_end(key)

        return obj

    def put(self, key, value):
        # Evict existing key first
        if key in self.cache:
            del self.cache[key]

        # LRU eviction
        if len(self.cache) >= self.max_size:
            evicted_key, _ = self.cache.popitem(last=False)
            print(f"Evicted LRU item: {evicted_key}")

        # Store weak reference
        self.cache[key] = weakref.ref(
            value,
            self._remove_dead_reference
        )

    def cleanup_deleted(self):
        """
        Remove entries whose objects have already
        been garbage collected.
        """
        dead_keys = [
            key
            for key, ref in self.cache.items()
            if ref() is None
        ]

        for key in dead_keys:
            del self.cache[key]

    def display(self):
        print("\nCurrent Cache State:")
        for key, ref in self.cache.items():
            obj = ref()
            status = "Alive" if obj else "Collected"
            print(f"{key}: {status}")


# Cacheable object type
class DataObject:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"DataObject(size={len(self.data)})"


# -------------------------
# Test
# -------------------------

cache = OptimizedLRUCache(max_size=3)

obj1 = DataObject("A" * 1000)
obj2 = DataObject("B" * 1000)
obj3 = DataObject("C" * 1000)

cache.put("key1", obj1)
cache.put("key2", obj2)
cache.put("key3", obj3)

# Access key1 -> becomes most recently used
print("Accessed:", cache.get("key1"))

# Forces eviction of key2 (LRU)
obj4 = DataObject("D" * 1000)
cache.put("key4", obj4)

cache.display()

# Delete external reference
del obj3

# Cleanup dead references
cache.cleanup_deleted()

print("\nAfter cleanup:")
cache.display()