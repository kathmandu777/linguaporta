from fastapi import HTTPException, status


class ExpiredTokenException(HTTPException):
    def __init__(self, message: str = "Token has expired."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class InvalidTokenException(HTTPException):
    def __init__(self, message: str = "Invalid token."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class InvalidEmailOrPasswordException(HTTPException):
    def __init__(self, message: str = "Invalid email or password."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class InvalidCredentialsException(HTTPException):
    def __init__(self, message: str = "Invalid credentials."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class NotFoundException(HTTPException):
    def __init__(self, message: str = "Not found."):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message
        super().__init__(self.status_code, self.message)


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request."):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message
        super().__init__(self.status_code, self.message)
