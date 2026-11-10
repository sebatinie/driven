class InvalidRequestError(Exception):
    """Custom exception for invalid API requests."""
    pass


def process_request(request_params):
    try:
        # Required keys
        required_keys = ['user_id', 'action', 'value']

        if request_params["action"] == "crash":
            x = 10 / 0
        # Validate request
        for key in required_keys:
            if key not in request_params:
                raise InvalidRequestError(
                    f"Missing required parameter: {key}"
                )

        # Transform keys to uppercase
        transformed_data = {
            key.upper(): value
            for key, value in request_params.items()
        }

        # Success response
        return {
            'status': 'success',
            'message': 'Request processed successfully',
            'data': transformed_data
        }

    except InvalidRequestError as e:
        # Standardized error response
        return {
            'status': 'error',
            'message': str(e),
            'code': 'INVALID_REQUEST'
        }
    except Exception as e:
        print(f"Unexpected error: {e}")

        return {
            "status": "error",
            "message": "Internal server error",
            "code": "INTERNAL_ERROR"
        }


# request_data = {
#     "user_id": input("Enter user ID: "),
#     "action": input("Enter action: "),
#     "value": int(input("Enter value: "))
# }

# result = process_request(request_data)

# print(result)

# # Test input
# request_data = {
#     'user_id': '123',
#     'action': 'delete',
#     'value': 50
# }
test_cases = [

    # Success
    {
        "user_id": "123",
        "action": "delete",
        "value": 50
    },

    # Missing user_id
    {
        "action": "delete",
        "value": 50
    },

    # Missing action
    {
        "user_id": "123",
        "value": 50
    },

    # Missing value
    {
        "user_id": "123",
        "action": "delete"
    },

    # Empty dictionary
    {
    },

    # Unexpected error
    {
        "user_id": "123",
        "action": "crash",
        "value": 50
    }
]


for i, test_case in enumerate(test_cases, start=1):

    print(f"\nTest Case {i}")

    result = process_request(test_case)

    print(result)