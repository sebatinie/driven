from .exceptions import (
    APITimeoutError,
    APIAuthenticationError,
    APIDataValidationError
)

def get_user_from_api(user_id):
    if user_id == 1:
            return {
                "id": 1,
                "name": "John",
                "email": "john@example.com"
            }
    
    elif user_id == 2:
            raise APITimeoutError()
    
    elif user_id == 3:
            raise APIAuthenticationError()
    
    elif user_id == 4:
            raise APIDataValidationError()
    
    return {
            "id": user_id,
            "name": "Unknown User"
        }
def fetch_user_data(user_id):
    try:
        user_data = get_user_from_api(user_id)
        return {
            "status": "success",
            "data": user_data
        }

    except APITimeoutError:
        return {
            "status": "timeout",
            "message": "Request timed out"
        }

    except APIAuthenticationError:
        return {
            "status": "auth_failed",
            "message": "Authentication failed"
        }

    except APIDataValidationError:
        return {
            "status": "invalid_data",
            "message": "Data validation failed"
        }
    
def main(self):
    result = fetch_user_data(123)

    if result["status"] == "success":
        print("User data:", result["data"])
    else:
        print("Error:", result["message"])

