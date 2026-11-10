import json


def serialize_orders(orders, filename):
    """
    Serialize orders to a binary file using JSON.
    """

    with open(filename, "wb") as file:
        json_bytes = json.dumps(orders).encode("utf-8")
        file.write(json_bytes)


def deserialize_orders(filename):
    """
    Deserialize orders from a binary file.
    """

    with open(filename, "rb") as file:
        json_bytes = file.read()

    return json.loads(json_bytes.decode("utf-8"))


# Example usage
orders = [
    {
        'customer': 'Alice',
        'products': [101, 102, 103],
        'timestamp': '2024-01-15T10:30:00'
    },
    {
        'customer': 'Bob',
        'products': [201],
        'timestamp': '2024-01-15T11:45:00'
    }
]


# Serialize
serialize_orders(orders, "orders.dat")

# Deserialize
loaded_orders = deserialize_orders("orders.dat")

# Verify data integrity
print("Original Orders:")
print(orders)

print("\nDeserialized Orders:")
print(loaded_orders)

print("\nData Integrity Check:")
print(orders == loaded_orders)