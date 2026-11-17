class TransactionException(Exception):
    """Base exception for all transaction-related errors."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details

    def handle_error(self):
        return f"Transaction Error: {self.message}"


class InsufficientFundsException(TransactionException):
    """Raised when account balance is not enough."""

    def __init__(self, account_number, balance, amount):
        message = f"Insufficient funds in account {account_number}"
        details = {
            "balance": balance,
            "required_amount": amount
        }
        super().__init__(message, details)

    def handle_error(self):
        return (
            f"Insufficient Funds: Available Balance = "
            f"{self.details['balance']}, "
            f"Required = {self.details['required_amount']}"
        )


class InvalidAccountException(TransactionException):
    """Raised when account number does not exist."""

    def __init__(self, account_number):
        message = f"Invalid account number: {account_number}"
        super().__init__(message)

    def handle_error(self):
        return f"Account Validation Failed: {self.message}"


class NetworkFailureException(TransactionException):
    """Raised when a network failure occurs."""

    def __init__(self):
        message = "Network connection lost during transaction"
        super().__init__(message)

    def handle_error(self):
        return "Network Failure: Please retry the transaction later."


class TransactionProcessor:
    def __init__(self):
        # Sample account database
        self.accounts = {
            "ACC1001": 5000,
            "ACC1002": 2000,
            "ACC1003": 10000
        }

    def validate_account(self, account_number):
        if account_number not in self.accounts:
            raise InvalidAccountException(account_number)

    def check_funds(self, account_number, amount):
        balance = self.accounts[account_number]

        if balance < amount:
            raise InsufficientFundsException(
                account_number,
                balance,
                amount
            )

    def execute_transaction(
        self,
        account_number,
        amount,
        simulate_network_failure=False
    ):
        self.validate_account(account_number)
        self.check_funds(account_number, amount)

        if simulate_network_failure:
            raise NetworkFailureException()

        self.accounts[account_number] -= amount

        return (
            f"Transaction Successful! "
            f"Withdrawn: {amount}, "
            f"Remaining Balance: "
            f"{self.accounts[account_number]}"
        )

    def process_transaction(
        self,
        account_number,
        amount,
        simulate_network_failure=False
    ):
        try:
            result = self.execute_transaction(
                account_number,
                amount,
                simulate_network_failure
            )

            print(result)

        except TransactionException as e:
            print(e.handle_error())
            print(f"Error Details: {e.details}")


# Driver Code
if __name__ == "__main__":

    processor = TransactionProcessor()

    print("\n--- Successful Transaction ---")
    processor.process_transaction("ACC1001", 1000)

    print("\n--- Invalid Account ---")
    processor.process_transaction("ACC9999", 1000)

    print("\n--- Insufficient Funds ---")
    processor.process_transaction("ACC1002", 5000)

    print("\n--- Network Failure ---")
    processor.process_transaction(
        "ACC1003",
        2000,
        simulate_network_failure=True
    )