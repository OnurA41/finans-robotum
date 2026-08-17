# Centralized configuration management
import os
from typing import Optional

class ConfigError(Exception):
    pass

class Config:
    REQUIRED = ["TELEGRAM_TOKEN", "CHAT_ID"]

    def __init__(self):
        self.TELEGRAM_TOKEN: Optional[str] = os.getenv("TELEGRAM_TOKEN")
        self.CHAT_ID: Optional[str] = os.getenv("CHAT_ID")
        self.GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.validate()

    def validate(self):
        missing = [k for k in self.REQUIRED if not getattr(self, k)]
        if missing:
            raise ConfigError(f"Missing required config: {', '.join(missing)}")
