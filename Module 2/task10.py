import json


def load_and_validate_customers(file_path):
    """
    Load customer data from a JSON file and validate records.

    Validation rules:
    - name must be non-empty
    - email must contain '@'
    - age must be a positive integer

    Args:
        file_path (str): Path to the JSON file

    Returns:
        tuple: (valid_customers, invalid_customers)
    """

    valid_customers = []
    invalid_customers = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            customers = json.load(file)

        for customer in customers:
            name = customer.get("name")
            email = customer.get("email")
            age = customer.get("age")

            is_valid = (
                isinstance(name, str)
                and name.strip() != ""
                and isinstance(email, str)
                and "@" in email
                and isinstance(age, int)
                and age > 0
            )

            if is_valid:
                valid_customers.append(customer)
            else:
                invalid_customers.append(customer)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax. {e}")

    return valid_customers, invalid_customers


# Test
if __name__ == "__main__":

    valid, invalid = load_and_validate_customers("customers.json")

    print("Valid Customers:")
    print(valid)

    print("\nInvalid Customers:")
    print(invalid)