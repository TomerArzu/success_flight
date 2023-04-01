class SuccessFlightException(Exception):
    def __init__(self, message, exception_message, error_code=None, http_status_code=None):
        super().__init__(message)
        self.message = message
        self.exception_message = exception_message
        self.error_code = error_code
        self.http_status_code = http_status_code


class DataSourceNotFoundException(SuccessFlightException):
    def __init__(self, message, exception_message, error_code=None, http_status_code=None):
        self.error_code = "DATA_SOURCE_ERROR.FILE_NOT_FOUND"
        self.http_status_code = 409
        super().__init__(message, exception_message, self.error_code, self.http_status_code)


class DataSourceParsingException(SuccessFlightException):
    def __init__(self, message, exception_message, error_code=None, http_status_code=None):
        self.error_code = "DATA_SOURCE_FORMAT_ERROR.UNWOUND_TYPE"
        self.http_status_code = 409
        super().__init__(message, exception_message, self.error_code, self.http_status_code)


class DataSourceLineHeadersException(SuccessFlightException):
    def __init__(self, message, exception_message, error_code=None, http_status_code=None):
        self.error_code = "DATA_SOURCE_FORMAT_ERROR.UNEXPECTED_LINE_HEADER"
        self.http_status_code = 409
        super().__init__(message, exception_message, self.error_code, self.http_status_code)


class FlightDataNotFoundException(SuccessFlightException):
    def __init__(self, message, exception_message, error_code=None, http_status_code=None):
        self.error_code = "FLIGHT_DATA.FLIGHT_NOT_FOUND"
        self.http_status_code = 404
        super().__init__(message, exception_message, self.error_code, self.http_status_code)
