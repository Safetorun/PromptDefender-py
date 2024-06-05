from typing import Optional

from pydantic import BaseModel


class SafePromptResponse(BaseModel):
    safe_prompt: str
    canary: Optional[str] = None
    xml_tag: Optional[str] = None


class KeepExecutor(BaseModel):

    def generate_prompt(self, prompt: str, randomise_xml_tag: bool) -> SafePromptResponse:
        """
        Generate a prompt that is safe to use

        :param prompt: the base prompt that you want to shield
        :param randomise_xml_tag: whether to randomise the xml tag

        :return: a safe prompt
        """
        return SafePromptResponse(safe_prompt=prompt)
