import logging
import os
from typing import Optional, Dict

import requests
from pydantic import BaseModel

import time
from functools import wraps


def retry(attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Failed to execute {func.__name__}, retrying in {delay} seconds... {e}")
                    time.sleep(delay)
            raise Exception(f"Failed to execute {func.__name__} after {attempts} attempts")

        return wrapper

    return decorator


class WallRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    scan_pii: Optional[bool] = None
    xml_tag: Optional[str] = None
    check_badwords: Optional[bool] = None
    fast_check: Optional[bool] = None


class WallResponse(BaseModel):
    potential_jailbreak: bool
    contains_pii: Optional[bool] = None
    potential_xml_escaping: Optional[bool] = None
    suspicious_user: Optional[bool] = None
    suspicious_session: Optional[bool] = None


class PromptDefenderClient(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    allow_pii: Optional[bool] = None
    api_key: Optional[str] = None
    api_url: str = "https://prompt.safetorun.com/wall"
    check_badwords: Optional[bool] = None
    fast_check: Optional[bool] = None
    headers: Dict[str, str] = {}

    def __init__(self, /, **kwargs):

        super().__init__(**kwargs)
        self.api_key = kwargs["api_key"] if kwargs["api_key"] is not None else os.getenv("PROMPT_DEFENDER_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided via environment variable or parameter "
                             "(Use PROMPT_DEFENDER_API_KEY for environment variable)")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json",
                        "User-Agent": "PromptDefenderClient-v1.0"}

    @retry(attempts=5, delay=2)
    def call_remote_wall(self, prompt: str) -> WallResponse:

        request = WallRequest(
            prompt=prompt,
            user_id=self.user_id,
            session_id=self.session_id,
            scan_pii=self.allow_pii,
            check_badwords=self.check_badwords,
            fast_check=self.fast_check
        )
        
        request = request.json(exclude_none=True)
        logging.info(f"Calling /wall endpoint with request: {request}")
        response = requests.post(self.api_url, headers=self.headers, data=request, timeout=25)
        logging.info(f"Response from /wall endpoint: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return WallResponse(**response.json())
        else:
            raise Exception(
                f"Failed to call /wall endpoint: {response.status_code}, {response.text}, Request: {request}")
