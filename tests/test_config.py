# tests for configuration and logging
import os
import logging
import pytest

from src.config import Config, ConfigError
from src.logging_config import configure_logging


def test_config_missing(monkeypatch):
    monkeypatch.delenv('TELEGRAM_TOKEN', raising=False)
    monkeypatch.delenv('CHAT_ID', raising=False)
    with pytest.raises(ConfigError):
        Config()


def test_config_present(monkeypatch):
    monkeypatch.setenv('TELEGRAM_TOKEN', 'fake-token')
    monkeypatch.setenv('CHAT_ID', '12345')
    c = Config()
    assert c.TELEGRAM_TOKEN == 'fake-token'
    assert c.CHAT_ID == '12345'


def test_logging_masking(caplog):
    configure_logging(level='INFO')
    logger = logging.getLogger('test')
    with caplog.at_level(logging.INFO):
        logger.info('This is a message with token=SECRET_TOKEN_1234567890')
    # Ensure the real secret does not appear in logs and masking is applied
    assert 'SECRET_TOKEN_1234567890' not in caplog.text
    assert '[REDACTED]' in caplog.text
