# Exceptions to send more explicit errors

class WrongAPIKeyException(Exception):
    """
    Raised if no working API key is provided (the Tensor server returns 403
    errors)
    """
    pass


class NoJSONException(Exception):
    """
    Raised when the response from the Sanctum Trade API does not contain a JSON
    body.
    """
    pass


class TransactionFailedException(Exception):
    """
    Raised when the Solana transaction fails to execute.
    """
    pass
