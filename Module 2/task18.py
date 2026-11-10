import pickle
import os


def serialize_users(users, filename):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(users, f, protocol=pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        print(f"Serialization error: {e}")


def deserialize_users(filename):
    required_fields = {'id', 'name', 'email'}

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, 'rb') as f:
            users = pickle.load(f)

        # Validate top-level structure
        if not isinstance(users, list):
            return []

        # Validate each user record
        for user in users:

            if not isinstance(user, dict):
                return []

            if not required_fields.issubset(user.keys()):
                return []

        return users

    except (
        pickle.UnpicklingError,
        EOFError,
        AttributeError,
        ValueError,
        OSError
    ) as e:
        print(f"Deserialization error: {e}")
        return []


# Test
test_users = [
    {
        'id': 1,
        'name': 'Alice',
        'email': 'alice@example.com'
    },
    {
        'id': 2,
        'name': 'Bob',
        'email': 'bob@example.com'
    }
]

serialize_users(test_users, 'users.pkl')

result = deserialize_users('users.pkl')

print("Loaded users:")
print(result)

# Verify data integrity
assert result == test_users

print("\nRound-trip serialization successful")