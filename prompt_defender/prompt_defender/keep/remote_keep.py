from ..core import KeepExecutor, SafePromptResponse
from typing import Optional, Dict, Callable
from pydantic import BaseModel
import os
import requests


class KeepRequest(BaseModel):
    randomise_xml_tag: Optional[bool] = None
    prompt: str


class KeepResponse(BaseModel):
    shielded_prompt: str
    xml_tag: str


class RemoteKeepExecutor(KeepExecutor):
    api_key: Optional[str] = None
    api_url: str = "https://prompt.safetorun.com/keep"
    headers: Dict[str, str] = {}

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs["api_key"] if kwargs["api_key"] is not None else os.getenv("PROMPT_DEFENDER_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided via environment variable or parameter "
                             "(Use PROMPT_DEFENDER_API_KEY for environment variable)")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json",
                        "User-Agent": "PromptDefenderClient-v1.0"}

    def generate_prompt(self, prompt: str, randomise_xml_tag: bool) -> SafePromptResponse:
        """
        Generate a prompt that is safe to use

        :param prompt: the base prompt that you want to shield

        :return: a safe prompt
        """
        request = KeepRequest(
            prompt=prompt,
            randomise_xml_tag=randomise_xml_tag
        )

        request = request.json(exclude_none=True)

        response = requests.post(self.api_url, headers=self.headers, data=request, timeout=25)

        if response.status_code == 200:
            response = KeepResponse(**response.json())
            return SafePromptResponse(safe_prompt=response.shielded_prompt, xml_tag=response.xml_tag)
        else:
            raise Exception(
                f"Failed to call /keep endpoint: {response.status_code}, {response.text}, Request: {request}")


def remote_keep_builder(api_key: str = None) -> Callable[[], KeepExecutor]:
    """
    Factory function to build a Keep object

    :param api_key: the API key to use to authenticate with the remote endpoint

    :return: Keep object which you can call generate_prompt on to generate a safe prompt
    """
    if api_key is None:
        api_key = os.getenv("PROMPT_DEFENDER_API_KEY")

    if not api_key:
        raise ValueError("API key must be provided via environment variable or parameter "
                         "(Use PROMPT_DEFENDER_API_KEY for environment variable)")

    return lambda: RemoteKeepExecutor(api_key=api_key)
