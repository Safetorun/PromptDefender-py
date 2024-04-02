import logging
from typing import Optional
from .prompt_defender_client import PromptDefenderClient
import os


def rapid_api_check() -> Optional[str]:
    return os.getenv("RAPID_API_KEY")


class PromptDefenderClientRapidApi(PromptDefenderClient):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    allow_pii: Optional[bool] = None
    api_key: Optional[str] = None
    api_url: str = "https://prompt.safetorun.com/wall"
    rapid_api_key: Optional[str] = None

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "https://prompt-defender.p.rapidapi.com/wall"
        self.rapid_api_key = kwargs["rapid_api_key"] if kwargs["rapid_api_key"] is not None else rapid_api_check()

        if not self.rapid_api_key:
            raise ValueError("Rapid API key must be provided via environment variable or parameter "
                             "(Use RAPID_API_KEY for environment variable)")

        self.headers = {"X-RapidAPI-Key": self.rapid_api_key,
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                        "User-Agent": "PromptDefenderClient-v1.0",
                        "x-rapidapi-host": "prompt-defender.p.rapidapi.com"
                        }

        logging.info(f"Created rapid API client")
