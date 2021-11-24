

class EntropyError(Exception):
    """
    Raised when the entropy of the data is too low.
    """
    def __init__(self, message="EntropyError") -> None:
        super().__init__(message)


class APICallFailed(Exception):
    """
    Raised when the API call fails.
    """
    def __init__(self, message="APICallFailed") -> None:
        super().__init__(message)