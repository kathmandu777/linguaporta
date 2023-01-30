from fastapi import HTTPException, status


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


class APIException(HTTPException):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.status_code, self.message)
