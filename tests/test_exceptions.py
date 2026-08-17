import logging
from src.exceptions import AppError, ConfigError, DataUnavailableError


def test_exceptions_hierarchy():
    assert issubclass(ConfigError, AppError)
    assert issubclass(DataUnavailableError, AppError)
