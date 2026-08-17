class AppError(Exception):
    """Base class for application errors."""

class ConfigError(AppError):
    pass

class DataUnavailableError(AppError):
    """When data cannot be fetched but this is a recoverable situation."""

class APITimeoutError(AppError):
    pass

class APIError(AppError):
    pass

class ParseError(AppError):
    pass
