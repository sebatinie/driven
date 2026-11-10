import pickle


def serialize_and_transform(user_data):
    """
    Serialize user data and transform string values to uppercase.

    Args:
        user_data: dict with keys username, email, age, preferences

    Returns:
        tuple: (pickled_bytes, transformed_dict)
    """

    def transform_value(value):
        # Convert strings to uppercase
        if isinstance(value, str):
            return value.upper()

        # Recursively process dictionaries
        elif isinstance(value, dict):
            return {
                k: transform_value(v)
                for k, v in value.items()
            }

        # Recursively process lists
        elif isinstance(value, list):
            return [
                transform_value(item)
                for item in value
            ]

        # Leave other types unchanged
        else:
            return value

    # Serialize original data
    pickled_bytes = pickle.dumps(user_data)

    # Create transformed dictionary
    transformed_dict = {}

    for key, value in user_data.items():
        transformed_dict[key] = transform_value(value)
# for key, value in user_data.items():
#         if isinstance(value, str):
#             transformed_dict[key]=value.upper()
#         elif isinstance(value, dict):
#             transformed_dict[key]={
#                 k:v.upper() if isinstance(v,str) else v for k,v in value.items()
#             }
#         elif isinstance(value, list):
#             transformed_dict[key]=[item.upper() if isinstance(item,str)else item
#             for item in value
#             ]
#         else:
#             transformed_dict[key]=value
    return pickled_bytes, transformed_dict


def test_function():
    user = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 28,
        "preferences": {
            "theme": "dark",
            "notifications": "enabled",
            "devices": [
                "mobile",
                "laptop"
            ]
        }
    }

    # Serialize and transform
    pickled, transformed = serialize_and_transform(user)

    # Deserialize
    unpickled = pickle.loads(pickled)

    # Verify original data is preserved
    assert unpickled == user

    # Verify uppercase transformation
    assert transformed["username"] == "ALICE"
    assert transformed["email"] == "ALICE@EXAMPLE.COM"
    assert transformed["preferences"]["theme"] == "DARK"
    assert transformed["preferences"]["notifications"] == "ENABLED"
    assert transformed["preferences"]["devices"] == [
        "MOBILE",
        "LAPTOP"
    ]

    print("Original User:")
    print(user)

    print("\nTransformed User:")
    print(transformed)

    print("\nUnpickled User:")
    print(unpickled)

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_function()