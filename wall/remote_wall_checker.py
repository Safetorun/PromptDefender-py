import os
import requests
from pydantic import BaseModel, ValidationError
from dataclasses import dataclass
from typing import Optional


class WallRequest(BaseModel):
    user_id: str
    session_id: str
    prompt: str
    scan_pii: bool
    xml_tag: Optional[str] = None


@dataclass
class WallResponse:
    contains_pii: Optional[bool]
    potential_jailbreak: bool
    potential_xml_escaping: Optional[bool]
    suspicious_user: Optional[bool]
    suspicious_session: Optional[bool]


class PromptDefenderClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_url = "https://prompt.safetorun.com/wall"
        self.api_key = api_key if api_key is not None else os.getenv("PROMPT_DEFENDER_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided via environment variable or parameter")

    def call_remote_wall(self, request: WallRequest) -> WallResponse:
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        response = requests.post(self.api_url, headers=headers, data=request.json(), timeout=60)
        if response.status_code == 200:
            data = response.json()
            return WallResponse(**data)
        else:
            raise Exception(f"Failed to call /wall endpoint: {response.status_code}, {response.text}")


# Example usage
if __name__ == "__main__":
    try:
        client = PromptDefenderClient()
        request = WallRequest(
            user_id="user123",
            session_id="session456",
            prompt="This is a test prompt.",
            scan_pii=True,
            xml_tag="<xmltag>"
        )
        response = client.call_wall_endpoint(request)
        print(response)
    except ValueError as e:
        print(e)
    except ValidationError as e:
        print(e.json())
