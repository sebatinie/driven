class AuthenticationError(Exception):
    """
    Base exception for all authentication-related errors.
    """
    pass


class InvalidCredentialsError(AuthenticationError):
    def __init__(self):
        super().__init__(
            "Invalid username or password. "
            "Please verify your credentials and try again."
        )


class AccountLockedError(AuthenticationError):
    def __init__(self):
        super().__init__(
            "Account is locked due to multiple failed login attempts. "
            "Please wait or contact support."
        )


class SessionExpiredError(AuthenticationError):
    def __init__(self):
        super().__init__(
            "Your session has expired. "
            "Please log in again."
        )


def validate_login(username, password, account_status):

    valid_username = "admin"
    valid_password = "Password123"

    if account_status.lower() == "locked":
        raise AccountLockedError()

    if account_status.lower() == "expired":
        raise SessionExpiredError()

    if username != valid_username or password != valid_password:
        raise InvalidCredentialsError()

    return "Login Successful!"


if __name__ == "__main__":

    username = input("Enter username: ")
    password = input("Enter password: ")
    account_status = input(
        "Enter account status (active/locked/expired): "
    )

    try:
        result = validate_login(
            username,
            password,
            account_status
        )
        print(result)

    except AuthenticationError as e:
        print(f"Authentication Error: {e}")