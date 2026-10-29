import time
import weakref
import gc
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CacheEntry:
    obj_ref: weakref.ref
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0

    def get_object(self):
        obj = self.obj_ref()
        if obj is not None:
            self.last_accessed = time.time()
            self.access_count += 1
        return obj


class CacheManager:
    def __init__(self, max_size=100, ttl_seconds=300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()

    def add(self, key, obj):
        """
        Add object to cache using weak reference.
        Object can still be garbage collected if
        no strong references exist elsewhere.
        """

        def cleanup_callback(_):
            self.cache.pop(key, None)

        self.cache[key] = CacheEntry(
            obj_ref=weakref.ref(obj, cleanup_callback)
        )

        self.cache.move_to_end(key)
        self._evict_if_needed()

    def get(self, key):
        #Retrieve object and update usage statistics.
        entry = self.cache.get(key)

        if not entry:
            return None

        obj = entry.get_object()

        # Object already collected by Python GC
        if obj is None:
            self.cache.pop(key, None)
            return None

        # Update LRU ordering
        self.cache.move_to_end(key)

        return obj

    def remove(self, key):
        self.cache.pop(key, None)

    def clear(self):
        self.cache.clear()
        gc.collect()

    def collect_expired(self):
        """
        Remove TTL-expired or dead entries.
        """
        current_time = time.time()
        expired = []

        for key, entry in list(self.cache.items()):
            obj = entry.obj_ref()

            if obj is None:
                expired.append(key)
                continue

            age = current_time - entry.last_accessed

            if age > self.ttl_seconds:
                expired.append(key)

        for key in expired:
            del self.cache[key]

        gc.collect()

    def _evict_if_needed(self):
        """
        LRU eviction policy.
        Removes least recently used entries
        when max size is exceeded.
        """
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def stats(self):
        result = {}

        for key, entry in self.cache.items():
            result[key] = {
                "access_count": entry.access_count,
                "last_accessed": entry.last_accessed,
                "alive": entry.obj_ref() is not None,
            }

        return result


# Example cacheable object
class DataObject:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

    def __repr__(self):
        print (self.name)
        return f"DataObject({self.name})"