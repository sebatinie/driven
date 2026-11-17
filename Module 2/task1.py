# obj = {"name": "Jenny", "age": 25}

# # Pickling
# pickle.dump(obj, open("data.pkl", "wb"))
# # Unpickling
# loaded = pickle.load(open("data.pkl", "rb"))
# #print(loaded)

# pickle.dump(obj, file) # write pickled object to file
# pickle.dumps(obj) # return pickled object as bytes
# with open('data.pkl', 'rb') as file:
#     data = pickle.load(file)
# print(data)
# # read pickled object from file
# pickle.loads(bytes) 

import pickle


class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age


class VersionedUserData:
    def __init__(self, version, user):
        self.version = version
        self.user = user


def serialize_user(user, version, filename):
    """
    Wrap the user in a versioned container and save it to a file.
    """
    container = VersionedUserData(version, user)

    with open(filename, "wb") as file:
        pickle.dump(container, file)


def deserialize_user(filename):
    """
    Load the versioned container from a file.
    """
    with open(filename, "rb") as file:
        container = pickle.load(file)

    return container


# Test
if __name__ == "__main__":
    # Create a user
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        age=30
    )

    filename = "user_data.pkl"

    # Save with version 1
    serialize_user(user, version=1, filename=filename)

    # Load the data back
    loaded_container = deserialize_user(filename)

    # Check version and print user information
    if loaded_container.version == 1:
        loaded_user = loaded_container.user
        print(
            f"Name: {loaded_user.name}, "
            f"Email: {loaded_user.email}, "
            f"Age: {loaded_user.age}"
        )