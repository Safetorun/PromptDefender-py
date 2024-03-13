from typing import Optional, List
from pydantic import BaseModel, validator


class PromptValidator(BaseModel):
    max_length: Optional[int] = None
    acceptable_values: Optional[List[str]] = None

    def validate_prompt(self, prompt: str) -> bool:
        """
        Validate a prompt

        :param prompt: The prompt to validate

        :return:
        """
        if self.max_length is not None and len(prompt) > self.max_length:
            return False

        if self.acceptable_values is not None and prompt not in self.acceptable_values:
            return False

        return True
