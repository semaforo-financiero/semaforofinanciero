class AppException(Exception):
    def __init__(self, status_code: int = 400, code: str = "ERROR", message: str = "An error occurred", details: dict | None = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class UserAlreadyExists(AppException):
    def __init__(self, message: str = "User already registered", details: dict | None = None):
        super().__init__(status_code=409, code="USER_ALREADY_EXISTS", message=message, details=details)


class AuthError(AppException):
    def __init__(self, message: str = "Authentication error", details: dict | None = None):
        super().__init__(status_code=401, code="AUTH_ERROR", message=message, details=details)


class ProfileCreationError(AppException):
    def __init__(self, message: str = "Profile creation failed", details: dict | None = None):
        super().__init__(status_code=500, code="PROFILE_CREATION_FAILED", message=message, details=details)
