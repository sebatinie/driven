import pickle
import os


def save_settings(settings, filepath):
    """
    Save settings dictionary to a pickle file.
    """

    try:
        with open(filepath, 'wb') as f:
            pickle.dump(settings, f)

    except (OSError, pickle.PickleError) as e:
        print(f"Error saving settings: {e}")


def load_settings(filepath):
    """
    Load settings dictionary from a pickle file.

    Returns:
        dict: Loaded settings or an empty dictionary on failure.
    """

    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        # Validate loaded data
        if not isinstance(data, dict):
            print("Warning: settings file does not contain a dictionary.")
            return {}

        return data

    except (
        FileNotFoundError,
        EOFError,
        pickle.UnpicklingError,
        AttributeError,
        ImportError,
        IndexError,
        OSError
    ) as e:
        print(f"Warning: could not load settings: {e}")
        return {}


# Normal usage
settings = {
    'theme': 'dark',
    'language': 'en'
}

save_settings(settings, 'config.pkl')

loaded = load_settings('config.pkl')
print("Loaded settings:", loaded)

# Test case: missing file
loaded_missing = load_settings('nonexistent.pkl')
print("Missing file result:", loaded_missing)

# Test case: corrupted data
with open('corrupted.pkl', 'wb') as f:
    f.write(b'not valid pickle data')

loaded_corrupted = load_settings('corrupted.pkl')
print("Corrupted file result:", loaded_corrupted)

# Test case: valid pickle but wrong type
with open('invalid_type.pkl', 'wb') as f:
    pickle.dump(['not', 'a', 'dict'], f)

loaded_invalid = load_settings('invalid_type.pkl')
print("Invalid type result:", loaded_invalid)