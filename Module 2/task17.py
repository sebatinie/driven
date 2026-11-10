import pickle
import os


def serialize_deserialize_records(records, file_path):
    try:
        # Serialize records to file
        with open(file_path, 'wb') as f:
            pickle.dump(records, f, protocol=pickle.HIGHEST_PROTOCOL)

        # Deserialize records from file
        with open(file_path, 'rb') as f:
            loaded_records = pickle.load(f)

        return loaded_records

    except (pickle.PickleError, EOFError):
        return []

    except OSError:
        return []


def load_records(file_path):
    """
    Load records from an existing pickle file.
    Return an empty list if the file does not exist.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    except (pickle.PickleError, EOFError, OSError):
        return []


# Test data
records = [
    {
        'id': 1,
        'name': 'Alice',
        'email': 'alice@example.com',
        'timestamp': 1000
    },
    {
        'id': 2,
        'name': 'Bob',
        'email': 'bob@example.com',
        'timestamp': 2000
    }
]

# Serialize and deserialize
result = serialize_deserialize_records(records, 'users.pkl')

print("Original Records:")
print(records)

print("\nLoaded Records:")
print(result)

# Verify exact match
assert result == records

print("\nData integrity verified")

# Missing file test
missing = load_records('missing.pkl')
print("\nMissing File Result:")
print(missing)