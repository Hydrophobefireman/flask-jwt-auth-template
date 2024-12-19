# A special error class which is caught by our request handler
# is you throw this error anywhere during a request execution,
# we will send the error message in a json respose
class AppException(Exception):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message
