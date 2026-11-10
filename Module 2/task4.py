import pickle


def cache_objects(objects, filename):
    """
    Serialize multiple objects to a single cache file.
    """
    with open(filename, 'wb') as f:
        for obj in objects:
            pickle.dump(obj, f)


def load_cache(filename):
    """
    Deserialize all objects from a cache file.
    """
    objects = []

    try:
        with open(filename, 'rb') as f:
            while True:
                try:
                    obj = pickle.load(f)
                    objects.append(obj)

                except EOFError:
                    # Normal end of file
                    break

                except (
                    pickle.UnpicklingError,
                    AttributeError,
                    ImportError,
                    IndexError
                ) as e:
                    print(f"Warning: cache file is corrupted: {e}")
                    break

    except FileNotFoundError:
        print(f"Cache file '{filename}' not found.")

    return objects


def test():
    data = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        [1, 2, 3]
    ]

    cache_objects(data, 'test_cache.pkl')

    loaded = load_cache('test_cache.pkl')

    print(f"Original: {data}")
    print(f"Loaded:   {loaded}")

    assert loaded == data, "Mismatch between original and loaded data"

    print("✅ Cache serialization/deserialization successful")


if __name__ == "__main__":
    test()