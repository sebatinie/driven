import sys

def track_object_lifecycle(operations):
    """
    Track object lifecycle through create, reference, and dereference operations.

    Args:
        operations: List of tuples (operation_type, object_id)

    Returns:
        Dictionary with keys: 'in_memory', 'garbage_eligible', 'summary'
    """
    objects = {}
    reference_counts = {}

    for operation in operations:
        op_type = operation[0]
        obj_id = operation[1]

        if op_type == 'create':
            objects[obj_id] = True
            reference_counts[obj_id] = 1
            print(f"Created object: {obj_id}, Ref Count = 1")

        elif op_type == 'reference':
            if obj_id in reference_counts:
                reference_counts[obj_id] += 1
                print(
                    f"Referenced object: {obj_id}, "
                    f"Ref Count = {reference_counts[obj_id]}"
                )

        elif op_type == 'dereference':
            if obj_id in reference_counts and reference_counts[obj_id] > 0:
                reference_counts[obj_id] -= 1
                print(
                    f"Dereferenced object: {obj_id}, "
                    f"Ref Count = {reference_counts[obj_id]}"
                )

                if reference_counts[obj_id] == 0:
                    print(
                        f"Object {obj_id} is eligible for garbage collection"
                    )

    in_memory = [
        obj_id
        for obj_id in objects
        if reference_counts[obj_id] > 0
    ]

    garbage_eligible = [
        obj_id
        for obj_id in objects
        if reference_counts[obj_id] == 0
    ]

    return {
        'in_memory': in_memory,
        'garbage_eligible': garbage_eligible,
        'summary': {
            obj_id: reference_counts[obj_id]
            for obj_id in objects
        }
    }


# Test Data
operations = [
    ('create', 'A'),
    ('reference', 'A'),
    ('create', 'B'),
    ('reference', 'B'),
    ('dereference', 'A'),
    ('dereference', 'A'),
    ('dereference', 'B')
]

result = track_object_lifecycle(operations)

print("\n=== Final Memory Summary ===")
print("Objects Still In Memory:", result['in_memory'])
print("Garbage Collection Candidates:", result['garbage_eligible'])
print("Reference Counts:", result['summary'])