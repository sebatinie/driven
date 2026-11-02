import sys
import gc


def analyze_memory_retention(objects_data):
    """
    Analyzes object reference counts and identifies potential memory leaks.

    Args:
        objects_data: List of tuples (object_name, object_ref)

    Returns:
        Dictionary with keys: 'valid_count', 'issues', 'warnings'
    """

    result = {
        'valid_count': 0,
        'issues': [],
        'warnings': []
    }

    if objects_data is None:
        result['warnings'].append('Input is None')
        return result

    if not isinstance(objects_data, list):
        result['warnings'].append('Input is not a list')
        return result

    HIGH_REFCOUNT_THRESHOLD = 100

    for item in objects_data:

        # Validate tuple structure
        if not isinstance(item, tuple) or len(item) != 2:
            result['warnings'].append(
                f'Invalid entry format: {item}'
            )
            continue

        obj_name, obj_ref = item

        # Handle None values
        if obj_ref is None:
            result['warnings'].append(
                f'{obj_name}: object reference is None'
            )
            continue

        try:
            ref_count = sys.getrefcount(obj_ref)

            result['valid_count'] += 1

            print(
                f"Analyzing object '{obj_name}' "
                f"(Reference Count = {ref_count})"
            )

            # Detect abnormally high reference counts
            if ref_count > HIGH_REFCOUNT_THRESHOLD:
                warning_msg = (
                    f"{obj_name}: unusually high reference count "
                    f"({ref_count})"
                )

                result['warnings'].append(warning_msg)

                print(
                    f"WARNING: {obj_name} may be retaining "
                    f"more references than expected."
                )

            # Simple leak suspicion
            if ref_count > 10:
                result['issues'].append(
                    f"{obj_name}: possible memory retention "
                    f"(ref_count={ref_count})"
                )

        except Exception as e:
            result['issues'].append(
                f"{obj_name}: error analyzing object - {str(e)}"
            )

    # Force garbage collection
    unreachable = gc.collect()

    print(f"\nGarbage Collector reclaimed {unreachable} objects.")

    if unreachable > 0:
        result['warnings'].append(
            f'GC detected and cleaned {unreachable} unreachable objects '
            f'(possible circular references)'
        )

    return result


# Example Usage
if __name__ == "__main__":

    sample_list = [1, 2, 3]

    data = [
        ("sample_list", sample_list),
        ("empty_dict", {}),
        ("none_object", None),
        ("invalid_entry",)
    ]

    report = analyze_memory_retention(data)

    print("\n=== Memory Analysis Report ===")
    print(f"Valid Objects Analyzed : {report['valid_count']}")
    print(f"Issues                : {report['issues']}")
    print(f"Warnings              : {report['warnings']}")