import pickle
from datetime import datetime


def serialize_task(task_data):
    """
    Serialize a task dictionary to bytes.
    """
    return pickle.dumps(task_data)


def deserialize_task(serialized_data):
    """
    Deserialize bytes back into a task dictionary.
    """
    return pickle.loads(serialized_data)


if __name__ == "__main__":

    # Step 1: Create a sample task dictionary
    task = {
        "name": "DataProcessingJob",
        "timestamp": datetime.now().isoformat(),
        "status": "COMPLETED",
        "configuration": {
            "batch_size": 1000,
            "retry_count": 3
        }
    }

    print("Original Task:")
    print(task)

    # Step 2: Serialize the dictionary to bytes
    serialized_task = serialize_task(task)

    print("\nSerialized Data:")
    print(serialized_task)

    # Step 3: Simulate passing data to another process
    received_task = deserialize_task(serialized_task)

    print("\nDeserialized Task:")
    print(received_task)

    # Step 4: Verify the deserialized object matches the original
    if task == received_task:
        print("\nVerification Successful: Deserialized object matches the original.")
    else:
        print("\nVerification Failed: Objects do not match.")